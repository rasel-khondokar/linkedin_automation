import json

from settings import DIRNAME_REPORT, today, ROOT_PATH
LINKEDIN_APP_NAME = 'linkedin'
LINKEDIN_MAIN_SITE = 'https://www.linkedin.com/'
LINKEDIN_SEARCH_URL = "https://www.linkedin.com/search/results/people/?geoUrn=%5B%22106215326%22%5D&network=%5B%22S%22%5D&origin=FACETED_SEARCH&sid=*rb"
DIRNAME_LINKEDIN_BLOCKING = f'LINKEDIN_BLOCKING/'
CHROME_HEADLESS = False
VIRTUAL_DISPLAY = False
# config
with open(f'{ROOT_PATH}/config.json') as reader:
    config_file = json.load(reader)
LINKEDIN_CREDENTIAL = config_file['linkedin']
dir_linkedin_error = f'{DIRNAME_REPORT}/{today}/{DIRNAME_LINKEDIN_BLOCKING}/'
DELAY_SHORT = 3
DELAY_LONG = 5



