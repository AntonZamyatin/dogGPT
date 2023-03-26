import os
from datetime import datetime
from time import sleep
from tg_bot import TG_BOT
import openai
from dotenv import load_dotenv

class Dog():

    def __init__(self):
        self.__set_credentials()
        self.tg_bot: TG_BOT = TG_BOT(self, self.tg_bot_token)
        self.root: str = os.path.dirname(os.path.realpath(__file__))
        self.log_path: str = self.root + '/logs'
        self.img_path: str = self.root + '/img'
        
    def __set_credentials(self) -> None:
        load_dotenv()
        self.openai_org_id: str = os.getenv('OpenAI_ORG_ID')
        self.openai_api_key: str = os.getenv('OpenAI_API_KEY')
        self.vrss_api_key: str = os.getenv('VRSS_API_KEY')
        self.tg_bot_token: str = os.getenv('TG_BOT_TOKEN')
    
    def write_to_botlog(self, text: str) -> None:
        now = datetime.now()
        logdir: str = f'{self.log_path}/botlog/'
        if not os.path.exists(logdir):
            os.makedirs(logdir)
        logfile: str = logdir + f'{now.year}_{now.month}_{now.day}.log'
        with open(logfile, 'a') as lf:
            print(f'{now.hour}:{now.minute}:{now.second}:{now.microsecond}',
                  text,sep='\t', file=lf)
    
    def run(self) -> None:
        self.write_to_botlog('INFO\tDog started')
        while True:
            try:
                self.write_to_botlog("INFO\tTG_BOT\tstarted")
                self.tg_bot.run()
            except KeyboardInterrupt:
                self.write_to_botlog('INFO\tDog\tstopped by user from keybord')
                break
            except Exception as e:
                self.write_to_botlog(f'ERROR\tTG_BOT\t{e}')
            sleep(1)

if __name__ == "__main__":
    dog = Dog()
    dog.run()