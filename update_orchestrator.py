import os
import json
from injector import inject, singleton
from telegram_bot import TelegramBot
from push_data import store_data
from data_corrections import DataCorrectionService
from weight_data_repository import WeightDataRepository
from image_processing import ImageProcessorService

class UpdateOrchestrator:
    @inject
    @singleton
    def __init__(self, bot: TelegramBot, correction_service: DataCorrectionService, 
                 weight_data_repository: WeightDataRepository, image_processor_service: ImageProcessorService):
        self.bot = bot
        self.correction_service = correction_service
        self.weight_data_repository = weight_data_repository
        self.image_processor_service = image_processor_service
        current_file_directory = os.path.dirname(os.path.abspath(__file__))
        self.images_directory = f"{current_file_directory}/images/"

    def send_weight_data(self, data):
        store_data(data)
        self.bot.send_message("Data sent successfully")
        self.weight_data_repository.remove_weight_data()

    def remove_temp_weight_data(self):
        print('Removing data')
        self.weight_data_repository.remove_weight_data()

    def compose_submit_message(self, data):
        message = ""
        for index, (key, value) in enumerate(data.items(), start=1):
            message += f"{index}) {key}: {value}\n"

        self.bot.send_message(f'Data:\n{message}\n\nSubmit this data? (y/n)')       
        
    def convert_image_to_text(self, file_id):
        self.bot.send_message("Processing photo")
        file_name = f"{self.images_directory}photo_{file_id}.jpg"

        if self.bot.download_file(file_id, file_name):
            self.bot.send_message("Photo downloaded successfully!")
            data = self.image_processor_service.image_to_text(file_name)
            self.weight_data_repository.store_weight_data(data)
            self.compose_submit_message(data)

    def process_update(self, update):
        if 'text' in update['message']:
            data = self.weight_data_repository.get_weight_data()

            if update['message']['text'].lower() == "y":
                self.send_weight_data(data)
            elif update['message']['text'].lower() == "n":
                self.remove_temp_weight_data()
                self.bot.send_message('Removed data')
            else:
                print('Processing corrections')
                data = self.correction_service.update_values(data, update['message']['text'])
                self.compose_submit_message(data)
                
        elif 'photo' in update['message']:
            self.convert_image_to_text(update['message']['photo'][-1]['file_id'])            
        else:
            self.bot.send_message("Please send a photo.")
        