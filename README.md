# BIR-25
This bot uses selenium to scrape accounting data from stockopedia and fidelity to pick a selection of 25 undervalued stocks.

# Method
A list of companies and their corresponding tickers are scrapped from the hargreves lansdown website and written into a google sheet file.
Then, bot navigates to the stockopedia website and extracts key accounting values for each stock (You will need a stockopedia subscription for this step). This is then written into the google sheets file.
Next we collect data for dividends yield and buyback yeild from the fidelity website. Bot will search each company through google and use selenium to navigate to the appropriate page which contains this data.It will then be written into the google sheet. Shareholder yeild is then found by adding the two yeilds together.
Now each stock is ready to be assigned a rank from 1 to 100 for each accounting value. If the stock has a value of n/a it will be assigned a rank of 50.
Ranks will then be added up to give a total rank across all factors.
Then the top decile by rank is considered and sorted in order or greatest 6-month price momentum. The bot then creates a .txt file which shows the top 35 most undervalued stocks from the inital list. user only needs to purchase 25 for the stratagy to work but 35 are included just incase user is unable to buy any of the first 25 for any reason.
