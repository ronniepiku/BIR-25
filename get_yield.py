import os
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import gspread
import time


def get_yield(file_name, sh_name):
    gc = gspread.service_account(filename=file_name)
    sh = gc.open(sh_name)
    company_names = sh.sheet1.col_values(1)[1:]
    tickers = sh.sheet1.col_values(2)[1:]

    os.environ['PATH'] += r";C:\SeleniumDrivers"
    driver = webdriver.Chrome()
    wait = WebDriverWait(driver, 10)

    driver.get("https://www.google.co.uk/")
    wait.until(EC.element_to_be_clickable((By.ID, "L2AGLb")))  # Wait for the element to be clickable
    driver.find_element(By.ID, "L2AGLb").click()

    # Google search for company and select first result
    for i, company_name in enumerate(company_names):
        e = company_name.replace(' ', '+').replace('&', '%26')
        search_terms = ['"buyback"', '"yield"', '"fidelity"', f'{e}', tickers[i]]
        search_terms_str = '+'.join(search_terms)
        search_url = f'https://www.google.co.uk/search?q={search_terms_str}'
        driver.get(search_url)
        time.sleep(1)

        search_result_link = driver.find_elements(By.CLASS_NAME, "LC20lb.MBeuO.DKV0Md")

        # Click on links that will contain data
        dividend_yield_val = "n/a"
        buyback_yield_val = "n/a"

        for link in search_result_link:
            if "Share Dividends" in link.text:
                link.click()
                try:
                    cookies_button = driver.find_element(By.ID, "ensCloseBanner")
                    cookies_button.click()
                except:
                    pass

                dividend_yield = driver.find_elements(By.CSS_SELECTOR,
                                                      "#yield-table > tbody > tr:nth-child(1) > td:nth-child(2)")
                buyback_yield = driver.find_elements(By.CSS_SELECTOR,
                                                     "#yield-table > tbody > tr:nth-child(1) > td:nth-child(3)")

                if dividend_yield and dividend_yield[0].text != "-":
                    dividend_yield_val = float(dividend_yield[0].text)
                else:
                    dividend_yield_val = "n/a"

                if buyback_yield and buyback_yield[0].text != "-":
                    buyback_yield_val = float(buyback_yield[0].text)
                else:
                    buyback_yield_val = "n/a"

                print(dividend_yield_val)
                print(buyback_yield_val)
                break

        # Check if a captcha is displayed
        captcha_form = driver.find_elements(By.ID, "captcha-form")
        if captcha_form:
            wait = WebDriverWait(driver, 100)
            wait.until(EC.invisibility_of_element_located((By.ID, "captcha-form")))

        sh.sheet1.batch_update([
            {
                'range': f'M{i+2}',
                'values': [[dividend_yield_val, buyback_yield_val]]
            }
        ])
