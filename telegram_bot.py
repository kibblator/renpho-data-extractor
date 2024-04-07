import requests
import os
from injector import inject, singleton

class TelegramBot:
    @inject
    @singleton
    def __init__(self):
        telegram_host = "https://api.telegram.org"
        bot_token = os.environ['BOT_TOKEN']
        
        self.offset = 0
        self.target_group_chat_id = os.environ['TARGET_CHAT_ID']
        self.base_url = f"{telegram_host}/bot{bot_token}/"
        self.base_file_url = f"{telegram_host}/file/bot{bot_token}/"

    def get_file_info(self, file_id):
        response = requests.get(self.base_url + f"getFile?file_id={file_id}")
        return response.json()['result']

    def download_file(self, file_id, file_name):
        file_info = self.get_file_info(file_id)
        if file_info:
            file_url = f"{self.base_file_url}{file_info['file_path']}"
            with open(f"{file_name}", 'wb') as f:
                response = requests.get(file_url)
                f.write(response.content)
            return True
        else:
            print("Failed to get file info.")
            return False

    def send_message(self, text):
        payload = {
            "chat_id": self.target_group_chat_id,
            "text": text
        }
        requests.post(f"{self.base_url}sendMessage", json=payload)

    def get_updates(self):
        print('Getting update')
        response = requests.get(self.base_url + f"getUpdates?offset={self.offset}")
        data = response.json()
        if 'result' in data and data['result']:
            updates = data['result']
            self.offset = updates[-1]['update_id'] + 1
            return updates
        else:
            return []