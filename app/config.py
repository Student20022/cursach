import sys
from pydantic_settings import BaseSettings, SettingsConfigDict


ABBREVIATIONS = 'abbreviations.txt'
END_LOG = 'end.log'
START_LOG = 'start.log'
TIME_FMT = '%Y-%m-%d_%H:%M:%S.%f'
TOP_LIST_LIMIT = 16
ENGINE_OPTIONS = {'echo': True}


class Settings(BaseSettings):
    DB_NAME: str
    DB_USER: str
    DB_PASS: str
    DB_HOST: str
    DB_PORT: int
    DB_POSTGRES: str

    env_file: str = '.env'

    @property
    def DATABASE_URL_psycopg(self) -> str:
        return f'postgresql+psycopg2://{self.DB_USER}:{self.DB_PASS}@{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}'

    @property
    def DATABASE_URL(self) -> str:
        return f'postgresql+psycopg2://{self.DB_USER}:{self.DB_PASS}@{self.DB_HOST}:{self.DB_PORT}/{self.DB_POSTGRES}'

    if any('pytest' in arg for arg in sys.argv):
        env_file = '.env.test'

    model_config = SettingsConfigDict(env_file=env_file)


settings = Settings()
