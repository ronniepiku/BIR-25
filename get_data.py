import os
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import gspread
import time


def get_data(file_name, sh_name):
    os.environ['PATH'] += r"C:SeleniumDrivers"
    chrome_options = webdriver.ChromeOptions()
    # chrome_options.add_argument('--headless')
    driver = webdriver.Chrome(options=chrome_options)
    wait = WebDriverWait(driver, 10)

    # Navigate to the login page
    driver.get("https://www.stockopedia.com/auth/login/")

    # Enter credentials and log in
    username = input("Please enter your username: ")
    email_field = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "#email")))
    email_field.clear()
    email_field.send_keys(username)

    password = input("Please enter your password: ")
    password_field = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "#password")))
    password_field.clear()
    password_field.send_keys(password)

    login_button2 = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, "#auth_submit")))
    login_button2.click()

    # Wait for the homepage to load
    wait.until(EC.url_contains("home"))

    # Open the Investmentbot2023 sheet
    gc = gspread.service_account(filename=file_name)
    sh = gc.open(sh_name)

    # Search for each ticker symbol
    tickers = sh.sheet1.col_values(2)[1:]
    for i, ticker in enumerate(tickers):
        try:
            # Construct the URL for the ticker symbol
            print(ticker)
            ticker_url = f"https://www.stockopedia.com/share-prices/LON:{ticker}"
            # Navigate to the ticker symbol's page
            driver.get(ticker_url)
            wait.until(EC.presence_of_element_located((By.XPATH, "//span[contains(@class, 'ng-star-inserted')]")))

            elements_values = driver.find_elements(By.XPATH,
                                   "//div[@class='gr__col gr__col--shrink space-in-l-2']//span[@class='ng-star-inserted']")
            elements_momentum = driver.find_elements(By.XPATH,
                                    "//td[@class='align-r ng-star-inserted']//span[@class='ng-star-inserted']//span")

            # Gets values by indexing elements and converting html to text
            if elements_values[8].text == 'n/a':
                ebitda_ev = 'n/a'
            else:
                ebitda_ev = 1 / float(elements_values[8].text.replace(',', ''))

            price_to_book_value = elements_values[4].text
            print(price_to_book_value)
            price_to_earnings = elements_values[0].text
            price_to_sales = elements_values[7].text
            price_to_cashflow = elements_values[6].text
            momentum = elements_momentum[2].text

            # Update worksheet with data
            sh.sheet1.update_cell(i + 2, 3, price_to_book_value)
            sh.sheet1.update_cell(i + 2, 5, price_to_earnings)
            sh.sheet1.update_cell(i + 2, 7, price_to_sales)
            sh.sheet1.update_cell(i + 2, 11, price_to_cashflow)
            sh.sheet1.update_cell(i + 2, 9, ebitda_ev)
            sh.sheet1.update_cell(i + 2, 19, momentum)
            time.sleep(1.5)

        except Exception as e:
            print(f"Error searching for ticker symbol {e}")
            continue
