#Currently has an interval of 1 min for testing. Can be scheduled as needed.

import schedule
import time
import logging

# Your scraping functions should be imported or defined here
from final2 import fetch_caleprocure_data, extract_richmond_data, extract_eureka_current_data, extract_eureka_completed_data, scrape_esri_sections, fetch_url, save_to_csv

# Setup logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def job():
    logging.info("Starting scheduled scraping tasks...")
    
    # Fetch and save CaleProcure data
    fetch_caleprocure_data()

    # Fetch Richmond data
    richmond_url = 'https://www.ci.richmond.ca.us/1404/Major-Projects'
    richmond_html_content = fetch_url(richmond_url)
    richmond_projects = extract_richmond_data(richmond_html_content)
    if richmond_projects:
        save_to_csv(richmond_projects, './data/richmond_projects.csv')
    else:
        logging.warning("No Richmond data to save")

    # Fetch Eureka Current Projects data
    eureka_current_url = 'https://www.eurekaca.gov/744/Current-Projects'
    eureka_current_html_content = fetch_url(eureka_current_url)
    eureka_current_projects = extract_eureka_current_data(eureka_current_html_content)
    if eureka_current_projects:
        save_to_csv(eureka_current_projects, './data/eureka_current_projects.csv')
    else:
        logging.warning("No Eureka Current Projects data to save")

    # Fetch Eureka Completed Projects data
    eureka_completed_url = 'https://www.eurekaca.gov/305/Completed-Projects'
    eureka_completed_html_content = fetch_url(eureka_completed_url)
    eureka_completed_projects = extract_eureka_completed_data(eureka_completed_html_content)
    if eureka_completed_projects:
        save_to_csv(eureka_completed_projects, './data/eureka_completed_projects.csv')
    else:
        logging.warning("No Eureka Completed Projects data to save")

    # Scrape ESRI sections
    esri_data = scrape_esri_sections()
    if esri_data:
        save_to_csv(esri_data, './data/esri_links.csv')
    else:
        logging.warning("No ESRI data to save")

    logging.info("Scheduled scraping tasks completed.")

# Schedule the job every minute for testing
schedule.every().minute.do(job)

while True:
    schedule.run_pending()
    time.sleep(60)  # Wait a minute before checking again
