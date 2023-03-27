from typing import List, Optional, TYPE_CHECKING
import os
from datetime import datetime
from time import sleep
from tg_bot import TG_BOT
from gptapi import GPT_API
from dotenv import load_dotenv
from nltk.tokenize import RegexpTokenizer
from word_lists import DOGBOT_TRIGGERS, BAD_WORDS
from functools import wraps
from logger import Logger

if TYPE_CHECKING:
    from telegram import Update, User, Chat
    
class Dog():

    def __init__(self):
        self.__set_credentials()
        self.tg_bot: TG_BOT = TG_BOT(self, self.tg_bot_token)
        self.gptapi: GPT_API = GPT_API(self.openai_org_id,
                                       self.openai_api_key)
        self.logger: Logger = Logger() 
        self.root: str = os.path.dirname(os.path.realpath(__file__))
        self.img_path: str = self.root + '/img'
        self.tokenizer: RegexpTokenizer = RegexpTokenizer(r'\w+')
        
    def __set_credentials(self) -> None:
        load_dotenv()
        self.openai_org_id: str = os.getenv('OpenAI_ORG_ID')
        self.openai_api_key: str = os.getenv('OpenAI_API_KEY')
        self.vrss_api_key: str = os.getenv('VRSS_API_KEY')
        self.tg_bot_token: str = os.getenv('TG_BOT_TOKEN')
    
    def send_typing():
        """Sends `action` while processing func command."""
        def decorator(func):
            @wraps(func)
            async def command_func(self, chat_type: str,
                                   message_text: str, update: str):
                await self.tg_bot.set_typing(update.effective_chat)
                return await func(self, chat_type, message_text, update)
            return command_func
        return decorator
    
    async def process_group_message(self, update: 'Update') -> None:
        self.logger.chatlog(message_text, chat, user)
        message_text: str = update.effective_message.text
        user: 'User' = update.effective_user
        chat: 'Chat' = update.effective_chat
        if any([x in message_text.lower() for x in BAD_WORDS]):
            await update.effective_message.reply_text('Не ругайся')
        tokens = self.tokenizer.tokenize(message_text)
        if tokens and tokens[0].lower() in DOGBOT_TRIGGERS:
            await self.process_gpt_request('chat', message_text, update)
    
    async def process_private_message(self, update: 'Update') -> None:
        self.logger.pmlog(message_text, user)
        user: 'User' = update.effective_user
        message_text = update.effective_message.text
        await self.process_gpt_request('pm', message_text, update)
        
    @send_typing()        
    async def process_gpt_request(self, chat_type: str,
                                  message_text: str, update: 'Update') -> None:
        chat_id: int = update.effective_chat.id
        prompt = ' '.join(message_text.split()[1:])
        with open('log.txt', 'a') as lf:
            print(f'\tasking: {prompt}', file=lf)
        num_tokens, responce = self.gptapi.get_responce(prompt)
        self.logger.logdog(responce, chat_type, chat_id)
        responce = f'{responce}\n---\ntokens used: {num_tokens}  |  it costs: {num_tokens*2*10**-4:.4f}¢'
        await self.tg_bot.reply_on_message(update, responce)
    
    def run(self) -> None:
        self.logger.botlog('INFO\tDog started')
        while True:
            try:
                self.logger.botlog("INFO\tTG_BOT\tstarted")
                self.tg_bot.run()
            except KeyboardInterrupt:
                self.logger.botlog('INFO\tDog\tstopped by user from keybord')
                break
            except Exception as e:
                self.logger.botlog(f'ERROR\tTG_BOT\t{e}')
            sleep(1)

if __name__ == "__main__":
    dog = Dog()
    dog.run()