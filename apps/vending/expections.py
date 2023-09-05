class ProductOutOfStockException(Exception):
    def __init__(self, product, message=""):
        super().__init__(product.name + " is out of stock. " + message)


class NotEnoughCreditException(Exception):
    def __init__(self, message=""):
        super().__init__("You do not have enough credit. " + message)
