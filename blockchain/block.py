from time import time

class Block:
    def __init__(self,index, previous_hash, transactions, proof, timestamp=None):
        self.index = index 
        self.previous_hash = previous_hash
        self.timestamp = time() if timestamp is None else timestamp 
        self.transactions = transactions
        self.proof = proof 
           
    def __repr__(self):
        return "Index {}, Previous Hash {}, proof {}, transactions {}".format(self.index, self.previous_hash, self.proof, self.transactions)