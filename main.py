from get_names import get_names
from get_data import get_data
from get_yield import get_yield
from Shareholder_yield import shareholder_yield
from Spreadsheet import spreadsheet

file_name = input("Please insert the file name for your google service account: ")

get_names(file_name)
get_data(file_name)
get_yield(file_name)
shareholder_yield(file_name)
spreadsheet(file_name)
