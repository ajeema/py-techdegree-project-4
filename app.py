import csv
from datetime import datetime

from playhouse.dataset import DataSet
from settings import *
from peewee import *


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


def open_csv():
	with open(SOURCE, newline='') as csvfile:
		dialect = csv.Sniffer().sniff(csvfile.read())
		csvfile.seek(0)
		reader = csv.reader(csvfile, dialect)
		return [product for product in reader]

		rows = list(reader)
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
			else:
				Product.create(product_name=row['product_name'],
					date_updated=row['date_updated'],
					product_quantity=row['product_quantity'],
					product_price=row['product_price'])

def backup():
	print("Which format would you like to export to?")
	print("""
[1] .json
[2] .db
[3] .csv
	""")
	export_type = input("___:")
	if export_type == '1':
		db.freeze(product.all(), format='json', filename='backup.json')
	elif export_type == '2':
		print("some action")
	elif export_type == '3':
		print("some action")
	else:
		print("You didn't enter a valid option")


def view_every_product():
	"""Display all products"""
	pass


if __name__ == '__main__':
	initialize()
	open_csv()
	backup()
