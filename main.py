import time
from injector import Injector
from telegram_bot import TelegramBot
from update_orchestrator import UpdateOrchestrator

def main():
    injector = Injector()
    bot = injector.get(TelegramBot)
    update_orchestrator = injector.get(UpdateOrchestrator)

    while True:
        updates = bot.get_updates()
        for update in updates:
            print('Processing update')
            update_orchestrator.process_update(update)
        time.sleep(5)
        

if __name__ == "__main__":
    main()