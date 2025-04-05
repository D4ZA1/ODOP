import time

from security.key_generation import sign_data, verify_signature


class Transaction:



    def __init__(self, product, district, price, quality_score,
                 buyer=None, seller=None, private_key=None, timestamp=None, signature=None):
        self.product = product
        self.district = district
        self.price = price
        self.quality_score = quality_score
        self.timestamp = timestamp or time.time()
        self.buyer = buyer
        self.seller = seller
        self.signature = signature

        # Only sign if there's a private key and no existing signature
        if private_key and not self.signature:
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
        data = f"{self.product}{self.district}{self.price}{self.quality_score}{self.buyer}{self.seller}{self.timestamp}"
        return sign_data(private_key, data)

    def verify_transaction(self, public_key):
        if not self.signature:
            return False
        data = f"{self.product}{self.district}{self.price}{self.quality_score}{self.buyer}{self.seller}{self.timestamp}"
        return verify_signature(public_key, data, bytes.fromhex(self.signature))

    def __str__(self):
        return f"Transaction({self.product}, {self.district}, {self.price}, {self.quality_score}, {self.buyer}, {self.seller}, {self.timestamp})"

