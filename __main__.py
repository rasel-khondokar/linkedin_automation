import os
from datetime import datetime
from pyvirtualdisplay import Display
from app_configs.config_linkedin import dir_linkedin_error, LINKEDIN_MAIN_SITE, LINKEDIN_CREDENTIAL, \
    LINKEDIN_APP_NAME, DIRNAME_LINKEDIN_BLOCKING, VIRTUAL_DISPLAY
from functions import make_dir_if_not_exists
from scraping.Linkedin.common import LinkedinScraper
from scraping.Linkedin.linkedin_connect_candidate import automate_linkedin_connection, connect_to_profile
from settings import TIME_ZONE, DIRNAME_REPORT


def main():

    today = datetime.now().astimezone(TIME_ZONE).strftime('%Y-%m-%d')
    make_dir_if_not_exists(dir_linkedin_error)
    scheduler_log_path = f'{DIRNAME_REPORT}/{today}'
    make_dir_if_not_exists(scheduler_log_path)

    # Login to linkedin
    linkedin_scraper = LinkedinScraper()
    linkedin_driver = linkedin_scraper.login(LINKEDIN_MAIN_SITE, LINKEDIN_CREDENTIAL, dir_linkedin_error)

    start_linkedin_auto = datetime.now().astimezone(TIME_ZONE).strftime('%Y-%m-%d %H:%M:%S')
    # Verification_id:home_children_button
    print(f'{start_linkedin_auto} : {LINKEDIN_APP_NAME} candidate connecting started!')
    try:
        # Scrape from linkedin company
        automate_linkedin_connection(linkedin_driver)
    except Exception as e:
        print(e)
    # End the scraping
    end_linkedin_jobs = datetime.now().astimezone(TIME_ZONE).strftime('%Y-%m-%d %H:%M:%S')
    print(f'{end_linkedin_jobs} :  {LINKEDIN_APP_NAME} candidate connecting ended!')
    print('_______________________________________________________________________________')

    # Quit the driver
    linkedin_driver.quit()

if __name__ == "__main__":
    if VIRTUAL_DISPLAY:
        with Display(visible=True, size=(1600, 900)):
            main()
    else:
        main()