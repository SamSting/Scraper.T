
# Final code. Scrapes and Stores data from all 5 urls as given in the Assignment pdf.

import logging
import time
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
import pandas as pd
import uuid
from bs4 import BeautifulSoup
import csv

# Setup logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def fetch_url(url):
    logging.info(f"Fetching URL: {url}")

    # Set up Chrome options
    chrome_options = Options()
    chrome_options.add_argument("--headless") 
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")


    service = Service(r'D:\chromedriver-win64\chromedriver.exe')  

    driver = webdriver.Chrome(service=service, options=chrome_options)

    driver.get(url)


    time.sleep(10)  # Adjust the sleep time if necessary
    html_content = driver.page_source
    driver.quit()
    return html_content

def fetch_caleprocure_data():
    url = 'https://caleprocure.ca.gov/pages/Events-BS3/event-search.aspx'

    # Set up Chrome options
    options = Options()
    options.headless = True  
    service = Service(executable_path='D:\chromedriver-win64\chromedriver.exe')  

    # Initialize the WebDriver
    driver = webdriver.Chrome(service=service, options=options)

    # Open the webpage
    driver.get(url)

    # Wait for the dynamic content to load
    time.sleep(10)  
    
    # Find all rows in the table
    rows = driver.find_elements(By.XPATH, "//tr[contains(@data-if-container-label, 'tbl')]")
    
    caleprocure_projects = []
    
    # Loop through each row and extract data
    for row in rows:
        try:
            event_id_element = row.find_element(By.XPATH, ".//td[@data-if-label='tdEventId']")
            event_name_element = row.find_element(By.XPATH, ".//td[@data-if-label='tdEventName']")
            dep_name_element = row.find_element(By.XPATH, ".//td[@data-if-label='tdDepName']")
            end_date_element = row.find_element(By.XPATH, ".//td[@data-if-label='tdEndDate']")
            status_element = row.find_element(By.XPATH, ".//td[@data-if-label='tdStatus']")
            
            event_id = event_id_element.text.strip()
            event_name = event_name_element.text.strip()
            dep_name = dep_name_element.text.strip()
            end_date = end_date_element.text.strip()
            status = status_element.text.strip()
            
            if event_id and event_name and dep_name and end_date and status:
                # Store the extracted data in a dictionary
                project = {
                    'Event ID': event_id,
                    'Event Name': event_name,
                    'Department Name': dep_name,
                    'End Date': end_date,
                    'Status': status
                }
                caleprocure_projects.append(project)
        except Exception as e:
            logging.error(f"Error parsing row data: {e}")
    
    # Close the WebDriver
    driver.quit()
    
    # Save the data to a CSV file
    with open('./data/caleprocure.csv', mode='w', newline='') as file:
        writer = csv.DictWriter(file, fieldnames=['Event ID', 'Event Name', 'Department Name', 'End Date', 'Status'])
        writer.writeheader()
        writer.writerows(caleprocure_projects)
    
    logging.info("Data has been successfully written to caleprocure.csv")

def extract_richmond_data(html_content):
    logging.info("Extracting data from Richmond HTML")
    soup = BeautifulSoup(html_content, 'html.parser')
    
    projects = []
    
    # Find all subheadings and their corresponding project lists
    subheads = soup.find_all('h3', class_='subhead2')
    
    for subhead in subheads:
       
        project_list = subhead.find_next_sibling('ul')
        
        if (project_list):
            for item in project_list.find_all('li'):
                try:
                    
                    project_link = item.find('a')
                    if project_link:
                        project_name = project_link.get_text(strip=True)
                        project_url = project_link['href']
                        
                        project = {
                            'original_id': None,
                            'aug_id': str(uuid.uuid4()),
                            'country_name': 'United States',
                            'country_code': 'USA',
                            'region_name': 'California',
                            'region_code': 'CA',
                            'latitude': None,
                            'longitude': None,
                            'url': project_url,
                            'title': project_name,
                            'description': None,
                            'status': None,
                            'timestamp': None,
                            'timestamp_label': None,
                            'budget': None,
                            'budget_label': None,
                            'currency': None,
                            'sector': None,
                            'subsector': None,
                            'document_urls': None,
                        }
                        
                        projects.append(project)
                        logging.info(f"Scraped project: {project_name}, URL: {project_url}")
                except Exception as e:
                    logging.error(f"Error parsing project data: {e}")

    return projects

