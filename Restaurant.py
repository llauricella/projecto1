class Restaurant:
    def __init__(self, name):
        self.name = name
        self.products = []

    def add_product(self, product):
        self.products.append(product)

    def to_dict(self):
        return {
            "name": self.name,
            "products": [product.to_dict() for product in self.products]
        }