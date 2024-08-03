
#run scraper.py for change in effect. Used for Richmond Major Projects, Eurekaca Current and Completed Projects. Used to serialize the data in the assignment format.

import logging
import pandas as pd
import uuid
from bs4 import BeautifulSoup

# Setup logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def extract_richmond_data(soup):
    logging.info("Extracting data from Richmond HTML")
    
    projects = []
    
    # Find all subheadings and their corresponding project lists
    subheads = soup.find_all('h3', class_='subhead2')
    
    for subhead in subheads:
        # Get the corresponding list of projects under each subheading
        project_list = subhead.find_next_sibling('ul')
        
        if project_list:
            for item in project_list.find_all('li'):
                try:
                    # Extract project name and link
                    project_link = item.find('a')
                    if project_link:
                        project_name = project_link.get_text(strip=True)
                        project_url = project_link['href']
                        
                        project = {
                            'original_id': None,  # Assuming there's no unique ID in the source
                            'aug_id': str(uuid.uuid4()),
                            'country_name': 'United States',
                            'country_code': 'USA',
                            'region_name': 'California',
                            'region_code': 'CA',
                            'latitude': None,  # Geocoding required
                            'longitude': None,  # Geocoding required
                            'url': project_url,
                            'title': project_name,
                            'description': None,  # Additional scraping needed
                            'status': None,  # Additional scraping needed
                            'timestamp': None,  # Additional scraping needed
                            'timestamp_label': None,  # Additional scraping needed
                            'budget': None,  # Additional scraping needed
                            'budget_label': None,  # Additional scraping needed
                            'currency': None,  # Additional scraping needed
                            'sector': None,  # Additional scraping needed
                            'subsector': None,  # Additional scraping needed
                            'document_urls': None,  # Additional scraping needed
                        }
                        
                        projects.append(project)
                        logging.info(f"Scraped project: {project_name}, URL: {project_url}")
                except Exception as e:
                    logging.error(f"Error parsing project data: {e}")

    return projects

def extract_eureka_current_data(soup):
    logging.info("Extracting data from Eureka Current Projects HTML")
    
    projects = []
    
    # Find all tabs
    tabs = soup.find_all('div', class_='tabbedWidget cpTabPanel')
    
    for tab in tabs:
        try:
            # Extract project name and description
            project_name = tab.find('h2').get_text(strip=True)
            project_description = tab.find('div', class_='fr-view').get_text(strip=True)
            project_link_tag = tab.find('a', href=True)
            project_url = project_link_tag['href'] if project_link_tag else None
            
            project = {
                'original_id': None,  # Assuming there's no unique ID in the source
                'aug_id': str(uuid.uuid4()),
                'country_name': 'United States',
                'country_code': 'USA',
                'region_name': 'California',
                'region_code': 'CA',
                'latitude': None,  # Geocoding required
                'longitude': None,  # Geocoding required
                'url': project_url,
                'title': project_name,
                'description': project_description,
                'status': None,  # Additional scraping needed
                'timestamp': None,  # Additional scraping needed
                'timestamp_label': None,  # Additional scraping needed
                'budget': None,  # Additional scraping needed
                'budget_label': None,  # Additional scraping needed
                'currency': None,  # Additional scraping needed
                'sector': None,  # Additional scraping needed
                'subsector': None,  # Additional scraping needed
                'document_urls': None,  # Additional scraping needed
            }
            
            projects.append(project)
            logging.info(f"Scraped project: {project_name}, URL: {project_url}")
        except Exception as e:
            logging.error(f"Error parsing project data: {e}")

    return projects

def extract_eureka_completed_data(soup):
    logging.info("Extracting data from Eureka Completed Projects HTML")
    
    projects = []
    
    # Find all tabs
    tabs = soup.find_all('div', class_='tabbedWidget cpTabPanel')
    
    for tab in tabs:
        try:
            # Extract project name and description
            project_name = tab.find('h2').get_text(strip=True)
            project_description = tab.find('div', class_='fr-view').get_text(strip=True)
            project_link_tag = tab.find('a', href=True)
            project_url = project_link_tag['href'] if project_link_tag else None
            
            project = {
                'original_id': None,  # Assuming there's no unique ID in the source
                'aug_id': str(uuid.uuid4()),
                'country_name': 'United States',
                'country_code': 'USA',
                'region_name': 'California',
                'region_code': 'CA',
                'latitude': None,  # Geocoding required
                'longitude': None,  # Geocoding required
                'url': project_url,
                'title': project_name,
                'description': project_description,
                'status': None,  # Additional scraping needed
                'timestamp': None,  # Additional scraping needed
                'timestamp_label': None,  # Additional scraping needed
                'budget': None,  # Additional scraping needed
                'budget_label': None,  # Additional scraping needed
                'currency': None,  # Additional scraping needed
                'sector': None,  # Additional scraping needed
                'subsector': None,  # Additional scraping needed
                'document_urls': None,  # Additional scraping needed
            }
            
            projects.append(project)
            logging.info(f"Scraped project: {project_name}, URL: {project_url}")
        except Exception as e:
            logging.error(f"Error parsing project data: {e}")

    return projects

def save_to_csv(data, filename):
    logging.info(f"Saving data to {filename}")
    df = pd.DataFrame(data)
    df.to_csv(filename, index=False)

if __name__ == '__main__':
    # For testing, read the raw HTML from files
    with open('data/richmond_raw_html.html', 'r', encoding='utf-8') as f:
        richmond_html_content = f.read()
        
    with open('data/eureka_current_raw_html.html', 'r', encoding='utf-8') as f:
        eureka_current_html_content = f.read()
    
    with open('data/eureka_completed_raw_html.html', 'r', encoding='utf-8') as f:
        eureka_completed_html_content = f.read()
    
    richmond_soup = BeautifulSoup(richmond_html_content, 'html.parser')
    eureka_current_soup = BeautifulSoup(eureka_current_html_content, 'html.parser')
    eureka_completed_soup = BeautifulSoup(eureka_completed_html_content, 'html.parser')
    
    richmond_projects = extract_richmond_data(richmond_soup)
    eureka_current_projects = extract_eureka_current_data(eureka_current_soup)
    eureka_completed_projects = extract_eureka_completed_data(eureka_completed_soup)
    
    if richmond_projects:
        save_to_csv(richmond_projects, './data/richmond_projects.csv')
    else:
        logging.warning("No Richmond data to save")
        
    if eureka_current_projects:
        save_to_csv(eureka_current_projects, './data/eureka_current_projects.csv')
    else:
        logging.warning("No Eureka Current Projects data to save")
        
    if eureka_completed_projects:
        save_to_csv(eureka_completed_projects, './data/eureka_completed_projects.csv')
    else:
        logging.warning("No Eureka Completed Projects data to save")
