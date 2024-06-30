# Importes externos
import json
import os
import random
import uuid

# Importes locales
from search import search_matches_by_country, search_matches_by_stadium, search_matches_by_date, display_matches, search_by_name, search_by_type, search_by_pricerange, show_results

def manage_matches(matches):
    if matches:
        while True:
            print("\nSeleccione una opción de búsqueda:")
            print("1. Buscar partidos por país")
            print("2. Buscar partidos por estadio")
            print("3. Buscar partidos por fecha")
            print("4. Salir")

            choice = input("Ingrese su opción: ")

            # Busca los partidos por país.
            if choice == '1':
                country = input("Ingrese el nombre del país: ")
                found_matches = search_matches_by_country(matches, country)
                display_matches(found_matches)

            # Busca partidos por estadio.
            elif choice == '2':
                stadium_name = input("Ingrese el nombre del estadio: ")
                found_matches = search_matches_by_stadium(matches, stadium_name)
                display_matches(found_matches)

            # Busca partido por fecha.
            elif choice == '3':
                date_str = input("Ingrese la fecha (YYYY-MM-DD): ")
                found_matches = search_matches_by_date(matches, date_str)
                display_matches(found_matches)

            # Sale del programa.
            elif choice == '4':
                print("Saliendo de la gestión de partidas.")
                break

            else:
                print("Opción no válida. Por favor, seleccione una opción del 1 al 4.")
    else:
        print("No se encontraron partidos cargados.")

# _______________________________________________________________________________________

def manage_sales(matches, stadiums):
    customer_name = input("Ingrese su nombre: ")
    customer_id = input("Ingrese su cédula: ")
    age = input("Ingrese su edad: ")

    print("\nPartidos disponibles:")
    for match in matches:
        print(f"Partido #{match['number']}: {match['home_team_name']} vs {match['away_team_name']} en {match['date']}")

    match_number = int(input("Ingrese el número del partido que desea comprar ticket: "))
    selected_match = next((match for match in matches if match['number'] == match_number), None)

    if not selected_match:
        print("Número de partido inválido.")
        return

    stadium = random.choice(stadiums)
    print(f"El partido seleccionado se jugará en el estadio: {stadium['name']}")

    seat_type = input("Tipo de entrada (General/VIP): ").lower()
    if seat_type not in ["general", "vip"]:
        print("Tipo de entrada inválido.")
        return

    price = 35 if seat_type == "general" else 75

    seats = load_seats_from_file(stadium["name"])
    if not seats:
        seats = [["O" for _ in range(stadium["capacity"][1])] for _ in range(stadium["capacity"][0])]

    while True:
        print("\nMapa de asientos (O = Libre, X = Ocupado):")
        for row in seats:
            print(" ".join(row))
        
        row = int(input("Seleccione la fila de su asiento: "))
        col = int(input("Seleccione la columna de su asiento: "))

        if seats[row][col] == "O":
            seats[row][col] = "X"
            break
        else:
            print("El asiento está ocupado, por favor seleccione otro.")

    subtotal = price
    discount = 0

    if is_vampire_number(int(customer_id)):
        discount = subtotal * 0.5
        print("¡Felicidades! Su cédula es un número vampiro. Obtiene un 50% de descuento.")

    iva = (subtotal - discount) * 0.16
    total = subtotal - discount + iva

    print(f"\nDetalle del costo:")
    print(f"Subtotal: ${subtotal}")
    print(f"Descuento: -${discount}")
    print(f"IVA: ${iva}")
    print(f"Total a pagar: ${total}")

    confirm = input("¿Desea proceder con el pago? (s/n): ")
    if confirm.lower() == 's':
        ticket_code = generate_ticket_code()
        ticket_data = {
            "code": ticket_code,
            "customer_id": customer_id,
            "customer_age": age,
            "ticket_type": seat_type,
            "match_number": match_number
        }
        save_tickets_data(ticket_data)
        save_seats_to_file(stadium["name"], seats)
        print(f"Pago exitoso. Código de Ticket: {ticket_code}")
    else:
        print("Compra cancelada.")

def load_seats_from_file(stadium_name):
    file_path = f"seats/{stadium_name}.json"
    if os.path.exists(file_path):
        with open(file_path, "r") as file:
            return json.load(file)
    else:
        return []

def is_vampire_number(num):
    num_str = str(num)
    length = len(num_str)
    if length % 2 != 0:
        return False
    half_length = length // 2
    pairs = [(num_str[:half_length], num_str[half_length:])]
    for pair in pairs:
        product = int(pair[0]) * int(pair[1])
        if sorted(str(product)) == sorted(num_str):
            return True
    return False

def generate_ticket_code():
    return str(uuid.uuid4())[:8]

def save_tickets_data(ticket_code):
    file_path = "tickets.json"
    if os.path.exists(file_path):
        with open(file_path, "r") as file:
            ticket_data = json.load(file)
    else:
        ticket_data = []
    if ticket_code not in ticket_data:
        ticket_data.append(ticket_code)
    with open(file_path, "w") as file:
        json.dump(ticket_data, file, indent=4)

