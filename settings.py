import os

import pytz as pytz
from datetime import datetime


CHROMEDRIVER_PATH = 'chromedriver_linux64'
DIRNAME_ERROR_LOG = 'ERROR/'
DIRNAME_REPORT = 'REPORT'
ROOT_PATH = os.path.dirname(os.path.realpath(__file__))

TIME_ZONE = pytz.timezone('Asia/Dhaka')
today = datetime.now().astimezone(TIME_ZONE).strftime('%Y-%m-%d')
PUSH_TIME_FOR_REQUEST_TO_URL = 3
