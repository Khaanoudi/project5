import os
from dotenv import load_dotenv

load_dotenv()

TICKERCHART_USERNAME = os.getenv("TICKERCHART_USERNAME")
TICKERCHART_PASSWORD = os.getenv("TICKERCHART_PASSWORD")
