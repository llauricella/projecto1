
def search_matches_by_country(matches, country):
    found_matches = []
    for match in matches:
        if match["home_team_name"] == country or match["away_team_name"] == country:
            found_matches.append(match)
    return found_matches

def search_matches_by_stadium(matches, stadium_name):
    found_matches = []
    for match in matches:
        if "stadium" in match and match["stadium"]["name"] == stadium_name:
            found_matches.append(match)
    return found_matches

def search_matches_by_date(matches, date_str):
    found_matches = []
    for match in matches:
        if match["date"] == date_str:
            found_matches.append(match)
    return found_matches

def display_matches(matches):
    if not matches:
        print("No se encontraron partidos que coincidan con los criterios de búsqueda.")
    else:
        print("Partidos encontrados:")
        for match in matches:
            print(f"ID: {match['id']}")
            print(f"Número: {match['number']}")
            print(f"Fecha: {match['date']}")
            print(f"Grupo: {match['group']}")
            print(f"Local: {match['home_team_name']} ({match['home_team_code']})")
            print(f"Visitante: {match['away_team_name']} ({match['away_team_code']})")
            print("-----------------------------------")

#____________________________________________________________________________________

# Función para buscar productos por nombre
def search_by_name(products, nombre):
    results = []
    for product in products:
        if nombre.lower() in product['name'].lower():
            results.append(product)
    return results

# Función para buscar productos por tipo adicional
def search_by_type(products, tipo):
    results = []
    for product in products:
        if product.get('adicional', '').lower() == tipo.lower():
            results.append(product)
    return results

# Función para buscar productos por rango de precio
def search_by_pricerange(products, min_price, max_price):
    results = []
    for product in products:
        precio = float(product['price'])
        if min_price <= precio <= max_price:
            results.append(product)
    return results

# Función para mostrar los resultados de búsqueda

def show_results(results):
    if results:
        for product in results:
            price = float(product['price'])
            taxed_price = price * 1.16  # Calcula el precio con 16% de impuesto
            product['price_with_tax'] = taxed_price  # Agrega el precio con impuesto al diccionario
            print(f"Nombre: {product['name']}")
            print(f"Cantidad: {product['quantity']}")
            print(f"Precio (sin impuesto): ${price:.2f}")
            print(f"Precio (con 16% de impuesto): ${taxed_price:.2f}")
            print(f"Stock: {product['stock']}")
            print(f"Adicional: {product['adicional']}")
            print()
    else:
        print("No se encontraron resultados.")