def save_seats_to_file(stadium_name, seats):
    if not os.path.exists("seats"):
        os.makedirs("seats")
    file_path = f"seats/{stadium_name}.json"
    with open(file_path, "w") as file:
        json.dump(seats, file, indent=4)

#____________________________________________________________________

def manage_attendance(tickets):
    ticket_code = input("Ingrese el código del boleto: ")
    match_number = int(input("Ingrese el número del partido: "))
    message = validate_ticket(tickets, ticket_code, match_number)
    print(message)

def validate_ticket(tickets, ticket_code, match_number):
    file_path = "tickets.json"
    if ticket_code in tickets:
        tickets.remove(ticket_code)
        with open(file_path, "w") as file:
            json.dump(tickets, file, indent=4)
        return True, f"Boleto autenticado correctamente para el partido número {match_number}."
    return False, "Código de boleto inválido o ya utilizado."

#________________________________________________________________________

def manage_products(products):
    opcion = input("¿Qué desea buscar? (nombre / tipo / precio): ").lower()

    if opcion == "nombre":
        searched_name = input("Ingrese el nombre del producto: ").lower()
        results_name = search_by_name(products, searched_name)
        print(f"Resultados de búsqueda por nombre '{searched_name}':")
        show_results(results_name)

    elif opcion == "tipo":
        searched_type = input("Ingrese el tipo adicional ('alcoholic' / 'non-alcoholic' / 'plate'): ").lower()
        results_type = search_by_type(products, searched_type)
        print(f"Resultados de búsqueda por tipo '{searched_type}':")
        show_results(results_type)

    elif opcion == "precio":
        min_price = float(input("Ingrese el precio mínimo: "))
        max_price = float(input("Ingrese el precio máximo: "))
        results_price = search_by_pricerange(products, min_price, max_price)
        print(f"Resultados de búsqueda por rango de precio entre {min_price} y {max_price}:")
        show_results(results_price)

    else:
        print("Opción no válida. Por favor, elija 'nombre', 'tipo' o 'precio'.")

#_____________________________________________________________________________

def manage_restaurant_sales(products):
    customer_id = input("Ingrese su cédula: ")

    tickets = load_json('tickets.json')
    if not is_vip(customer_id, tickets):
        print("El cliente no tiene un boleto VIP.")
        return

    customer_age = get_customer_age(customer_id, tickets)
    if customer_age is None:
        print("No se pudo encontrar la edad del cliente.")
        return

    customer_order = []

    while True:
        print("\nProductos disponibles:")
        for product in products:
            if product["stock"] > 0:
                if "alcoholic" in product and product["alcoholic"] and customer_age < 18:
                    continue
                print(f"{product['name']} - ${product['price']} (Stock: {product['stock']})")

        product_name = input("Ingrese el nombre del producto que desea comprar (o 'n' para terminar): ")

        if product_name.lower() == 'n':
            break

        quantity = int(input("Ingrese la cantidad: "))

        product = next((p for p in products if p["name"] == product_name), None)

        if product and product["stock"] >= quantity:
            customer_order.append({
                "name": product["name"],
                "price": product["price"],
                "quantity": quantity
            })
            product["stock"] -= quantity
        else:
            print("Cantidad no disponible o producto no encontrado.")

    if not customer_order:
        print("No se seleccionaron productos.")
        return

    subtotal = sum(float(item["price"]) * float(item["quantity"]) for item in customer_order)
    discount = 0

    if is_perfect_number(int(customer_id)):
        discount = subtotal * 0.15

    total = subtotal - discount

    print("\nResumen de la compra:")
    for item in customer_order:
        print(f"{item['quantity']} x {item['name']} - ${item['price']} c/u")
    print(f"Subtotal: ${subtotal:.2f}")
    print(f"Descuento: -${discount:.2f}")
    print(f"Total: ${total:.2f}")

    confirm = input("¿Desea proceder con el pago? (s/n): ")
    if confirm.lower() == 's':
        save_json(products, 'products.json')
        save_restaurant_sales(customer_id, total)
        print("Pago exitoso. ¡Gracias por su compra!")
    else:
        print("Compra cancelada.")

def is_perfect_number(number):
    divisors = [i for i in range(1, number) if number % i == 0]
    return sum(divisors) == number

def is_vip(customer_id, tickets):
    for ticket in tickets:
        if ticket["customer_id"] == customer_id and ticket["ticket_type"].lower() == "vip":
            return True
    return False

def get_customer_age(customer_id, tickets):
    for ticket in tickets:
        if ticket["customer_id"] == customer_id:
            return int(ticket["customer_age"])
    return None

def save_json(data, file_path):
    with open(file_path, 'w', encoding='utf-8') as file:
        json.dump(data, file, ensure_ascii=False, indent=4)

def load_json(file_path):
    if os.path.exists(file_path):
        with open(file_path, 'r', encoding='utf-8') as file:
            return json.load(file)
    return []

def save_restaurant_sales(customer_id, total):
    file_path = "restaurant_sales.json"
    sales_data = load_json(file_path)

    sales_data.append({
        "customer_id": customer_id,
        "total_spent": total
    })

    save_json(sales_data, file_path)