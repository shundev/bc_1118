import hashlib
import json
from time import time
import requests


class Blockchain(object):
    def __init__(self):
        self.chain = []
        self.current_transactions = []
        self.nodes = set()

        self.new_block(previous_hash=1, proof=100)
    
    def register_node(self, address):
        self.nodes.add(address)
        
    def new_block(self, proof, previous_hash=None):
        block = {
            "index": len(self.chain) + 1,
            "timestamp": time(),
            "transactions": self.current_transactions,
            "proof": proof,
            "previous_hash": previous_hash or self.hash(self.chain[-1])
        }

        self.current_transactions = []
        self.chain.append(block)
        return block

    def new_transaction(self, sender, recipient, amount):
        self.current_transactions.append({
            "sender": sender,
            "recipient": recipient,
            "amount": amount
        })

        return self.last_block["index"] + 1
    
    def proof_of_work(self, last_proof):
        proof = 0
        while self.valid_proof(last_proof, proof) is False:
            proof += 1
        
        return proof
    
    def resolve_conficts(self):
        new_chain = None
        max_lengh = len(self.chain)

        for node in self.nodes:
            res = requests.get(f"http://{node}/chain")
            if res.status_code == 200:
                length = res.json()["length"]
                chain = res.json()["chain"]

                if length > max_lengh and self.valid_chain(chain):
                    max_lengh = length
                    new_chain = chain
            
        if new_chain:
            self.chain = new_chain
            return True
        
        return False
    
    def valid_chain(self, chain):
        last_block = chain[0]
        current_index = 1

        while current_index < len(chain):
            block = chain[current_index]
            if block["previous_hash"] != self.hash(last_block):
                return False
            
            if not self.valid_proof(last_block["proof"], block["proof"]):
                return False
            
            last_block = block
            current_index += 1
        
        return True
    
    @staticmethod
    def valid_proof(last_proof, proof):
        guess = f"{last_proof}{proof}".encode()
        guess_hash = hashlib.sha256(guess).hexdigest()

        return guess_hash[:4] == "0000"

    @staticmethod
    def hash(block):
        block_string = json.dumps(block, sort_keys=True).encode()
        return hashlib.sha256(block_string).hexdigest()

    @property
    def last_block(self):
        return self.chain[-1]


