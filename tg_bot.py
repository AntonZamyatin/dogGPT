from typing import List, Optional, TYPE_CHECKING
import logging
from telegram import ext
from telegram import Update
from telegram.ext import filters, ApplicationBuilder, ContextTypes,\
                         CommandHandler, MessageHandler
if TYPE_CHECKING:
    from dogbot import Dog

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

class TG_BOT():

    def __init__(self, dog: 'Dog', tg_token: str) -> None:
        self.dog: 'Dog' = dog
        self.tg_token: str = tg_token
        self.app: ext.Application =  ext.ApplicationBuilder()\
                                     .token(self.tg_token)\
                                     .build()
        self.setup_handlers()
    
    def setup_handlers(self):
        start_handler: CommandHandler = CommandHandler('start', 
                                                       self.start)
        echo_handler: MessageHandler = MessageHandler(filters.TEXT &\
                                                      (~filters.COMMAND),
                                                      self.echo)
        self.app.add_handler(start_handler)
        self.app.add_handler(echo_handler)        

    async def start(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        await context.bot.send_message(chat_id=update.effective_chat.id,
                                       text="I'm a bot, please talk to me!")
        
    async def echo(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        await context.bot.send_message(chat_id=update.effective_chat.id,
                                       text=update.message.text)
    
    def run(self) -> None:
        self.app.run_polling()  