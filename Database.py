import sqlite3

class Database:
    def __init__(self, db_name):
        self.db_name = db_name
        self.conn = sqlite3.connect(db_name)
        self.cursor = self.conn.cursor()
        self.conn.execute("PRAGMA foreign_keys = ON;")
    

    def get_attributes(self):
        return [d[0] for d in self.cursor.description]
    
    
    def init_database(self):

        self.cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS clinics(
                id INTEGER PRIMARY KEY, 
                name TEXT, 
                address TEXT, 
                phone_number TEXT, 
                opening_hours TEXT
            )
            """
        )
        self.cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS patients(
                id INTEGER PRIMARY KEY, 
                name TEXT, 
                surname TEXT, 
                pesel TEXT UNIQUE, 
                phone_number TEXT, 
                email TEXT
            )
            """
        )
        self.cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS dentists(
                id INTEGER PRIMARY KEY, 
                name TEXT, 
                surname TEXT, 
                specialisation TEXT, 
                clinic_id INTEGER,
                FOREIGN KEY(clinic_id) REFERENCES clinics(id)
            )
            """
        )
        self.cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS appointments(
                id INTEGER PRIMARY KEY,
                patient_id INTEGER,
                dentist_id INTEGER,
                clinic_id INTEGER,
                date STRING,
                time STRING,
                status STRING,
                FOREIGN KEY(patient_id) REFERENCES patients(id),
                FOREIGN KEY(dentist_id) REFERENCES dentists(id),
                FOREIGN KEY(clinic_id) REFERENCES clinics(id)
            )
            """
        )
        self.cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS treatments(
                id INTEGER PRIMARY KEY,
                name TEXT,
                description TEXT,
                price REAL
            )
            """
        )
        self.cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS payments(
                id INTEGER PRIMARY KEY,
                patient_id INTEGER,
                appointment_id INTEGER,
                amount REAL,
                status TEXT,
                FOREIGN KEY(patient_id) REFERENCES patients(id),
                FOREIGN KEY(appointment_id) REFERENCES appointments(id)
            )
            """
        )
        self.cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS products(
                id INTEGER PRIMARY KEY, 
                clinic_id INTEGER,
                name TEXT UNIQUE, 
                quantity INTEGER,
                min_stock_level INTEGER,
                FOREIGN KEY(clinic_id) REFERENCES clinics(id)
            )
            """
        )


    """
    /*************************************/
    ***       CRUD FOR PRODUCTS       ***
    /*************************************/
    """
    def create_product(self, product):
        self.cursor.execute(
            "INSERT INTO products(name, quantity, min_stock_level, clinic_id) VALUES (?, ?, ?, ?)", 
            (product.name, product.quantity, product.min_stock_level, product.clinic_id)
        )
        self.conn.commit()
    

    def read_products(self):
        res = self.cursor.execute("SELECT * FROM products")
        return res.fetchall()
    

    def read_products_with_clinic_name(self):
        res = self.cursor.execute(
            """
            SELECT p.id, c.name AS clinic_name, p.name AS product_name, p.quantity, p.min_stock_level
            FROM products p 
            JOIN clinics c ON c.id = p.clinic_id
            """
        )

        return res.fetchall()

    def update_product(self, new_name, new_quantity, new_min_stock_level, new_clinic, id):
        self.cursor.execute(
            """
            UPDATE products
            SET name = ?, quantity = ?, min_stock_level = ?, clinic_id = ?
            WHERE id = ?
            """, 
            (new_name, new_quantity, new_min_stock_level, new_clinic, id)
        )
        self.conn.commit()


    def delete_product(self, id):
        self.cursor.execute(
            "DELETE FROM products WHERE id = ?", (id, )
        )
        self.conn.commit()
    

    """
    /*************************************/
    ***        CRUD FOR CLINICS        ***
    /*************************************/
    """
    def create_clinic(self, clinic):
        
        self.cursor.execute(
            "INSERT INTO clinics(name, address, phone_number, opening_hours) VALUES (?, ?, ?, ?)", 
            (clinic.name, clinic.address, clinic.phone_number, clinic.opening_hours)
        )
        
        self.conn.commit()


    def read_clinics(self):
        res = self.cursor.execute("SELECT * FROM clinics")
        return res.fetchall()
    

    def update_clinics(self, id, name, address, phone_number, opening_hours):
        self.cursor.execute(
            """
            UPDATE clinics
            SET name = ?, address = ?, phone_number = ?, opening_hours = ?
            WHERE id = ?
            """,
            (name, address, phone_number, opening_hours, id)
        )
        self.conn.commit()
    

    def delete_clinic(self, id):
        self.cursor.execute(
            """
            DELETE FROM clinics
            WHERE id = ?
            """,
            (id, )
        )

        self.conn.commit()

    
    