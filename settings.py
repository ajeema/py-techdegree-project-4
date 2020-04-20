import os
from datetime import datetime

from playhouse.sqlite_ext import *
import pandas as pd



now = datetime.now()

# Database file/configuration
DATABASE = 'inventory.db'
db = SqliteDatabase(DATABASE)

# source product file
SOURCE = 'inventory.csv'

#Pandas dataframe




def clear():
	"""Clear the screen"""
	os.system('cls' if os.name == 'nt' else 'clear')












