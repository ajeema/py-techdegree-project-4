from collections import OrderedDict


class MainMenu:

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


menu = OrderedDict([
    ('a', add_product),
    ('v', view_product),
    ('b', backup_products),
    ('e', view_every_product)
])


main_menu()