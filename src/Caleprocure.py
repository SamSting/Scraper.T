
# Scraping Script for Caleprocure.

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
import csv
import time

# Set up Chrome options
options = Options()
options.headless = True  # Run in headless mode (no browser window)
service = Service(executable_path='path/to/chromedriver')  # Update this path

# Initialize the WebDriver
driver = webdriver.Chrome(service=service, options=options)

# Define the URL
url = 'https://caleprocure.ca.gov/pages/Events-BS3/event-search.aspx'

# Open the webpage
driver.get(url)

# Wait for the dynamic content to load
time.sleep(10)  # Adjust this as necessary based on your network speed

# Find all rows in the table
rows = driver.find_elements(By.XPATH, "//tr[contains(@data-if-container-label, 'tbl')]")

# Open a CSV file to write the data
with open('./data/caleprocure.csv', mode='w', newline='') as file:
    writer = csv.writer(file)
    
    # Write the header row
    writer.writerow(['Event ID', 'Event Name', 'Department Name', 'End Date', 'Status'])
    
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
                # Write the extracted data to the CSV file
                writer.writerow([event_id, event_name, dep_name, end_date, status])
        except:
            continue

# Close the WebDriver
driver.quit()

print("Data has been successfully written to caleprocure.csv")
