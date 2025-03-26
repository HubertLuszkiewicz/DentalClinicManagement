from models.Product import Product
from Database import Database
from handlers.handle_magazine import handle_magazine
from handlers.handle_clinic import handle_clinic
if __name__ == "__main__":

    database = Database("database.db")
    database.init_database()
    res = database.cursor.execute("SELECT name FROM sqlite_master")
    x = res.fetchall()
    print(x)


    while(True):
        print("------------------------------------------------------------")
        print("Zarządzaj siecią gabinetów dentystycznych: ")
        print("------------------------------------------------------------")
        print("[1] - Gabinety")
        print("[2] - Pacjenci")
        print("[3] - Dentyści")
        print("[4] - Wizyty")
        print("[5] - Zabiegi")
        print("[6] - Płatności")
        print("[7] - Magazyn")

        table_number = int(input("Podaj number tabeli: "))

        match table_number:
            case 1:
                handle_clinic(database)
            case 7:
                handle_magazine(database)
            case _:
                print("Na razie brak obsługi")