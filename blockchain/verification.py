from hash_utils import hash_block, hash_string_256

class Verification:
    
    def verify_chain(self, blockchain):
        """Verifies the current blockchain and returns True if valid, False if not valid."""
        for (index, block) in enumerate(blockchain):  # creates tuple with index
            if index == 0:
                continue
            if block.previous_hash != hash_block(blockchain[index -1]):
                return False 
            if not self.valid_proof(block.transactions[:-1], block.previous_hash, block.proof):
                print("Proof of work is invalid")
                return False 
        return True 
    
    def verify_all_transactions(self, open_transactions, get_balance):
        """Verifies all open transactions."""
        return all([self.verify_transaction(tx, get_balance) for tx in open_transactions])
    
    def verify_transaction(self, transaction, get_balance):
        sender_balance = get_balance(transaction.sender)
        return sender_balance >= transaction.amount

    def valid_proof(self, transactions, last_hash, proof):
        guess = (str([tx.to_ordered_dict() for tx in transactions]) + str(last_hash) + str(proof)).encode()
        guess_hash = hash_string_256(guess)
        return guess_hash[0:2] == "00"