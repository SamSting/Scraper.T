#Scrapes and stores data [[BOTH RAW HTML AND DATA CSV]]
 #Include scripts to add more.

import os
import subprocess
import logging

# Setup logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def run_script(script_name):
    try:
        logging.info(f"Running script: {script_name}")
        subprocess.run(['python', script_name], check=True)
    except subprocess.CalledProcessError as e:
        logging.error(f"Error occurred while running {script_name}: {e}")

if __name__ == '__main__':
    scripts = [
        'src/scraper.py',
        'src/data_standardization.py',
        'src/continuous_update.py'
    ]
    
    for script in scripts:
        run_script(script)
