import time


class Product:


    def __init__(self, product_id, name, origin_district, market, timestamp=None):
        self.product_id = product_id
        self.name = name
        self.origin_district = origin_district
        self.market = market
        self.timestamp = timestamp or time.time()

    def to_dict(self):
        return {
            "product_id": self.product_id,
            "name": self.name,
            "origin_district": self.origin_district,
            "market": self.market,
            "timestamp": self.timestamp
        }
