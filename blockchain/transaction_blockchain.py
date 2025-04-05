import json

from blockchain.block import Block
from blockchain.transaction import Transaction


class TransactionBlockchain:




    def __init__(self):
        self.chain = []
        self.create_genesis_block()

    def create_genesis_block(self):
        genesis = Block(0, "0", [])
        self.chain.append(genesis)

    def add_block(self, transactions, public_key):
        validated = []
        for tx_data in transactions:
            tx = Transaction(**tx_data)
            if tx.verify_transaction(public_key):
                validated.append(tx.to_dict())
            else:
                raise ValueError("Invalid signature.")
        new_block = Block(len(self.chain), self.chain[-1].hash, validated)
        self.chain.append(new_block)

    def get_chain(self):
        return [block.__dict__ for block in self.chain]

    def save_chain(self, filename):
        with open(filename, 'w') as f:
            json.dump([block.to_dict() for block in self.chain], f, indent=2)


    def load_chain(self, filename):
        try:
            with open(filename, 'r') as f:
                data = json.load(f)
                self.chain = [Block.from_dict(b) for b in data]
        except FileNotFoundError:
            print(f"[INFO] Chain file {filename} not found. Starting fresh.")
