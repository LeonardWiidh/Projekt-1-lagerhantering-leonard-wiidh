'''
open.py: 
lagerhantering av ett gamestop där du kan ta bort (R), lägga till (A), ändra (E), inspektera (I) och avsluta programmet (Q).

__author__  = "Leonard Wiidh"
__version__ = "1.0.0"
__email__   = "leonard.wiidh@elev.ga.ntig.se"
'''

import csv
from colors import bcolors

#laddar produktdata från db_products.csv
def load_data(filename): 
    products = [] 
    with open(filename, 'r') as file:
        reader = csv.DictReader(file)
        for row in reader:
            products.append({
                "id": int(row['id']),
                "name": row['name'],
                "desc": row['desc'],
                "price": float(row['price']),
                "quantity": int(row['quantity'])
                
            })
    return products

#visar alla produkter i listan med snygg formatering
def view_products(products):
    header = f"{'Nr':<3} {'Id':<3} {'Name':<40} {'Description':<79} {'Price':<15} {'Quantity'}"
    line = "-" * len(header)
    print(f"{bcolors.BOLD}{bcolors.GREEN}{header}{bcolors.DEFAULT}")
    print(f"{bcolors.BLUE}{line}{bcolors.DEFAULT}")
    for index, product in enumerate(products, start=1):
        print(f"{index:<3} {product['id']:<3} {product['name']:<40} {product['desc']:<79} ${product['price']:<14.2f} {product['quantity']}")
    print(f"{bcolors.BLUE}{line}{bcolors.DEFAULT}")

#tar bort en produkt med ID
def remove_product(products, id):
    product = next((p for p in products if p["id"] == id), None)
    if product:
        products.remove(product)
        print(f"{bcolors.RED}Produkten '{product['name']}' togs bort.{bcolors.DEFAULT}")
    else:
        print(f"{bcolors.YELLOW}Produkten hittades inte.{bcolors.DEFAULT}")

#lägger till en ny produkt till listan
        
def add_product(products):
    try:

        new_id = max([p['id'] for p in products]) + 1 if products else 0
        name = input("Ange produktens namn: ").strip()
        desc = input("Ange produktens beskrivning: ").strip()
        price = float(input("Ange produktens pris: "))
        quantity = int(input("Ange produktens kvantitet: "))
        products.append({
            "id": new_id,
            "name": name,
            "desc": desc,
            "price": price,
            "quantity": quantity })
        print(f"{bcolors.GREEN}Produkten '{name}' lades till.{bcolors.DEFAULT}")
    except ValueError:
        print(f"{bcolors.RED}Ogiltiga värden, försök igen.{bcolors.DEFAULT}")

#redigerar en produkt med hjälp av ID
def edit_product(products, id):
    product = next((p for p in products if p["id"] == id), None)
    if product:
        print(f"{bcolors.CYAN}Redigerar produkt #{id}: {product['name']}{bcolors.DEFAULT}")
        product['name'] = input(f"Ange nytt namn ({product['name']}): ").strip() or product['name']
        product['desc'] = input(f"Ange ny beskrivning ({product['desc']}): ").strip() or product['desc']
        try:
            product['price'] = float(input(f"Ange nytt pris ({product['price']}): ") or product['price'])
            product['quantity'] = int(input(f"Ange ny kvantitet ({product['quantity']}): ") or product['quantity'])
            print(f"{bcolors.GREEN}Produkten uppdaterades.{bcolors.DEFAULT}")
        except ValueError:
            print(f"{bcolors.RED}Ogiltiga värden, inga ändringar sparades.{bcolors.DEFAULT}")
    else:

        print(f"{bcolors.YELLOW}Produkten hittades inte.{bcolors.DEFAULT}")


#visar detaljerad information om en specifik produkt
def inspect_product(products, id):
    product = next((p for p in products if p["id"] == id), None)
    if product:
        print(f"{bcolors.PURPLE}Produktdetaljer för #{id}:{bcolors.DEFAULT}")
        print(f"Namn: {product['name']}")
        print(f"Beskrivning: {product['desc']}")
        print(f"Pris: ${product['price']}")
        print(f"Lager: {product['quantity']}")
    else:

        print(f"{bcolors.YELLOW}Produkten hittades inte.{bcolors.DEFAULT}")

#sparar den uppdaterade produktlistan till db_products.csv
def save_data(products, filename):
    with open(filename, mode='w', newline='') as file:
        writer = csv.DictWriter(file, fieldnames=["id", "name", "desc", "price", "quantity"])
        writer.writeheader()
        writer.writerows(products)
    print(f"{bcolors.GREEN}Ändringar sparades.{bcolors.DEFAULT}")
#huvudfunktion för att hantera menyn och användarens val
    
def main():
    products = load_data('db_products.csv')
    while True:

        print("\n")
        view_products(products)
        print(f"\n{bcolors.BOLD}Menyn:{bcolors.DEFAULT}")
        print("(A) Lägg till en produkt")
        print("(R) Ta bort en produkt")
        print("(E) Redigera en produkt")
        print("(I) Inspektera en produkt")
        print("(Q) Avsluta programmet")
        
        choice = input("\nAnge ditt val: ").strip().upper()
        if choice == 'Q':
            save_data(products, 'db_products.csv')
            print(f"{bcolors.BOLD}Programmet avslutades.{bcolors.DEFAULT}")
            break
        elif choice == 'A':
            add_product(products)
        elif choice == 'R':
            try:
                id = int(input("Ange produkt-ID att radera: "))

                remove_product(products, id)
            except ValueError:
                print(f"{bcolors.RED}Ange ett giltigt ID.{bcolors.DEFAULT}")
        elif choice == 'E':
            try:
                id = int(input("Ange produkt-ID att redigera: "))
                edit_product(products, id)
            except ValueError:
                print(f"{bcolors.RED}Ange ett giltigt ID.{bcolors.DEFAULT}")
        elif choice == 'I':
            try:
                id = int(input("Ange produkt-ID att inspektera: "))

                inspect_product(products, id)
            except ValueError:
                print(f"{bcolors.RED}Ange ett giltigt ID.{bcolors.DEFAULT}")

        else:
            print(f"{bcolors.RED}Ogiltigt val, försök igen.{bcolors.DEFAULT}")
if __name__ == "__main__":
    main()
