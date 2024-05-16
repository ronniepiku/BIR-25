import gspread
import os

from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC



def get_names(file_name, sh_name):
    # initialize global variables
    page = 1
    stocks = set()

    os.environ['PATH'] += r"C:SeleniumDrivers"
    chrome_options = webdriver.ChromeOptions()
    # chrome_options.add_argument('--headless')
    driver = webdriver.Chrome(options=chrome_options)

    # while loop runs through each page by changing url accordingly
    while page < 10:
        url = f"https://www.hl.co.uk/shares/stock-market-summary/ftse-all-share?page={page}"
        driver.get(url)

        # Accept cookies by clicking the button
        if page == 1:
            try:
                cookies_button = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.CLASS_NAME, 'button-module_button-primary')))
                cookies_button.click()
            except Exception as e:
                print("Failed to click cookies button:", e)

        # Wait for the page to load
        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CLASS_NAME, 'stockTable')))

        # Extract the page source
        html_text = driver.page_source

        # Continue with BeautifulSoup and data extraction
        soup = BeautifulSoup(html_text, 'lxml')

        # find all rows in the table
        rows = soup.select('.stockTable tr')

        # iterate over each row and extract ticker and name
        for row in rows:
            # find the ticker element within the row
            ticker_elem = row.select_one('td:first-of-type')
            if ticker_elem:
                ticker = ticker_elem.text.strip()
                # find the company name element within the row
                name_elem = row.select_one('.name-col a')
                if name_elem:
                    name = name_elem.text.strip()

                    # add ticker and name to sets
                    stocks.add((name, ticker))

        page += 1
    
    # convert set to list
    stocks = list(stocks)

    # Close the WebDriver
    driver.quit()

    # Interacts with service account with communicates with sheets
    gc = gspread.service_account(filename=file_name)

    # Opens sheet
    sh = gc.open(sh_name)

    # Create the list of updates for the batch update
    updates = [{'range': f'A{i+2}:B{i+2}',
                'values': [[stocks[i][0], stocks[i][1]]]} for i in range(len(stocks))]

    # Batch update the cells
    sh.sheet1.batch_update(updates)
