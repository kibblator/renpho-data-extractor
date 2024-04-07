import os
import json
from injector import singleton

class WeightDataRepository:
    @singleton
    def __init__(self):
        self.current_file_directory = os.path.dirname(os.path.abspath(__file__))
        self.images_directory = f"{self.current_file_directory}/images/"
        self.weight_data_path = f'{self.images_directory}data.json'

    def get_weight_data(self):
        data_path_exists = os.path.exists(self.weight_data_path)

        if data_path_exists:
            with open(self.weight_data_path, 'r') as file:
                data = file.read()
                return json.loads(data)
        else:
            return {}
    
    def store_weight_data(self, data):
        with open(f'{self.current_file_directory}/images/data.json', 'w') as file:
            json.dump(data, file)
    
    def remove_weight_data(self):
        os.remove(self.weight_data_path)