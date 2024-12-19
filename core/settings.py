from environs import Env 
from dataclasses import dataclass

@dataclass
class Bots:
    bot_token: str
    bot_owner_id: int
    
    
@dataclass
class DataBase:
    url: str
    

@dataclass
class Settings:
    bots: Bots
    database: DataBase
        
    
def get_settings(path: str):
    '''Get setting from the file in path'''
    env = Env()
    env.read_env(path)
    
    return Settings(
        bots=Bots(
            bot_token = env.str("BOT_TOKEN"),
            bot_owner_id = env.int("BOT_OWNER_ID")
        ),
        database=DataBase(
            url=env.str("DB_URL"),
        )
    )

settings = get_settings("config.txt")