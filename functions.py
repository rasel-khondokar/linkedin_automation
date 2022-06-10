from selenium.webdriver.chrome.options import Options
from get_chrome_driver import GetChromeDriver
from selenium import webdriver
import os
import logging
import time
from selenium.webdriver.remote.webelement import WebElement

from datetime import datetime


# Request to URL using Chrome driver
from settings import CHROMEDRIVER_PATH, DIRNAME_ERROR_LOG, TIME_ZONE, today
# Scroll to element
def scroll_to_element(driver, el: WebElement):
    driver.execute_script("arguments[0].scrollIntoView(true);", el)
    time.sleep(3)

# initialize the error log settings
def save_error_log(name):
    error_log = logging.getLogger(name)
    error_log_formatter = logging.Formatter('%(asctime)s : %(message)s')
    make_dir_if_not_exists(DIRNAME_ERROR_LOG)
    make_dir_if_not_exists(DIRNAME_ERROR_LOG + today + '/')
    error_log_file = logging.FileHandler(DIRNAME_ERROR_LOG + today + '/' + name + '.log', mode='a')
    error_log_file.setFormatter(error_log_formatter)
    error_log.setLevel(logging.ERROR)
    error_log.addHandler(error_log_file)
    return logging.getLogger(name)

# initialize the error log settings
def error_logger(source_name):
    return save_error_log(source_name)

# check directory if not exists then make directory
def make_dir_if_not_exists(file_path):
    dirs = file_path.split('/')
    if dirs:
        path = ''
        for dir in dirs:
            if dir:
                path = path + dir + '/'
                if not os.path.exists(path):
                    os.mkdir(path)
def get_driver(url, headless=True):
    option = Options()
    option.add_argument("--disable-notifications")
    option.add_argument('--no-sandbox')
    option.add_argument('--disable-dev-shm-usage')

    if headless:
        option.add_argument("--headless")

    chrome_dir = os.path.dirname(os.path.realpath(__file__))+'/'+CHROMEDRIVER_PATH
    make_dir_if_not_exists(chrome_dir)
    chrome_file_path = chrome_dir + '/chromedriver'
    try:
        driver = webdriver.Chrome(chrome_file_path, chrome_options=option)
        driver.get(url)
    except Exception as e:
        print('Selenium session is not Created !')

        if os.path.exists(chrome_file_path):
            os.remove(chrome_file_path)
            print(f'Removed {chrome_file_path} file!')

        download_driver = GetChromeDriver()
        download_driver.auto_download(extract=True, output_path=chrome_dir)
        print(f'Downloaded chrome driver for the chrome version {download_driver.matching_version()}!')
        driver = webdriver.Chrome(chrome_file_path, chrome_options=option)
        driver.get(url)

    driver.maximize_window()
    return driver