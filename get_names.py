from bs4 import BeautifulSoup
import requests
import re
import gspread


def get_names(file_name):
    # initialize global variables
    page = 1
    company_names = []
    tickers = []

    # while loop runs through each page by changing url accordingly
    while page != 7:
        url = f"https://www.hl.co.uk/shares/stock-market-summary/ftse-all-share?page={page}"

        # html for each page
        html_text = requests.get(url).text
        soup = BeautifulSoup(html_text, 'lxml')

        # define the regular expression pattern to match the company names and ticker since they change throughout
        pattern_name = re.compile(r"link-headline\s*\{Sedol:'\S*'}\sshareData")
        pattern_ticker = '[id^="ls-row-"][id$="-L"] > td:nth-child(1)'

        # find all the company names using the regular expression pattern
        for a_tag in soup.find_all('a', {'class': pattern_name}):
            company_names.append(a_tag.text.strip())

        tickers += [ticker.get_text().strip() for ticker in soup.select(pattern_ticker)]

        page += 1

    # Interacts with service account with communicates with sheets
    gc = gspread.service_account(filename=file_name)

    # Opens sheet
    sh = gc.open("Investmentbot2023")

    # Create the list of updates for the batch update
    updates = [{'range': f'A{i+2}:B{i+2}',
                'values': [[company_names[i], tickers[i]]]} for i in range(len(company_names))]

    # Batch update the cells
    sh.sheet1.batch_update(updates)
