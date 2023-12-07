from functools import reduce 
import hashlib as hl
import json 
from hash_utils import hash_block
import pickle 
from block import Block 
from verification import Verification
from transaction import Transaction

MINING_REWARD = 10

blockchain = []
open_transactions = []
owner = "Yusuf"

def load_data():
    global blockchain
    global open_transactions
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
            blockchain = updated_blockchain
            open_transactions = json.loads(content[1])
            updated_transactions = []
            for tx in open_transactions:
                updated_transaction = Transaction(tx["sender"], tx["sender"], tx["amount"])
                updated_transactions.append(updated_transaction)
            open_transactions = updated_transactions
    except (IOError, IndexError):
        genesis_block = Block(0, "", [], 100, 0)
        blockchain = [genesis_block]
        open_transactions = []
        print("File Not Found")
    

def save_data():
    try:
        with open("blockchain.txt", mode="w") as f:
            saveable_chain = [block.__dict__ for block in [Block(block_el.index, block_el.previous_hash,[tx.__dict__ for tx in block_el.transactions] ,block_el.proof, block_el.timestamp) for block_el in blockchain]]
            f.write(json.dumps(saveable_chain))
            f.write("\n")
            saveable_tx = [tx.__dict__ for tx in open_transactions]
            f.write(json.dumps(saveable_tx))
    except:
        print("Saving Failed.")
    

def proof_of_work():
    last_block = blockchain[-1]
    last_hash = hash_block(last_block)
    proof = 0 
    verifier = Verification()
    while not verifier.valid_proof(open_transactions, last_hash, proof):
        proof += 1
    return proof 


def get_last_value():
    """Returns the last value of the current blockchain."""
    if len(blockchain) < 1:
        return None 
    return blockchain[-1]


def add_transaction(recipient, sender=owner, amount=1.0):
    """ Appends a new value as the last value to the blockchain.
    Arguments:
        :sender. Sender of the coins.
        :recipient: Recipient of the coins
        :amount: The amount of coins send. Default is 1.0
    """
    transaction = Transaction(sender, recipient, amount)
    verifier = Verification()
    if verifier.verify_transaction(transaction, get_balance):
        open_transactions.append(transaction)
        save_data()
        return True 
    return False 

def mine_block():
    last_block = blockchain[-1] # gets last value
    hashed_block = hash_block(last_block)
    proof = proof_of_work()
    
    reward_transaction = Transaction("MINING", owner, MINING_REWARD)
    
    copied_transactions = open_transactions[:]
    copied_transactions.append(reward_transaction)
    block = Block(len(blockchain), hashed_block, copied_transactions, proof)
    
    blockchain.append(block)
    return True 


def get_transaction_value():
    """Returns the input of a user as a transaction amount float value."""
    tx_recipient = input("Enter the transaction's recipient")
    tx_amount = float(input("Please enter your transaction amount "))
    return (tx_recipient, tx_amount)


def get_user_choice():
    user_input = input("Your choice")
    return user_input


def print_blockchain_elements():
    for block in blockchain:
        print(f"Outputting block \n{block}")
    else:
        print("-" * 20)


def get_balance(participant):
    tx_sender = [[tx.amount for tx in block.transactions if tx.sender == participant] for block in blockchain]
    open_tx_sender = [tx.amount for tx in open_transactions if tx.sender == participant]
    tx_sender.append(open_tx_sender)
    
    amount_sent = reduce(lambda tx_sum, tx_amt: tx_sum +sum(tx_amt) if len(tx_amt) > 0 else tx_sum + 0, tx_sender, 0)
    tx_recipient = [[tx.amount for tx in block.transactions if tx.recipient == participant] for block in blockchain]
    amount_recieved = reduce(lambda tx_sum, tx_amt: tx_sum + sum(tx_amt) if len(tx_amt) > 0 else tx_sum + 0, tx_recipient, 0)
   
    return amount_recieved - amount_sent


load_data()

waiting_for_input = True 
while waiting_for_input:
    print("Please choose")
    print("1: Add a new transaction")
    print("2: Output the blockchain blocks")
    print("3: Mine a new block.")
    print("4: check transaction validity")
    print("q: Quit")
    user_choice = get_user_choice()
    if user_choice == "1":
        tx_data = get_transaction_value()
        recipient, amount = tx_data
        if add_transaction(recipient=recipient, amount=amount):
            print("Added Transaction.")
        else:
            print("Transaction failed.")
        print(open_transactions)
    elif user_choice == "2":
        print_blockchain_elements()
    elif user_choice == "3":
        if mine_block():
            open_transactions = []
            save_data()
    elif user_choice == "4":
        verifier = Verification()
        if verifier.verify_all_transactions(open_transactions, get_balance):
            print("All Transactions are valid.")
        else:
            print("There are invalid transactions.")
    elif user_choice == "q":
        waiting_for_input = False 
    else:
       print("Invalid input. Please pick a valid input.")
    verifier = Verification()
    if not verifier.verify_chain(blockchain):
        print_blockchain_elements()
        print("Invalid blockchain.")
        break
    print(f"Balance of Yusuf {get_balance('Yusuf'):6.2f}")
else:
    # executes when loop finishes
    print("User left")


print("DONE!!")
