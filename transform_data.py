from Team import Team
from Stadium import Stadium
from Restaurant import Restaurant
from Product import Product
from Match import Match

def transform_teams(raw_data_teams):
    teams = []
    for i in raw_data_teams:
        team = Team(
            id = i["id"],
            code = i["code"],
            name = i["name"],
            group = i["group"]
        )
        teams.append(team.to_dict())
    return teams

def transform_stadiums(raw_data_stadiums):
    stadiums = []
    restaurants = []
    products = []
    for i in raw_data_stadiums:
        stadium = Stadium(
            id=i["id"],
            name=i["name"],
            city=i["city"],
            capacity=i["capacity"]
        )
        for y in i["restaurants"]:
            restaurant = Restaurant(y["name"])
            for z in y["products"]:
                product = Product(
                    name=z["name"],
                    quantity=z["quantity"],
                    price=z["price"],
                    stock=z["stock"],
                    adicional=z["adicional"]
                )
                restaurant.add_product(product)
                products.append(product.to_dict())
            stadium.add_restaurant(restaurant)
            restaurants.append(restaurant.to_dict())
        stadiums.append(stadium.to_dict())
    return stadiums, restaurants, products

def transform_matches(raw_data_matches, teams):
    matches = []
    for i in raw_data_matches:
        try:
            if "id" in i and "number" in i and "home" in i and "away" in i and "date" in i and "group" in i:
                home_team = next((team for team in teams if team["id"] == i["home"]["id"]), None)
                away_team = next((team for team in teams if team["id"] == i["away"]["id"]), None)
                
                if home_team and away_team:
                    match = Match(id=i["id"],
                        number=i["number"],
                        home_team_id=home_team["id"],
                        home_team_name=home_team["name"],
                        home_team_code=home_team["code"],
                        away_team_id=away_team["id"],
                        away_team_name=away_team["name"],
                        away_team_code=away_team["code"],
                        date=i["date"],
                        group=i["group"])
                    matches.append(match.to_dict())
                else:
                    print(f"Error: Match data refers to non-existing team.")
            else:
                print(f"Error: Missing key in match data: {i}")
        except KeyError as e:
            print(f"Error: Missing key {e} in match data.")
            continue
    
    return matches