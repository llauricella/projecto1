# Importes externos
import requests
import json

# Busqueda de datos del Github de los equipos 
def fetch_teams(url):
    try:
        response = requests.get(url)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"Failed to fetch data: {e}")
        return None

# Busqueda de datos del Github de los estadios
def fetch_stadiums(url):
    try:
        response = requests.get(url)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"Failed to fetch data: {e}")
        return None

# Busqueda de datos del Github de los partidos
def fetch_matches(url):
    try:
        response = requests.get(url)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"Failed to fetch match data: {e}")
        return None

def load_json(file_path):
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            return json.load(file)
    except FileNotFoundError:
        return None