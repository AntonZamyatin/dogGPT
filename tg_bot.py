import re
from typing import List, Optional, TYPE_CHECKING
import logging
from telegram import ext, Chat, Update
from telegram.constants import ParseMode
from telegram.ext import filters, ApplicationBuilder, ContextTypes,\
                         CommandHandler, MessageHandler
if TYPE_CHECKING:
    from dogbot import Dog

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

def escape_markdown(text: str) -> str:
    """Escape characters in the given text that have special meaning in Markdown."""
    escape_chars = r'_[]()>#+-=|{}.!'
    return re.sub(r'([{}])'.format(re.escape(escape_chars)), r'\\\1', text)


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
        await update.message.reply_markdown_v2(text="I'm a bot, please talk to me!")
        
    async def message_proc(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        await context.bot.send_chat_action(chat_id=update.effective_chat.id, action='typing')
        user_name = update.effective_user.full_name
        chat = update.effective_chat
        if chat.type in (Chat.GROUP, Chat.SUPERGROUP):
            await self.dog.process_group_message(update)
        elif chat.type == Chat.PRIVATE:
            await self.dog.process_private_message(update)
            
    async def reply_on_message(self, update: Update, responce: str) -> None:
        await update.effective_message.reply_markdown_v2(escape_markdown(responce))
        
    def run(self) -> None:
        self.app.run_polling() 