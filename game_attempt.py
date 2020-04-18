import os
import csv
from datetime import datetime
from collections import OrderedDict

import pandas as pd
from peewee import *

from settings import *
from welcome import *


def open_csv():
	products = []
	with open('inventory.csv') as csvfile:
		reader = csv.DictReader(csvfile)
		rows = list(reader)
		for row in rows:
			products.append({
					'product_name': row['product_name'],
					'product_price': (row['product_price'].strip('$')).replace('.', ''),
					'product_quantity': int(row['product_quantity']),
					'date_updated': datetime.strptime(row['date_updated'], '%m/%d/%Y'),
			})
		if len(Product.select()) == 0:
			for product in products:
				Product.create(**product)
	return products


class Product(Model):
	product_id = AutoField()
	date_updated = DateTimeField()
	product_name = TextField()
	product_quantity = IntegerField()
	product_price = IntegerField()

	class Meta:
		database = db


# Database initialization and closing
def initialize():
	"""create table and db"""
	db.connect()
	db.create_tables([Product], safe = True)


def close_db():
	"""close database connection"""
	db.close()


def backup():
	"""backup db"""
	df = pd.read_sql_query("SELECT * FROM Product;", db)
	print("Which format would you like to export to?")
	print("""
[1] .json
[2] .csv
	""")
	export_type = input("___:")
	if export_type == '1':
		df.to_json('backups/backup.json', index = True)
	elif export_type == '2':
		df.to_csv('backups/backup.csv', index = True)
	else:
		print("You didn't enter a valid option")
	pass


def view_every_product():
	"""Display all products"""
	pass

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
	open_csv()
	menu_loop()
	#backup()
