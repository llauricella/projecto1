class Stadium:
    def __init__(self, id, name, city, capacity):
        self.id = id
        self.name = name
        self.city = city
        self.capacity = capacity
        self.restaurants = []

    def add_restaurant(self, restaurant):
        self.restaurants.append(restaurant)

    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "city": self.city,
            "capacity": self.capacity,
            "restaurants": [restaurant.to_dict() for restaurant in self.restaurants]
        }