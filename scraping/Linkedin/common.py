import time
from tkinter import *
from tkinter.simpledialog import askinteger

from app_configs.config_linkedin import CHROME_HEADLESS
from functions import get_driver


class LinkedinScraper():
    def get_pin_code(self):
        root = Tk()
        root.withdraw()
        pin_code = askinteger('Pin Code', 'Enter the pin code for continuation : ')
        root.destroy()
        return pin_code

    def is_blocked(self, driver):
        block_text = driver.find_element_by_css_selector('div._e6s span').text
        if block_text == 'Sorry, something went wrong.':
            return True

    def save_error_page(self, driver, url, dir_error_data):
        url = url.replace('/', '_')
        driver.save_screenshot(f'{dir_error_data}{url}.png')
        content = driver.page_source
        with open(f'{dir_error_data}{url}.html', 'w') as f:
            f.write(content)

    # Request to URL using Chrome driver
    def login(self, url, credential, dir_error_data):
        # driver = get_driver(url)
        driver = get_driver(url, headless=CHROME_HEADLESS)
        try:
            driver.find_element_by_name('session_key').send_keys(credential['Email'])
            driver.find_element_by_name('session_password').send_keys(credential['Password'])
            driver.find_element_by_css_selector('button.sign-in-form__submit-button').click()
            # WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.CSS_SELECTOR,
                                                                               # "#root > div._7om2 > div > div > div._7om2._2pip > div:nth-child(1) > div > div > a"))).click()
            # Check blocking
            driver.implicitly_wait(5)
            try:
                name = driver.find_element_by_css_selector('.profile-rail-card__actor-link').text
                if name == credential['User']:
                    print('Successfully logged in!')
                    driver.implicitly_wait(5)
            except:
                try:
                    print('Blocked!!')
                    pin_code = int(input('Enter the ***** pin code ****** for continuation : '))
                    driver.find_element_by_name('pin').send_keys(pin_code)
                    driver.find_element_by_css_selector('button#email-pin-submit-button').click()
                except Exception as e:
                    print('Failed to login!')
                    print(e)
                    self.save_error_page(driver, url, dir_error_data)
                # code = int(input('Enter 0 for continuation : '))
        except:
            self.save_error_page(driver, url, dir_error_data)
        return driver


