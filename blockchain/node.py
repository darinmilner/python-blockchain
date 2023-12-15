from blockchain import Blockchain
from verification import Verification
from uuid import uuid4

class Node:
    def __init__(self):
        # self.id = str(uuid4())
        self.id = "Ali"
        self.blockchain = Blockchain(self.id)
        
        
        
    def get_transaction_value(self):
        """Returns the input of a user as a transaction amount float value."""
        tx_recipient = input("Enter the transaction's recipient")
        tx_amount = float(input("Please enter your transaction amount "))
        return (tx_recipient, tx_amount)


    def get_user_choice(self):
        user_input = input("Your choice")
        return user_input


    def print_blockchain_elements(self):
        for block in self.blockchain.chain:
            print(f"Outputting block \n{block}")
        else:
            print("-" * 20)


    def listen_for_input(self):
        waiting_for_input = True 
        
        while waiting_for_input:
            print("Please choose")
            print("1: Add a new transaction")
            print("2: Output the blockchain blocks")
            print("3: Mine a new block.")
            print("4: check transaction validity")
            print("q: Quit")
            user_choice = self.get_user_choice()
            if user_choice == "1":
                tx_data = self.get_transaction_value()
                recipient, amount = tx_data
                if self.blockchain.add_transaction(recipient, self.id, amount=amount):
                    print("Added Transaction.")
                else:
                    print("Transaction failed.")
                print(self.blockchain.open_transactions)
            elif user_choice == "2":
                self.print_blockchain_elements()
            elif user_choice == "3":
                self.blockchain.mine_block()    
            elif user_choice == "4":
                if Verification.verify_all_transactions(self.blockchain.open_transactions, self.blockchain.get_balance):
                    print("All Transactions are valid.")
                else:
                    print("There are invalid transactions.")
            elif user_choice == "q":
                waiting_for_input = False 
            else:
                print("Invalid input. Please pick a valid input.")
           
            if not Verification.verify_chain(self.blockchain.chain):
                self.print_blockchain_elements()
                print("Invalid blockchain.")
                break
            print(f"Balance of {self.blockchain.get_balance()}")
        else:
            # executes when loop finishes
            print("User left")


        print("DONE!!")
        
node = Node()
node.listen_for_input()
