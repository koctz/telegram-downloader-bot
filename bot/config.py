import os
from dotenv import load_dotenv

load_dotenv()

BOT_TOKEN = os.getenv("BOT_TOKEN")
ADMINS = [x for x in os.getenv("ADMINS", "").split(",") if x]

DOWNLOAD_DIR = os.getenv("DOWNLOAD_DIR", "downloads")

