# Importes externos
import os
import json
from collections import defaultdict

def gestion_menu(restaurant_sales, matches, stadiums, tickets):
    while True:
        print("\nIndicadores de gestión")
        print("1. Promedio de gasto")
        print("2. Tabla de asistencia")
        print("3. Mayor asistencia")
        print("4. Mayor cantidad de boletos vendidos")
        print("5. Productos de resturante vendidos")
        print("6. Clientes con más boletos vendidos")
        print("7. Salir")
        
        choice = input("Elige una opción: ")
        
        if choice == '1':
            print("\nPromedio de gasto seleccionado")
            # Calcular y mostrar el promedio de gasto
            average_vip_spending, average_spending_per_customer = calculate_average_vip_spending(restaurant_sales)

            print(f"El promedio de gasto de un cliente VIP en un partido es: ${average_vip_spending:.2f}")

            print("\nPromedio de gasto por cliente VIP:")
            for customer_id, average_spent in average_spending_per_customer.items():
                print(f"Customer ID: {customer_id}, Promedio de gasto: ${average_spent:.2f}") 

        elif choice == '2':
            print("\nTabla de asistencia seleccionada")
            # Calcular y mostrar la asistencia de los partidos por estadio
            # No logre hacerlo
            print("En progreso...")
            break

        elif choice == '3':
            print("\nGestión de asistencias a partidos seleccionada")
            # Calcular la cantidad de asistencia por asientos ocupados
            sorted_stadiums = top_stadiums_by_x()

            print("Estadios ordenados por la cantidad de asientos ocupados ('X'):")
            for i, stadium in enumerate(sorted_stadiums, start=1):
                print(f"{i}. {stadium['stadium_name']} - {stadium['x_count']} asientos ocupados")
                        
        elif choice == '4':
            print("\nGestión de boletos comprados")
            # Calcular la cantidad de boletos comprados por asientos ocupados
            sorted_stadiums = top_stadiums_by_x()

            print("Estadios ordenados por la cantidad de boletos comprados:")
            for i, stadium in enumerate(sorted_stadiums, start=1):
                print(f"{i}. {stadium['stadium_name']} - {stadium['x_count']} boletos comprados")
            
        elif choice == '5':
            print("\nGestión de productos de resturante vendidos")
            # No lo pude hacer
            print("En progreso...")
            break
            
        elif choice == '6':
            print("\nClientes con más boletos vendidos seleccionada")
            # Top 3 clientes con más tickets vendidos mediante su cédula
            top_3_customers_with_most_tickets(tickets)

        elif choice == '7':
            print("Saliendo...")
            break

        else:
            print("Opción no válida. Por favor, elige de nuevo.")
    
#___________________________________________________________

def calculate_average_vip_spending(restaurant_sales):
        
        # Calculo de gasto de un VIP en un restaurante mediante los datos guardados en restaurant_sales.json

        if not restaurant_sales:
            print("No hay datos de ventas en restaurantes.")
            return 0, {}

        total_spent_by_customer = {}
        customer_count = {}

        for sale in restaurant_sales:
            customer_id = sale["customer_id"]
            total_spent = sale["total_spent"]

            if customer_id in total_spent_by_customer:
                total_spent_by_customer[customer_id] += total_spent
                customer_count[customer_id] += 1
            else:
                total_spent_by_customer[customer_id] = total_spent
                customer_count[customer_id] = 1

        total_spending = sum(total_spent_by_customer.values())
        total_customers = sum(customer_count.values())

        average_spending_per_customer = {}
        for customer_id, total_spent in total_spent_by_customer.items():
            average_spending_per_customer[customer_id] = total_spent / customer_count[customer_id]

        average_spending = total_spending / total_customers if total_customers > 0 else 0

        return average_spending, average_spending_per_customer

#____________________________________________________________


#________________________________________________________________

def count_x_in_seats(file_path):
    with open(file_path, 'r') as file:
        seats = json.load(file)
        count = sum(row.count('X') for row in seats)
    return count

def top_stadiums_by_x():
    seats_folder = "seats"
    stadiums = []

    # Obtener la lista de archivos JSON en la carpeta "seats"
    seat_files = [file for file in os.listdir(seats_folder) if file.endswith('.json')]

    # Contar la cantidad de 'X' en cada archivo y guardar los resultados
    for file in seat_files:
        file_path = os.path.join(seats_folder, file)
        stadium_name = file[:-5]  # Eliminar la extensión '.json' del nombre del archivo

        x_count = count_x_in_seats(file_path)
        stadiums.append({
            'stadium_name': stadium_name,
            'x_count': x_count
        })

    # Ordenar por la cantidad de 'X' de mayor a menor
    stadiums_sorted = sorted(stadiums, key=lambda x: x['x_count'], reverse=True)

    return stadiums_sorted

#________________________________________________________________

def top_3_customers_with_most_tickets(tickets):
    # Contar la cantidad de tickets por cada customer_id
    tickets_count = defaultdict(int)
    for ticket in tickets:
        customer_id = ticket['customer_id']
        tickets_count[customer_id] += 1

    # Ordenar customer_ids por cantidad de tickets (de mayor a menor)
    sorted_customers = sorted(tickets_count.items(), key=get_ticket_count, reverse=True)

    # Mostrar los top 3 clientes con más tickets
    print("Top 3 clientes con más boletos comprados:")
    for i, (customer_id, count) in enumerate(sorted_customers[:3], start=1):
        print(f"{i}. Cliente ID: {customer_id} - {count} boletos")

def get_ticket_count(item):
    # Función auxiliar para obtener la cantidad de boletos (usada como key en sorted())
    return item[1]