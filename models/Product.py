class Product:
    def __init__(self, name, quantity, min_stock_level, clinic_id):
        self.clinic_id = clinic_id
        self.name = name
        self.quantity = quantity
        self.min_stock_level = min_stock_level


    def print_details(self):
        print(f"name: {self.name} \nquantity: {self.quantity} \nminimum stock level: {self.min_stock_level} \nclinic id: {self.clinic_id}")