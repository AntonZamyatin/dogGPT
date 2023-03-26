from typing import List, Optional, TYPE_CHECKING
import logging
from telegram import ext, Chat
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
        message_handler: MessageHandler = MessageHandler(filters.TEXT &\
                                                         (~filters.COMMAND),
                                                         self.message_proc)
        self.app.add_handler(start_handler)
        self.app.add_handler(message_handler)        

    async def start(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        await context.bot.send_message(chat_id=update.effective_chat.id,
                                       text="I'm a bot, please talk to me!")
        
    async def message_proc(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        user_name = update.effective_user.full_name
        chat = update.effective_chat
        if chat.type == Chat.GROUP:
            print('have_message')
            await self.dog.process_group_message(update)
    
    def run(self) -> None:
        self.app.run_polling() 