import os
import csv
from datetime import datetime
from collections import OrderedDict

import openpyxl
import pandas as pd
from peewee import *

from settings import *
from welcome import *

db = SqliteDatabase('inventory.db')

class Product(Model):
    product_id = AutoField()
    date_updated = DateTimeField()
    product_name = TextField()
    product_quantity = IntegerField()
    product_price = IntegerField()

    class Meta:
        database = db

def initialize():
    """create table and db"""
    db.connect()
    # print("Just connected to DB")
    db.create_tables([Product], safe=True)
    # print("just created tables")


def open_and_clean_csv():
    with open('inventory.csv', newline='') as csvfile:
        artreader = csv.DictReader(csvfile, delimiter=',')
        rows = list(artreader)
        for row in rows[:]:

            row['product_quantity'] = int(row['product_quantity'])
            row['product_price'] = (row['product_price'].strip('$')).replace('.', '')
            row['product_price'] = int(row['product_price'])
            row['date_updated'] = datetime.strptime(row['date_updated'], '%m/%d/%Y')

            if Product.select().where(Product.product_name.contains(row['product_name'])):
                for product in Product.select().where(Product.product_name.contains(row['product_name'])):
                    if product.date_updated < row['date_updated']:
                        product.date_updated = row['date_updated']
                        product.product_quantity = row['product_quantity']
                        product.product_price = row['product_price']
                        product.save()
                    #else:

            else:
                Product.create(product_name=row['product_name'],
                               date_updated=row['date_updated'],
                               product_quantity=row['product_quantity'],
                               product_price=row['product_price'])

def backup():
	"""backup db"""
	df = pd.read_sql("SELECT * FROM Product;", db)
	print("Which format would you like to export to?")
	print("""
[1] .json
[2] .csv
[3] .xlsx
[4] all formats
	""")
	export_type = input("___:")
	if export_type == '1':
		BACKUP_DB
		print("Backup saved")
	elif export_type == '2':
		BACKUP_CSV
		print("Backup saved")
	elif export_type == '3':
		writer = pd.ExcelWriter('backups/backup.xlsx')
		df.to_excel(writer, 'DataFrame')
		writer.save()
		print("Backups saved")
	# elif export_type == '4':
	# 	BACKUP_ALL
	# 	writer = pd.ExcelWriter('backups/backup.xlsx', index=False)
	# 	df.to_excel(writer, 'DataFrame')
	# 	writer.save()
	# 	print("Backups saved")

	else:
		print("You didn't enter a valid option")
	pass


def view_every_product():
	"""Display all products"""
	df = pd.read_sql("SELECT * FROM Product;", db)

	print(df.columns())


def add_product():
	"""add a product"""
	pass


def search_product():
	"""Search for a product (i.e 1)"""
	pass


def menu_loop():
	"""show the menu"""
	choice = None

	while choice != 'q':
		print("Enter 'q' to quit.")
		for key, value in menu.items():
			print('{}) {}'.format(key, value.__doc__))
		choice = input('Action: ').lower().strip()

		if choice in menu:
			menu[choice]()


menu = OrderedDict([
		('a', add_product),
		('b', backup),
		('e', view_every_product),
		('v', search_product),
])

if __name__ == '__main__':
	loading()
	os.system('cls' if os.name == 'nt' else 'clear')
	welcome()
	initialize()
	open_and_clean_csv()
	menu_loop()

# backup()
