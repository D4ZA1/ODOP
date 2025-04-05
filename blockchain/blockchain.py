from .block import Block
from .transaction import Transaction


class Blockchain:


    def __init__(self):
        self.chain = []
        self.create_genesis_block()

    def create_genesis_block(self):
        genesis_block = Block(0, "0", [])
        self.chain.append(genesis_block)

    def add_block(self, transactions, public_key):
        for tx_data in transactions:
            transaction = Transaction(**tx_data)
            if not transaction.verify_transaction(public_key):
                raise ValueError("Invalid transaction signature!")
        
        previous_block = self.chain[-1]
        new_block = Block(len(self.chain), previous_block.hash, transactions)
        self.chain.append(new_block)
        return new_block

    def get_chain(self):
        return [block.__dict__ for block in self.chain]

