
import csv
from datetime import datetime
from collections import OrderedDict

import pandas as pd
from peewee import *

from settings import *
from welcome import *

db = SqliteDatabase(DATABASE)

class Product(Model):
    product_id = AutoField()
    product_name = TextField()
    product_price = IntegerField()
    product_quantity = IntegerField()
    date_updated = DateTimeField()

    class Meta:
        database = db

def initialize():
    db.connect()
    db.create_tables([Product], safe=True)


def open_and_clean_csv():
    with open(SOURCE, newline='') as csvfile:
        inv_reader = csv.DictReader(csvfile, delimiter=',')
        rows = list(inv_reader)
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
                               product_price=row['product_price'],
                               product_quantity=row['product_quantity'],
                               date_updated=row['date_updated'])


def backup():
    """backup db"""
    print("Which format would you like to export to?")
    print("""
[1] .json
[2] .csv
[3] .xlsx
    """)
    export_type = input("___:")
    if export_type == '1':
        df.to_json('backups/backup.json', orient='records', lines=True)
        print(".json Backup saved")
    elif export_type == '2':
        df.to_csv('backups/backup.csv', sep='\t', index=False)
        print(".csv Backup saved")
    elif export_type == '3':
        writer = pd.ExcelWriter('backups/backup.xlsx')
        df.to_excel(writer, 'DataFrame', index=False)
        writer.save()
        print(".xlsx Backup saved")
    else:
        print("You didn't enter a valid option")


def view_every_product():
    """Display all products"""
    view_all = Product.select()

    print(view_all)

def add_product():
    """add a product"""
    input_name = str(input("Enter a name: "))
    input_qty = int(input("enter a quantity"))
    input_price = input("Enter a price")
    fields = [Product.product_name, Product.product_price, Product.product_quantity, Product.date_updated]
    data = [(input_name, input_price, input_qty, datetime.today()
                    )]

    Product.insert_many(data, fields=fields).execute()


def search_product():
    """Search for a product (i.e 1)"""
    clear()
    total_rows = Product.select().count()
    try:
        product_id = int(input(f'Input product id (hint: between 1 and {total_rows}:) '))
        # http://docs.peewee-orm.com/en/latest/peewee/api.html#Model.get_by_id
        product = Product.get_by_id(product_id)
        print("""
    Your search result is:
        """)
        print(f'NAME --------------|{product.product_name}')
        print('PRICE -------------|${}'.format(product.product_price / 100))
        print(f'QTY ---------------|{product.product_quantity}')
        print(f'DATE UPDATED ------|{product.date_updated}')
    except ValueError:
        print(f'Please enter a number value from 1 to {total_rows}')
    except Product.DoesNotExist:
        print(f"""The product does not exist.
{product_id} is not within 1 to {total_rows}
""")
        clear()



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
        ('v', search_product)
])

if __name__ == '__main__':
    try:
        loading()
        welcome()
        initialize()
        open_and_clean_csv()
        menu_loop()
    except KeyboardInterrupt:
        clear()
        print("\nThanks for dropping by!")