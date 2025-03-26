from models.Clinic import Clinic
from utilities.print_table import print_table

def handle_clinic(database):
    while True:
        
        print("------------------------------------------------------------")
        print("Dostępne akcje: ")
        print("[1] - dodaj nowy gabinet")
        print("[2] - wyświetl listę gabinetów")
        print("[3] - edytuj dane gabinetu")
        print("[4] - usuń gabinet")
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
                    address = input("Podaj adres: ")
                    if not address:
                        print("Adres nie może być pusty!")
                    else: break
                
                while True:
                    phone_number = input("Podaj numer telefonu: ")
                    if not phone_number:
                        print("Nr telefonu nie może być pusty!")
                    elif len(phone_number) != 9:
                        print("Numer telefonu musi mieć dokładnie 9 cyfr!")
                    else:
                        if not phone_number.isdigit():
                            print("Numer telefonu musi składać się wyłącznie z cyfr!")
                        else:
                            break
                
                while True:
                    opening_hours = input("Podaj godziny otwarcia: ")
                    if not opening_hours:
                        print("Pole godziny otwarcia nie może być puste!")
                    elif "-" not in opening_hours:
                        print("Poprawny format to HH-HH!")
                    else:
                        h1, h2 = opening_hours.split("-")
                        if  not h1.isdigit() or not h2.isdigit():
                            print("godziny nie są liczbami!")
                        else: 
                            break
                            

                clinic = Clinic(name, address, phone_number, opening_hours)
                
                database.create_clinic(clinic)
                
                if (database.cursor.rowcount > 0):
                    print("Dodano do listy")
                else:
                    print("Nie powiodło się dodawanie do listy!")
                
            case 2:
                print("Lista gabinetów: ")
                clinics = database.read_clinics()
                attributes = database.get_attributes()
                print_table(clinics, attributes)

            case 3:
                clinics = database.read_clinics()
                if len(clinics) == 0:
                    print("Brak gabinetów w bazie!")
                    continue

                print("Wybierz gabinet do edycji: ")
                attributes = database.get_attributes()
                print_table(clinics, attributes)

                while True:
                    try:
                        id = int(input("Id gabinetu: "))
                        for clinic in clinics:
                            if clinic[0] == id: 
                                selected_clinic = clinic

                        print("Wybrano gabinet: ")
                        print_table([selected_clinic], attributes)
                        break

                    except ValueError:
                        print("Id musi być liczbą!")

                    except UnboundLocalError:
                        print("Brak gabinetu o podanym id!")

                
                print("Wpisz nowe dane lub wciśnij enter jeśli nie chcesz zmieniać")
                
                name = input("Podaj nową nazwę: ")

                address = input("Podaj nowy adres: ")

                while True:
                    phone_number = input("Podaj numer telefonu: ")
                    if not phone_number:
                        break
                    elif len(phone_number) != 9:
                        print("Numer telefonu musi mieć dokładnie 9 cyfr!")
                    else:
                        if not phone_number.isdigit():
                            print("Numer telefonu musi składać się wyłącznie z cyfr!")
                        else:
                            break
                
                while True:
                    opening_hours = input("Podaj godziny otwarcia: ")
                    if not opening_hours:
                        break
                    elif "-" not in opening_hours:
                        print("Poprawny format to HH-HH!")
                    else:
                        h1, h2 = opening_hours.split("-")
                        if  not h1.isdigit() or not h2.isdigit():
                            print("godziny nie są liczbami!")
                        else: 
                            break

                database.update_clinics(
                    id, 
                    name if name else selected_clinic[1],
                    address if address else selected_clinic[2], 
                    phone_number if phone_number else selected_clinic[3], 
                    opening_hours if opening_hours else selected_clinic[4]
                )

                print("Zmieniono dane gabinetu!")

            case 4:
                print("Który gabinet chcesz usunąć?")
                clinics = database.read_clinics()
                attributes = database.get_attributes()
                print_table(clinics, attributes)
                
                while True:
                    try:
                        id = int(input("Podaj id gabinetu do usunięcia: "))
                    except ValueError:
                        print("Niepopranwe id!")
                        continue
                    else:
                        database.delete_clinic(id)

                        if (database.cursor.rowcount > 0):
                            print("Usunięto gabinet!")
                            break
                        else:
                            print("Brak gabinetu o podanym id!")

            case _:
                print("Niepoprawny input")
        