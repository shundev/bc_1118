from time import time

# Genesis block
init_tx = [
    {
        "sender": None,
        "recipient": "localhost:2000",
        "amount": 1000
    },
    {
        "sender": None,
        "recipient": "localhost:2001",
        "amount": 2000
    }
]


class Blockchain(object):
    def __init__(self):
        self.chain = []
        self.current_txs = []
        self.nodes = set()

        self.current_txs.extend(init_tx)

        self.new_block(previous_hash=1, proof=100)
    
    def new_block(self, previous_hash, proof):
        block = {
            "index": len(self.chain) + 1,
            "timestamp": time(),
            "transactions": self.current_txs,
            "proof": proof,
            "previous_hash": previous_hash
        }

        self.current_txs = []
        self.chain.append(block)
        return block
