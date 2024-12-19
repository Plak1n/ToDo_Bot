from environs import Env 
from dataclasses import dataclass

@dataclass
class Bots:
    bot_token: str
    bot_owner_id: int
    
    
@dataclass
class DataBase:
    host: str
    port: str
    dbname: str
    user: str
    password: str
    

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
            host=env.str("DB_HOST"),
            port=env.str("DB_PORT"),
            dbname=env.str("DB_NAME"),
            user=env.str("DB_USER"),
            password=env.str("DB_PASSWORD")
        )
    )

settings = get_settings("config.txt")