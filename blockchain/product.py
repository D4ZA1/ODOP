
import time


class Product:

    def __init__(self, product_id, name, category, origin_district, quality_score=None, timestamp=None):
        self.product_id = product_id
        self.name = name
        self.category = category
        self.origin_district = origin_district
        self.quality_score = quality_score
        self.timestamp = timestamp or time.time()

    def to_dict(self):
        return {
            "product_id": self.product_id,
            "name": self.name,
            "category": self.category,
            "origin_district": self.origin_district,
            "quality_score": self.quality_score,
            "timestamp": self.timestamp
        }

