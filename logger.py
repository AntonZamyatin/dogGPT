import os
from typing import Set, Tuple, TYPE_CHECKING
from datetime import datetime

if TYPE_CHECKING:
    from telegram import Update, User, Chat

class Logger():
    
    def __init__(self):
        self.root: str = os.path.dirname(os.path.realpath(__file__))
        self.log_path: str = self.root + '/logs'
        self.bot_log_path: str = f'{self.log_path}/botlog/'
        self.chats_log_path: str = f'{self.log_path}/groups/'
        self.users_log_path: str = f'{self.log_path}/users/'
        self.known_users_file: str = f'{self.users_log_path}known_users.tsv'
        self.known_chats_file: str = f'{self.chats_log_path}known_groups.tsv'
        self.check_dirs()
        self.known_user_ids: Set = self.get_known_users_ids()
        self.known_chat_ids: Set = self.get_known_groups_ids()
    
    def get_known_users_ids(self) -> Set:
        user_ids: Set = set()
        if os.path.isfile(self.known_users_file):
            with open(self.known_users_file, 'r') as uf:
                for line in uf:
                    user_ids.add(int(line.split()[2]))
        return user_ids
            
    def get_known_groups_ids(self) -> Set:
        group_ids: Set = set()
        if os.path.isfile(self.known_chats_file):
            with open(self.known_chats_file, 'r') as uf:
                for line in uf:
                    group_ids.add(int(line.split()[2]))
        return group_ids
    
    def check_dirs(self) -> None:
        for path in (self.bot_log_path,
                    self.chats_log_path,
                    self.users_log_path):
            if not os.path.exists(path):
                os.makedirs(path)    
    
    def get_datetime_now(self) -> Tuple[str, str]:
        now: datetime.now = datetime.now()
        date: str = f'{now.year}_{now.month:02d}_{now.day:02d}'
        time: str = f'{now.hour:02d}:{now.minute:02d}:{now.second:02d}'
        return date, time       
        
        
    def pmlog(self, text: str, user: 'User') -> None:
        date, time = self.get_datetime_now()
        user_id: int = user.id
        user_fname: str = user.full_name
        if not user_id in self.known_user_ids:
            self.log_new_user(user_id, user_fname)
        logfile: str = self.users_log_path + f'{user_id}.log'
        with open(logfile, 'a') as lf:
            print(date, time, user_fname, text,
                  sep='\t', file=lf)
    
    def log_new_user(self, user_id: str, user_fname:str) -> None:
        date, time = self.get_datetime_now()
        with open(self.known_users_file, 'a') as lf:
            print(date, time, user_id, user_fname,
                  sep='\t', file=lf)
    
    def chatlog(self, text: str, chat: 'Chat', user: 'User') -> None:
        date, time = self.get_datetime_now()
        chat_id: int = chat.id
        chat_name: str = chat.name
        user_id: int = user.id
        user_fname: str = user.full_name
        if not chat_id in self.known_chat_ids:
            self.log_new_chat(chat_id, chat_name)
        logfile: str = self.chats_log_path + f'{chat_id}.log'
        with open(logfile, 'a') as lf:
            print(date, time, user_id, user_fname, text,
                  sep='\t', file=lf)
    
    def log_new_chat(self, chat_id: str, chat_fname:str) -> None:
        date, time = self.get_datetime_now()
        with open(self.known_chats_file, 'a') as lf:
            print(date, time, chat_id, chat_fname,
                  sep='\t', file=lf)    
    
    def logdog(self, text:str, chat_type: str, chat_id: int) -> None:
        date, time = self.get_datetime_now()
        if chat_type == 'pm':
            logfile: str = self.users_log_path + f'{chat_id}.log'
        else:
            logfile: str = self.chats_log_path + f'{chat_id}.log'
        with open(logfile, 'a') as lf:
            print(date, time, 'DOG', text,
                  sep='\t', file=lf)
    
    def botlog(self, text: str) -> None:
        date, time = self.get_datetime_now()
        logfile: str = self.bot_log_path +\
                       f'{date}.log'
        with open(logfile, 'a') as lf:
            print(f'{time}', text, sep='\t', file=lf)    
        