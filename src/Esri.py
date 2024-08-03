
# https://www.esri.com/en-us/industries/index --Scraping Script for ESRI.

import logging
import time
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup
import csv

# Setup logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def fetch_url(url):
    logging.info(f"Fetching URL: {url}")

    # Set up Chrome options
    chrome_options = Options()
    chrome_options.add_argument("--headless")  # Run headless if you don't need a GUI
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")

    
    service = Service(r'D:\chromedriver-win64\chromedriver.exe') 

    driver = webdriver.Chrome(service=service, options=chrome_options)
    
    driver.get(url)
    
    
    time.sleep(5)  
    html_content = driver.page_source
    driver.quit()
    return html_content

def parse_html(html_content):
    logging.info("Parsing HTML content")
    soup = BeautifulSoup(html_content, 'html.parser')
    return soup

def scrape_esri_sections():
    url = "https://www.esri.com/en-us/industries/index"
    html_content = fetch_url(url)
    soup = parse_html(html_content)
    
    
    sections = soup.find_all('div', class_='contentarea esri-text-container')
    
    
    data = []
    for section in sections:
        title = section.find('h3', class_='esri-text__title').get_text(strip=True)
        links = section.find_all('a')
        
        for link in links:
            link_text = link.get_text(strip=True)
            link_href = "https://www.esri.com" + link['href']  
            data.append((title, link_text, link_href))
    
    return data

def save_to_csv(data, filename):
    logging.info(f"Saving data to {filename}")
    with open(filename, mode='w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        writer.writerow(['Title', 'Link Text', 'URL'])
        writer.writerows(data)

if __name__ == '__main__':
    esri_data = scrape_esri_sections()
    if esri_data:
        save_to_csv(esri_data, './data/esri_links.csv')
    else:
        logging.warning("No data to save")

    print("Data has been successfully written to esri_links.csv")