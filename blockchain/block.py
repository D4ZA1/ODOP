
import hashlib
import json
import time


class Block:



    def __init__(self, index, previous_hash, transactions, timestamp=None, nonce=0):
        self.index = index
        self.previous_hash = previous_hash
        self.transactions = transactions
        self.timestamp = timestamp or time.time()
        self.hash = self.compute_hash()
        self.nonce = 0  # Placeholder for proof-of-work
    def compute_hash(self):
        block_string = json.dumps(self.__dict__, sort_keys=True)
        return hashlib.sha256(block_string.encode()).hexdigest()

    def to_dict(self):
        return {
            "index": self.index,
            "previous_hash": self.previous_hash,
            "transactions": self.transactions,
            "timestamp": self.timestamp,
            "nonce": self.nonce,
            "hash": self.hash
        }
    @classmethod
    def from_dict(cls, data):
        block = cls(
            index=data["index"],
            previous_hash=data["previous_hash"],
            transactions=data["transactions"],
            timestamp=data.get("timestamp"),
        )
        block.hash = data["hash"]  # Reassign saved hash
        return block
