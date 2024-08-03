# Scrapes and stores data for Richmond and Eureka. [[RAW HTML ONLY]].
import logging
import time
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup

# Setup logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def fetch_url(url):
    logging.info(f"Fetching URL: {url}")

    
    chrome_options = Options()
    chrome_options.add_argument("--headless")  
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

def scrape_richmond_projects():
    url = "https://www.ci.richmond.ca.us/1404/Major-Projects"
    html_content = fetch_url(url)
    soup = parse_html(html_content)
    return soup

def scrape_eureka_current_projects():
    url = "https://www.eurekaca.gov/744/Current-Projects"
    html_content = fetch_url(url)
    soup = parse_html(html_content)
    return soup

def scrape_eureka_completed_projects():
    url = "https://www.eurekaca.gov/305/Completed-Projects"
    html_content = fetch_url(url)
    soup = parse_html(html_content)
    return soup

if __name__ == '__main__':
    richmond_soup = scrape_richmond_projects()
    eureka_current_soup = scrape_eureka_current_projects()
    eureka_completed_soup = scrape_eureka_completed_projects()
    
    with open('data/richmond_raw_html.html', 'w', encoding='utf-8') as f:
        f.write(str(richmond_soup))
    with open('data/eureka_current_raw_html.html', 'w', encoding='utf-8') as f:
        f.write(str(eureka_current_soup))
    with open('data/eureka_completed_raw_html.html', 'w', encoding='utf-8') as f:
        f.write(str(eureka_completed_soup))
