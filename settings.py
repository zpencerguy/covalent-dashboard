import os
from dotenv import load_dotenv

CWD = os.getcwd()
if os.path.isfile(os.path.join(CWD, ".env")):
    load_dotenv(os.path.join(CWD, ".env"))

API_KEY = os.getenv("API_KEY", "")
