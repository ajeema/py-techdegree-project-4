import csv
import os
from collections import OrderedDict
from datetime import datetime
from peewee import *

from tabulate import tabulate

# define database file
db = SqliteDatabase('inventory.db')



# function to clear screen
def clear_screen():
    os.system("cls" if os.name == "nt" else "clear")

class Product(Model):
    """establish the product types"""
    product_id = AutoField()
    product_name = CharField(unique=True)
    product_price = IntegerField()
    product_quantity = IntegerField()
    date_updated = DateTimeField(default = datetime.now)

    class Meta:
        database = db

# open and clean source csv
def clean_csv():
    with open('inventory.csv', newline='') as csvfile:
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
                continue
    else:
            Product.create(product_name=row['product_name'],
                               date_updated=row['date_updated'],
                               product_quantity=row['product_quantity'],
                               product_price=row['product_price'])

def initialize_db():
    """Initialize the database connection and create tables"""
    db.connect()
    db.create_tables([Product], safe = True)

def add_product():
    """add products"""
    clear_screen()

    print("Hello here you will add a product")


def search_product():
    clear_screen()
    """Search inventory by product ID"""
    choice = int(input("Enter the product ID you'd like to see details about: "))
    searched = Product.get_or_none(Product.product_id == choice)
    print(searched,
          searched.product_name,
          searched.product_quantity,
          searched.product_price / 100)

# TODO - Make this backup actual db. currently it backs up empty
def backup_db():
    clear_screen()
    """backup database to backup.csv"""
    filename_csv = (f'backup-{datetime.now()}.csv')
    backup = input("Would you like to backup?: ")
    if backup == "Y" or "y" and '1':
        db.freeze(table.all(), format='json', filename=f'backup-{datetime.now()}.csv')
    csvfile.close()


def landing_screen():
    """Initial application landing screen"""
    print("Welcome to the game!")


def menu_screen():
    clear_screen()
    """Show the menu"""
    choice = None
    while choice != 'q':

        print("Choose an option below, or press 'q' to quit")
        for key, value in menu.items():
            print('{}) {}'.format(key, value.__doc__))
        choice = input('Action: ').lower().strip()

        if choice in menu:
            menu[choice]()
        elif choice == 'q':
            break
        else:
            print("Oops, that wasn't a valid selection. Try again...\n")
            clear_screen()

def view_all():
    """view all the products"""
    # for product in Product.select():
    #     prod_id = product.product_id,
    #     prod_name = product.product_name,
    #     prod_updated = str(product.date_updated) [:10],
    #     prod_qty = product.product_quantity,
    #     prod_price = (product.product_price / 100)
    #
    #     print(product, prod_name)

    print(db.get_columns('ID'))

#--------------------------------------------
menu = OrderedDict([
    ('a', add_product),
    ('v', search_product),
    ('b', backup_db),
    ('e', view_all)
])

if __name__ == '__main__':
    landing_screen()
    initialize_db()
    clean_csv()
    menu_screen()

