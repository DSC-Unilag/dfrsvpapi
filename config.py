import os
from dotenv import load_dotenv

load_dotenv()   # initialize dotenv

base_dir = os.path.abspath(os.getcwd())


class BaseConfig:
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SECRET_KEY = os.getenv("APP_SECRET")
    DB_USERNAME = os.getenv('DATABASE_USER')
    DB_PASSPHRASE = os.getenv('DATABASE_PASSWORD')
    # F_KEY_PATH = os.path.join(
    #     os.path.abspath(os.getcwd()),
    #     os.getenv('F_KEY')
    # )
    SQLALCHEMY_ECHO = False


class DevConfig(BaseConfig):
    DB_NAME = f"{os.getenv('DATABASE_HOST')}/{os.getenv('DATABASE_NAME')}"
    URI = f"{BaseConfig.DB_USERNAME}:{BaseConfig.DB_PASSPHRASE}@{DB_NAME}"
    SQLALCHEMY_DATABASE_URI = f"postgresql+psycopg2://{URI}"
    # SQLALCHEMY_DATABASE_URI = "sqlite:///test.db"


class Production(BaseConfig):
    DB_NAME = os.getenv('DATABASE-URL')
    URI = f"{BaseConfig.DB_USERNAME}:{BaseConfig.DB_PASSPHRASE}@{DB_NAME}"
    SQLALCHEMY_DATABASE_URI = f"postgresql+psycopg2://{URI}"


config_options = {
    "development": DevConfig,
    "dev": DevConfig,
    "production": Production
}
