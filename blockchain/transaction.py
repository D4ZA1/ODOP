
import time

from security.key_generation import sign_data, verify_signature


class Transaction:


    def __init__(self, product_id, price, buyer=None, seller=None, timestamp=None, private_key=None, signature=None):
        self.product_id = product_id
        self.price = price
        self.buyer = buyer
        self.seller = seller
        self.timestamp = timestamp or time.time()

        if signature:
            self.signature = signature
        elif private_key:
            self.signature = self.sign_transaction(private_key)
        else:
            self.signature = None

    def to_dict(self):
        return {
            "product_id": self.product_id,
            "price": self.price,
            "buyer": self.buyer,
            "seller": self.seller,
            "timestamp": self.timestamp,
            "signature": self.signature if self.signature else None
        }

    def sign_transaction(self, private_key):
        data = f"{self.product_id}{self.price}{self.buyer}{self.seller}{self.timestamp}"
        return sign_data(private_key, data)

    def verify_transaction(self, public_key):
        if not self.signature:
            return False
        data = f"{self.product_id}{self.price}{self.buyer}{self.seller}{self.timestamp}"
        return verify_signature(public_key, data,self.signature)

