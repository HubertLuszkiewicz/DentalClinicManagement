from tabulate import tabulate

def print_table(data, attributes):
    print(tabulate(data, headers=attributes))
                