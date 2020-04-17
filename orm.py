from peewee import *

from collections import OrderedDict
import datetime
import sys

db = SqliteDatabase('inventory.db')


class Entry(Model):
    context = TextField() 
    timestamp = DateTimeField(default=datetime.datetime.now)

    class Meta:
        database = db

def initialize():
    """create the database and the table if they don't exist"""
    db.connect()
    db.create_tables([Entry], safe=True)


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

def add_entry():
    """add an entry"""
    print("Enter your entry. Press ctrl+Z when finished.")
    data = sys.stdin.read().strip()

    if data:
        if input('Save entry? [Yn] ').lower() != 'n':
            Entry.create(content=data)
            print("Saved successfully!")


def view_entries():
    """view previous entries"""


def delete_entry(entry):
    """delete an entry"""

menu = OrderedDict([
    ('a', add_entry),
    ('v', view_entries),
])


if __name__ == '__main__':
    initialize()
    menu_loop()