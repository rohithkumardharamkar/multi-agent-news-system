from dotenv import load_dotenv
import os

load_dotenv()


TEMPERATURE = float(os.getenv("TEMPERATURE", 0))
MAX_TOKENS = int(os.getenv("MAX_TOKENS", 4000))
MAX_ARTICLES = int(os.getenv("MAX_ARTICLES", 10))
TOP_ARTICLES = int(os.getenv("TOP_ARTICLES", 5))
EMAIL_HOST = os.getenv("EMAIL_HOST","smtp.gmail.com")
EMAIL_PORT = int(os.getenv("EMAIL_PORT",587))
EMAIL_USER = os.getenv("EMAIL_USER","")
EMAIL_PASSWORD = os.getenv("EMAIL_PASSWORD","")
EMAIL_TO = os.getenv("EMAIL_TO","")
REPORT_FOLDER = "reports"
