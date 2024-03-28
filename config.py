import os
from pathlib import Path
from urllib.parse import quote_plus

from dotenv import load_dotenv

ROOT_PATH = Path(__file__).parent

load_dotenv(ROOT_PATH.joinpath(".env").resolve())

BASE_URL = "https://magento.softwaretestingboard.com/"
