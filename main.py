from get_names import get_names
from get_data import get_data
from get_yield import get_yield
from Shareholder_yield import shareholder_yield
from Spreadsheet import spreadsheet

file_name = input("Please insert the file name for your google service account: ")
sh_name = input('Please enter the name of the gsheets file you want to save data too: ')

get_names(file_name, sh_name)
get_data(file_name, sh_name)
get_yield(file_name, sh_name)
shareholder_yield(file_name, sh_name)
spreadsheet(file_name, sh_name)