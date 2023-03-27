from typing import List, Optional, TYPE_CHECKING
import os
from datetime import datetime
from time import sleep
from tg_bot import TG_BOT
from gptapi import GPT_API
from dotenv import load_dotenv
from nltk.tokenize import RegexpTokenizer
from word_lists import DOGBOT_TRIGGERS, BAD_WORDS

if TYPE_CHECKING:
    from telegram import Update
    
class Dog():

    def __init__(self):
        self.__set_credentials()
        self.tg_bot: TG_BOT = TG_BOT(self, self.tg_bot_token)
        self.gptapi: GPT_API = GPT_API(self.openai_org_id,
                                       self.openai_api_key)
        self.root: str = os.path.dirname(os.path.realpath(__file__))
        self.log_path: str = self.root + '/logs'
        self.img_path: str = self.root + '/img'
        self.tokenizer: RegexpTokenizer = RegexpTokenizer(r'\w+')
        
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
            
    async def process_group_message(self, update: 'Update') -> None:
        message_text = update.effective_message.text
        if any([x in message_text.lower() for x in BAD_WORDS]):
            await update.effective_message.reply_text('Не ругайся')
        print('have message', message_text)
        tokens = self.tokenizer.tokenize(message_text)
        if tokens and tokens[0].lower() in DOGBOT_TRIGGERS:
            prompt = ' '.join(message_text.split()[1:])
            with open('log.txt', 'a') as lf:
                print(f'\tasking: {prompt}', file=lf)
            num_tokens, responce = self.gptapi.get_responce(prompt)
            responce = f'tokens used: {num_tokens}  |  it costs: {num_tokens*2*10**-4:.4f}¢\n---\n{responce}'
            await self.tg_bot.reply_on_message(update, responce)
    
    async def process_private_message(self, update: 'Update') -> None:
        message_text = update.effective_message.text
        num_tokens, responce = self.gptapi.get_responce(message_text)
        responce = f'tokens used: {num_tokens}  |  it costs: {num_tokens*2*10**-6:.2}$\n---\n{responce}'
        await self.tg_bot.reply_on_message(update, responce)
    
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