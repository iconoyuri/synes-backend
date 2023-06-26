
from dotenv import load_dotenv
import os
from functions import graph_driver

load_dotenv()


APP_NAME = os.getenv("APP_NAME")
APP_DOMAIN = os.getenv("APP_DOMAIN")
DATABASE_URI = os.getenv("DATABASE_URI")
DATABASE_DEFAULT_USERNAME = os.getenv("DATABASE_DEFAULT_USERNAME")
DATABASE_DEFAULT_PASSWORD = os.getenv("DATABASE_DEFAULT_PASSWORD")
MAIL_SENDER_ADDRESS = os.getenv("MAIL_SENDER_ADDRESS")
MAIL_APP_SENDER_PASSWORD = os.getenv("MAIL_APP_SENDER_PASSWORD")


default_driver = graph_driver(DATABASE_DEFAULT_USERNAME, DATABASE_DEFAULT_PASSWORD)
