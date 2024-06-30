# Importes externos
import json
import os

# Importes locales
from fetch_data import fetch_teams, fetch_stadiums, fetch_matches, load_json
from transform_data import transform_teams, transform_stadiums, transform_matches
from manage import manage_matches, manage_sales, manage_attendance, manage_products, manage_restaurant_sales
from gestion import gestion_menu

# Guardado de data
def save_data(data, file_path):
    if os.path.exists(file_path):
        with open(file_path, 'w', encoding='utf-8') as file:
            json.dump(data, file, ensure_ascii=False, indent=4)
    else:
        data = []

# URLs de la data
url_teams = "https://raw.githubusercontent.com/Algoritmos-y-Programacion/api-proyecto/main/teams.json"
url_stadiums = "https://raw.githubusercontent.com/Algoritmos-y-Programacion/api-proyecto/main/stadiums.json"
url_matches = "https://raw.githubusercontent.com/Algoritmos-y-Programacion/api-proyecto/main/matches.json"

# Archivos locales para guardar los datos
file_path_teams = "teams.json"
file_path_stadiums = "stadiums.json"
file_path_restaurants = "restaurants.json"
file_path_products = "products.json"
file_path_matches = "matches.json"
file_path_tickets = "tickets.json"
file_path_restaurant_sales = "restaurant_sales.json"

# Fetch y transformación de datos de equipos
raw_data_teams = fetch_teams(url_teams)
if raw_data_teams is not None:
    teams = transform_teams(raw_data_teams)
    save_data(teams, file_path_teams)
    print("Datos de equipos guardados.")
else:
    print("No se pudieron obtener los datos de equipos.")

# Fetch y transformación de datos de estadios, restaurantes y productos
raw_data_stadiums = fetch_stadiums(url_stadiums)
if raw_data_stadiums is not None:
    stadiums, restaurants, products = transform_stadiums(raw_data_stadiums)
    save_data(stadiums, file_path_stadiums)
    save_data(restaurants, file_path_restaurants)
    save_data(products, file_path_products)
    print("Datos de estadios, restaurantes y productos guardados.")
else:
    print("No se pudieron obtener los datos de estadios.")

# Fetch y transformación de datos de partidos
raw_data_matches = fetch_matches(url_matches)
if raw_data_matches is not None:
    teams = load_json(file_path_teams)
    matches = transform_matches(raw_data_matches, teams)
    save_data(matches, file_path_matches)
    print("Datos de partidos guardados.")
else:
    print("No se pudieron obtener los datos de partidos.")


# Menú principal
while True:
    print("\nMenú Principal")
    print("1. Gestionar partidos y estadios")
    print("2. Gestionar venta de entradas")
    print("3. Gestionar asistencias a partidos")
    print("4. Gestionar restaurantes")
    print("5. Gestionar venta de restaurantes")
    print("6. Indicadores de gestión")
    print("7. Salir")
    
    choice = input("Elige una opción: ")
    
    if choice == '1':
        print("\nGestión de partidos y estadios seleccionada")
        # Gestión de partidos.
        matches = load_json(file_path_matches)
        manage_matches(matches)

    elif choice == '2':
        print("\nGestión de venta de entradas seleccionada")
        # Gestión de venta de entradas.
        matches = load_json(file_path_matches)
        stadiums = load_json(file_path_stadiums)
        manage_sales(matches, stadiums)

    elif choice == '3':
        print("\nGestión de asistencias a partidos seleccionada")
        # Gestión de confirmación de tickets
        tickets = load_json(tickets)
        manage_attendance(tickets)
        
    elif choice == '4':
        print("\nGestión de restaurantes seleccionada")
        # Gestión de restaurantes
        products = load_json(file_path_products)
        manage_products(products)

    elif choice == '5':
        print("\nGestión de venta de restaurantes seleccionada")
        # Gestión de venta de restaurantes
        products = load_json(file_path_products)
        manage_restaurant_sales(products)

    elif choice == '6':
        print("\nIndicadores de gestión seleccionada")
        # Indicadores de gestión
        restaurant_sales = load_json(file_path_restaurant_sales)
        matches = load_json(file_path_matches)
        stadiums = load_json(file_path_stadiums)
        tickets = load_json(file_path_tickets)
        gestion_menu(restaurant_sales, matches, stadiums, tickets)

    elif choice == '7':
        print("Saliendo...")
        break
    else:
        print("Opción no válida. Por favor, elige de nuevo.")
