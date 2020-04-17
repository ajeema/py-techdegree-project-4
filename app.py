#!/usr/bin/env python3

from collections import OrderedDict
import datetime
import os
import sys

from peewee import *

db = SqliteDatabase('test.db')

class Products(Model):
    content = TextField()
    timestamp = DateTimeField(default = datetime.datetime.now)

    class Meta:
        database = db


def initialize():
    db.connect()
    db.create_tables([Entry], safe = True)

def clear():
    os.system('cls' if os.name == 'nt' else 'clear')

def menu_loop():
    """Show the menu."""
    choice = None

    while choice != 'q':
        clear()
        print("Enter q to quit")
        for key, value in menu.items():
            print('{} {}'.format(key, value.__doc__))
        choice = input('Action: ').lower().strip()

        if choice in menu:
            clear()
            menu[choice]()



def add_entry():
    """) Add an entry."""
    pass

def view_entries(search_query=None):
    """ View previous entries."""
    pass



menu = OrderedDict([
        ('a', add_entry),
        ('v', view_entries),
])
if __name__ == "__main__":
    initialize()
    menu_loop()

