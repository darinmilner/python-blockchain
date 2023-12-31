from hash_utils import hash_block, hash_string_256

class Verification:
    @classmethod
    def verify_chain(cls, blockchain):
        """Verifies the current blockchain and returns True if valid, False if not valid."""
        for (index, block) in enumerate(blockchain):  # creates tuple with index
            if index == 0:
                continue
            if block.previous_hash != hash_block(blockchain[index -1]):
                return False 
            if not cls.valid_proof(block.transactions[:-1], block.previous_hash, block.proof):
                print("Proof of work is invalid")
                return False 
        return True 
    
    @classmethod
    def verify_all_transactions(cls, open_transactions, get_balance):
        """Verifies all open transactions."""
        return all([cls.verify_transaction(tx, get_balance) for tx in open_transactions])
    
    @staticmethod
    def verify_transaction(transaction, get_balance):
        sender_balance = get_balance()
        return sender_balance >= transaction.amount

    @staticmethod
    def valid_proof(transactions, last_hash, proof):
        guess = (str([tx.to_ordered_dict() for tx in transactions]) + str(last_hash) + str(proof)).encode()
        guess_hash = hash_string_256(guess)
        return guess_hash[0:2] == "00"