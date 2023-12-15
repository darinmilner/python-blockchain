from functools import reduce 
import hashlib as hl
import json 
from hash_utils import hash_block
import pickle 
from block import Block 
from verification import Verification
from transaction import Transaction

MINING_REWARD = 10

class Blockchain:
    def __init__(self, hosting_node_id):
        genesis_block = Block(0, "", [], 100, 0)
        self.chain = [genesis_block]
        self.open_transactions = []
        self.load_data()
        self.hosting_node = hosting_node_id

    def load_data(self):
        try:
            with open("blockchain.txt", mode="r") as f:
                content = f.readlines()
                blockchain = json.loads(content[0][:-1])  # gets line except for \n
                updated_blockchain = []
                for block in blockchain:           
                    converted_tx = [Transaction(tx["sender"], tx["recipient"], tx["amount"]) for tx in block["transactions"]]
            
                    updated_block = Block(
                        block["index"], 
                        block["previous_hash"],
                        converted_tx,
                        block["proof"],
                        block["timestamp"]
                    )
                
                    updated_blockchain.append(updated_block)
                self.chain = updated_blockchain
                open_transactions = json.loads(content[1])
                updated_transactions = []
                for tx in open_transactions:
                    updated_transaction = Transaction(tx["sender"], tx["sender"], tx["amount"])
                    updated_transactions.append(updated_transaction)
                self.open_transactions = updated_transactions
        except (IOError, IndexError):
            print("Handled Exception.")
    

    def save_data(self):
        try:
            with open("blockchain.txt", mode="w") as f:
                saveable_chain = [block.__dict__ for block in [Block(block_el.index, block_el.previous_hash,[tx.__dict__ for tx in block_el.transactions] ,block_el.proof, block_el.timestamp) for block_el in self.chain]]
                f.write(json.dumps(saveable_chain))
                f.write("\n")
                saveable_tx = [tx.__dict__ for tx in self.open_transactions]
                f.write(json.dumps(saveable_tx))
        except:
            print("Saving Failed.")
        

    def proof_of_work(self):
        last_block = self.chain[-1]
        last_hash = hash_block(last_block)
        proof = 0 
       
        while not Verification.valid_proof(self.open_transactions, last_hash, proof):
            proof += 1
        return proof 


    def get_last_value(self):
        """Returns the last value of the current blockchain."""
        if len(self.chain) < 1:
            return None 
        return self.chain[-1]


    def add_transaction(self, recipient, sender, amount=1.0):
        """ Appends a new value as the last value to the blockchain.
        Arguments:
            :sender. Sender of the coins.
            :recipient: Recipient of the coins
            :amount: The amount of coins send. Default is 1.0
        """
        transaction = Transaction(sender, recipient, amount)
      
        if Verification.verify_transaction(transaction, self.get_balance):
            self.open_transactions.append(transaction)
            self.save_data()
            return True 
        return False 

    def mine_block(self):
        last_block = self.chain[-1] # gets last value
        hashed_block = hash_block(last_block)
        proof = self.proof_of_work()
        
        reward_transaction = Transaction("MINING", self.hosting_node, MINING_REWARD)
        
        copied_transactions = self.open_transactions[:]
        copied_transactions.append(reward_transaction)
        block = Block(len(self.chain), hashed_block, copied_transactions, proof)
        
        self.chain.append(block)
        self.open_transactions = []
        self.save_data()
        return True 


    def get_balance(self):
        participant = self.hosting_node
        
        tx_sender = [[tx.amount for tx in block.transactions if tx.sender == participant] for block in self.chain]
        open_tx_sender = [tx.amount for tx in self.open_transactions if tx.sender == participant]
        tx_sender.append(open_tx_sender)
        
        amount_sent = reduce(lambda tx_sum, tx_amt: tx_sum +sum(tx_amt) if len(tx_amt) > 0 else tx_sum + 0, tx_sender, 0)
        tx_recipient = [[tx.amount for tx in block.transactions if tx.recipient == participant] for block in self.chain]
        amount_recieved = reduce(lambda tx_sum, tx_amt: tx_sum + sum(tx_amt) if len(tx_amt) > 0 else tx_sum + 0, tx_recipient, 0)
    
        return amount_recieved - amount_sent



