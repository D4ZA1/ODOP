
import time

from security.key_generation import sign_data, verify_signature


class Transaction:

    def __init__(self, product, district, price, quality_score, private_key=None, timestamp=None, buyer=None, seller=None):
        self.product = product
        self.district = district
        self.price = price
        self.quality_score = quality_score
        self.timestamp = timestamp or time.time()
        self.buyer = buyer
        self.seller = seller
        self.signature = None
        
        # Sign the transaction if private key is provided
        if private_key:
            self.signature = self.sign_transaction(private_key)

    def to_dict(self):
        return {
            "product": self.product,
            "district": self.district,
            "price": self.price,
            "quality_score": self.quality_score,
            "timestamp": self.timestamp,
            "buyer": self.buyer,
            "seller": self.seller,
            "signature": self.signature.hex() if self.signature else None
        }

    def sign_transaction(self, private_key):
        transaction_data = self.product + self.district + str(self.price) + str(self.quality_score) + str(self.timestamp)
        return sign_data(private_key, transaction_data)

    def verify_transaction(self, public_key):
        if self.signature is None:
            return False
        transaction_data = self.product + self.district + str(self.price) + str(self.quality_score) + str(self.timestamp)
        return verify_signature(public_key, transaction_data, bytes.fromhex(self.signature))

    def __str__(self):
        return f"Transaction({self.product}, {self.district}, {self.price}, {self.quality_score}, {self.timestamp})"