def extract_eureka_current_data(html_content):
    logging.info("Extracting data from Eureka Current Projects HTML")
    soup = BeautifulSoup(html_content, 'html.parser')
    
    projects = []
    
    # Find all tabs
    tabs = soup.find_all('div', class_='tabbedWidget cpTabPanel')
    
    for tab in tabs:
        try:
           
            project_name = tab.find('h2').get_text(strip=True)
            project_description = tab.find('div', class_='fr-view').get_text(strip=True)
            project_link_tag = tab.find('a', href=True)
            project_url = project_link_tag['href'] if project_link_tag else None
            
            project = {
                'original_id': None,
                'aug_id': str(uuid.uuid4()),
                'country_name': 'United States',
                'country_code': 'USA',
                'region_name': 'California',
                'region_code': 'CA',
                'latitude': None,
                'longitude': None,
                'url': project_url,
                'title': project_name,
                'description': project_description,
                'status': None,
                'timestamp': None,
                'timestamp_label': None,
                'budget': None,
                'budget_label': None,
                'currency': None,
                'sector': None,
                'subsector': None,
                'document_urls': None,
            }
            
            projects.append(project)
            logging.info(f"Scraped project: {project_name}, URL: {project_url}")
        except Exception as e:
            logging.error(f"Error parsing project data: {e}")

    return projects

def extract_eureka_completed_data(html_content):
    logging.info("Extracting data from Eureka Completed Projects HTML")
    soup = BeautifulSoup(html_content, 'html.parser')
    
    projects = []
    
   
    tabs = soup.find_all('div', class_='tabbedWidget cpTabPanel')
    
    for tab in tabs:
        try:
            
            project_name = tab.find('h2').get_text(strip=True)
            project_description = tab.find('div', class_='fr-view').get_text(strip=True)
            project_link_tag = tab.find('a', href=True)
            project_url = project_link_tag['href'] if project_link_tag else None
            
            project = {
                'original_id': None,
                'aug_id': str(uuid.uuid4()),
                'country_name': 'United States',
                'country_code': 'USA',
                'region_name': 'California',
                'region_code': 'CA',
                'latitude': None,
                'longitude': None,
                'url': project_url,
                'title': project_name,
                'description': project_description,
                'status': None,
                'timestamp': None,
                'timestamp_label': None,
                'budget': None,
                'budget_label': None,
                'currency': None,
                'sector': None,
                'subsector': None,
                'document_urls': None,
            }
            
            projects.append(project)
            logging.info(f"Scraped project: {project_name}, URL: {project_url}")
        except Exception as e:
            logging.error(f"Error parsing project data: {e}")

    return projects

def save_to_csv(data, filename):
    logging.info(f"Saving data to {filename}")
    # Ensure data is a list of tuples or dictionaries
    if data and isinstance(data[0], tuple):
        # For a list of tuples, assume headers are known
        headers = ['Title', 'Link Text', 'URL']
        with open(filename, mode='w', newline='', encoding='utf-8') as file:
            writer = csv.writer(file)
            writer.writerow(headers)  # Write the header
            writer.writerows(data)    # Write the data rows
    elif data and isinstance(data[0], dict):
        # For a list of dictionaries, use pandas for convenience
        df = pd.DataFrame(data)
        df.to_csv(filename, index=False)
    else:
        logging.error("Data format is unsupported for CSV writing.")


def scrape_esri_sections():
    url = "https://www.esri.com/en-us/industries/index"
    html_content = fetch_url(url)
    soup = BeautifulSoup(html_content, 'html.parser')

    # Print out the first part of the HTML to understand its structure
    print(soup.prettify()[:2000])  

    # Find all relevant sections
    sections = soup.find_all('div', class_='contentarea esri-text-container')
    
    # Extract the links and their texts from all sections
    data = []
    for section in sections:
        
        print(section.prettify()[:500])  

        try:
            # Find the title based on current structure
            title_tag = section.find('h3', class_='esri-text__title')  
            title = title_tag.get_text(strip=True) if title_tag else 'No Title'
            
            links = section.find_all('a', href=True)
            for link in links:
                link_text = link.get_text(strip=True)
                link_href = "https://www.esri.com" + link['href']  
                data.append((title, link_text, link_href))
        
        except Exception as e:
            logging.error(f"Error extracting data from section: {e}")
    
    return data



if __name__ == '__main__':
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

    logging.info("Scraping and data extraction complete.")