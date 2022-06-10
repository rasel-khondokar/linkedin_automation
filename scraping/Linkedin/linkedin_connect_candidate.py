import time
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import Select

from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.wait import WebDriverWait

from app_configs.config_linkedin import LINKEDIN_CREDENTIAL, dir_linkedin_error, \
    LINKEDIN_APP_NAME, LINKEDIN_SEARCH_URL, DELAY_LONG, DELAY_SHORT
from functions import  error_logger, scroll_to_element

error_log = error_logger(LINKEDIN_APP_NAME)

def connect_to_profile(driver, candidate_links):
    count_total_candidate_request_send = 0
    count_candidate_already_added = 0
    count_already_added_in_connection = 0
    try:
        # open new tab
        driver.execute_script(f"window.open('{candidate_links}', 'new_window')")
        time.sleep(DELAY_SHORT)

        # Switch to the tab
        driver.switch_to.window(driver.window_handles[1])
        time.sleep(DELAY_SHORT)

        # Click Connect if not added before
        try:
            WebDriverWait(driver, 5).until(EC.presence_of_element_located((By.CSS_SELECTOR,"button.pvs-profile-actions__action.artdeco-button.artdeco-button--2.artdeco-button--primary.artdeco-button--disabled.ember-view")))
            txt_already_connected = "Already Sent Connection Request"
            print(txt_already_connected)
            count_candidate_already_added += 1
            driver.switch_to.window(driver.window_handles[0])
            return txt_already_connected
        except Exception as e:
            error_log.exception(e)

        connection_button = WebDriverWait(driver, 5).until(EC.presence_of_element_located((By.CSS_SELECTOR,
                                                                    'button.pvs-profile-actions__action.artdeco-button.artdeco-button--2')))
        # except:
            # message_button = WebDriverWait(driver, 5).until(EC.presence_of_element_located((By.CSS_SELECTOR,
            #                                                                                 "button.pvs-profile-actions__action.artdeco-button.artdeco-button--secondary.artdeco-button--muted.artdeco-button")))

        connect_or_follow = connection_button.text
        if connect_or_follow == 'Connect':
            try:
                connection_button.click()
            except Exception as e:
                error_log.exception(e)
        else:
            # connecting follow account

            # click to more button
            try:
                btn_more = f"document.getElementsByClassName('artdeco-dropdown__trigger artdeco-dropdown__trigger--placement-bottom ember-view pvs-profile-actions__action')[0].click();"
                driver.execute_script(btn_more)
                time.sleep(1.5)
            except Exception as e:
                error_log.exception(e)

            # click to connect button
            try:
                btn_connect = f"document.getElementsByClassName('pvs-profile-actions__action display-flex align-items-center')[2].click();"
                driver.execute_script(btn_connect)
                time.sleep(1.5)
                # javaScript = f"document.getElementsByClassName('mr2 artdeco-button')[0].click();"
                driver.execute_script(f"document.getElementsByClassName('mr2 artdeco-button')[0].click();")
                time.sleep(1.5)
            except Exception as e:
                error_log.exception(e)
            print("This is a Follow account!")


        try:
            # click to add a note button
            WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.CSS_SELECTOR, "button.mr1.artdeco-button"))).click()
            type_message = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.CSS_SELECTOR, "textarea.ember-text-area")))

            # Write the note
            type_message.clear()
            type_message.send_keys(LINKEDIN_CREDENTIAL['Text'])

            # click to send button
            driver.find_element_by_css_selector('button.ml1.artdeco-button').click()
            count_total_candidate_request_send += 1
            time.sleep(1)

            # Back to the main window
            driver.switch_to.window(driver.window_handles[0])
            time.sleep(DELAY_SHORT)

        except Exception as e:
            error_log.exception(e)

    except Exception as e:
        error_log.exception(e)

def automate_linkedin_connection(driver):

    time.sleep(DELAY_LONG)
    driver.get(LINKEDIN_SEARCH_URL)

    # Search mutual connection by designation
    try:
        search = driver.find_element_by_css_selector('input.search-global-typeahead__input.always-show-placeholder')
        search.send_keys(LINKEDIN_CREDENTIAL['Designation'])
        search.send_keys(Keys.ENTER)
    except Exception as e:
        error_log.exception(e)
    time.sleep(DELAY_LONG)

    RUNNING_STATUS = True
    while RUNNING_STATUS:
        try:
            time.sleep(DELAY_SHORT)
            candidates_container = driver.find_elements_by_css_selector("li.reusable-search__result-container")
            for candidate in candidates_container:
                candidate_links = candidate.find_element_by_css_selector(".entity-result__title-line.flex-shrink-1 a").get_attribute('href')

                connect_to_profile(driver, candidate_links)
                time.sleep(DELAY_SHORT)

                scroll_to_element(driver, candidate)
            driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            try:
                WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.CSS_SELECTOR,
                                    "button.artdeco-pagination__button.artdeco-pagination__button--next.artdeco-button.artdeco-button--muted.artdeco-button--icon-right.artdeco-button--1.artdeco-button--tertiary.ember-view"))).click()
            except:
                print("No more page found!")
                RUNNING_STATUS = False
        except Exception as e:
            error_log.exception(e)








