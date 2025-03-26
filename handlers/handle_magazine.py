from models.Product import Product
from tabulate import tabulate
from utilities.print_table import print_table
import sqlite3

def handle_magazine(database):
    while True:
        print("------------------------------------------------------------")
        print("Dostępne akcje: ")
        print("[1] - dodaj nowy produkt")
        print("[2] - wyświetl listę produktów w magazynie")
        print("[3] - edytuj produkt")
        print("[4] - usuń produkt")
        print("[0] - powrót do menu głównego")
        print("------------------------------------------------------------")
        option = int(input("Wybierz akcję: "))
        if option == 0: break
        match option:
            case 1:

                while True:
                    name = input("Podaj nazwe: ")
                    if not name:
                        print("Nazwa nie może być pusta!")
                    else: break
                
                while True:
                    try:
                        quantity = int(input("Podaj ilość: "))
                        if quantity <= 0: 
                            print("Ilość musi być większa od 0!")
                            continue
                        break

                    except ValueError:
                        print("Ilość musi być liczbą!")
                
                while True:
                    try:
                        min_stock_level = int(input("Podaj mininmalny stan magazynowy: "))
                        if quantity <= 0: 
                            print("Minimalny stan magazynowy musi być większy od 0!")
                            continue
                        break
                    except ValueError:
                        print("Minimalny wymagany stan musi być liczbą!")
                
                print("Wybierz gabinet: ")
                clinics = database.read_clinics()
                for cli in clinics:
                    print(f"[{cli[0]}] - {cli[1]}")
                
                while True:
                    try:
                        clinic_id = int(input("Podaj id gabinetu: "))
                        product = Product(name, quantity, min_stock_level, clinic_id)
                        database.create_product(product)
                        print("Dodano do listy")
                        break
                    except ValueError:
                        print("Id musi być liczbą!")

                    except sqlite3.IntegrityError:
                        print("Brak gabinetu o takim id!")

            case 2:
                print("Lista produktów: ")
            
                products = database.read_products_with_clinic_name()
                attributes = database.get_attributes()
                print_table(products, attributes)

            case 3:
                products = database.read_products()
                if len(products) == 0:
                    print("Brak produktów w magazynie!")
                    continue

                print("Który produkt produkt chcesz zmienić?")
                attributes = database.get_attributes()
                print_table(products, attributes)

                num = int(input("Wybierz id produktu do edycji: "))
                idx = [p[0] for p in products].index(num)
                selected_product = products[idx]
                
                print("Wybrano produkt: ")
                print_table([selected_product], attributes)
                
                new_name = input("Podaj nowa nazwe: ")
                new_quantity = int(input("Podaj nową ilość: "))
                new_min_stock_level = int(input("Podaj minimalny stan magazynowy: "))
                
                print("Dla którego gabinetu?")
                clinics = database.read_clinics()
                for cli in clinics:
                    print(f"[{cli[0]}] - {cli[2]}")
                new_clinic = int(input("Podaj id gabinetu: "))

                database.update_product(new_name, new_quantity, new_min_stock_level, new_clinic, selected_product[0])
                print("Zmieniono produkt!")

            case 4:
                products = database.read_products()
                
                print("Który produkt usunąć?")
                attributes = database.get_attributes()
                print_table(products, attributes)

                product_id = int(input("Podaj id produktu do usunięcia: "))
                
                database.delete_product(product_id)
                print(f"Usunięto z listy")

            case _:
                print("Niepoprawny input")
        