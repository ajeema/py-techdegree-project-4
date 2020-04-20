import os

from playhouse.sqlite_ext import *
import pandas as pd

# Database file/configuration
DATABASE = 'inventory.db'
db = SqliteDatabase(DATABASE)

#Pandas dataframe
df = pd.read_sql("SELECT * FROM Product;", db)

# source product file
SOURCE = 'inventory.csv'


def clear():
	"""Clear the screen"""
	os.system('cls' if os.name == 'nt' else 'clear')












