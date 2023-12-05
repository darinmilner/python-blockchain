from functools import reduce 
import hashlib as hl
from collections import OrderedDict
import json 
from hash_utils import hash_string_256, hash_block
import pickle 

MINING_REWARD = 10

blockchain = []
open_transactions = []
owner = "Yusuf"
participants = {"Yusuf"}

def load_data():
    global blockchain
    global open_transactions
    try:
        with open("blockchain.txt", mode="r") as f:
            content = f.readlines()
            # content = pickle.loads(f.read())   
            # blockchain = content["chain"]
            # open_transactions = content["ot"]
            blockchain = json.loads(content[0][:-1])  # gets line except for \n
            updated_blockchain = []
            for block in blockchain:
                updated_block = {
                    "previous_hash": block["previous_hash"],
                    "index": block["index"],
                    "proof": block["proof"],
                    "transactions": [
                        OrderedDict([("sender", tx["sender"]), ("recipient", tx["recipient"]), ("amount", tx["amount"])]) for tx in block["transactions"]
                    ]
                }
                updated_blockchain.append(updated_block)
            blockchain = updated_blockchain
            open_transactions = json.loads(content[1])
            updated_transactions = []
            for tx in open_transactions:
                updated_transaction = OrderedDict([("sender", tx["sender"]), ("recipient", tx["recipient"]), ("amount", tx["amount"])])
                updated_transactions.append(updated_transaction)
            open_transactions = updated_transactions
    except IOError:
        genesis_block = {
            "previous_hash": "", 
            "index": 0, 
            "transactions": [],
            "proof": 100
        }

        blockchain = [genesis_block]
        open_transactions = []
        print("File Not Found")
    

def save_data():
    try:
        with open("blockchain.txt", mode="w") as f:
            f.write(json.dumps(blockchain))
            f.write("\n")
            f.write(json.dumps(open_transactions))
    except:
        print("Saving Failed.")
        # save_data = {
        #     "chain": blockchain,
        #     "ot": open_transactions
        # }
        # f.write(pickle.dumps(save_data))
        

def valid_proof(transactions, last_hash, proof):
    guess = (str(transactions) + str(last_hash) + str(proof)).encode()
    guess_hash = hash_string_256(guess)
    return guess_hash[0:2] == "00"


def proof_of_work():
    last_block = blockchain[-1]
    last_hash = hash_block(last_block)
    proof = 0 
    while not valid_proof(open_transactions, last_hash, proof):
        proof += 1
    return proof 


def get_last_value():
    """Returns the last value of the current blockchain."""
    if len(blockchain) < 1:
        return None 
    return blockchain[-1]


def verify_transaction(transaction):
    sender_balance = get_balance(transaction["sender"])
    return sender_balance >= transaction["amount"]


def add_transaction(recipient, sender=owner, amount=1.0):
    """ Appends a new value as the last value to the blockchain.

    Arguments:
        :sender. Sender of the coins.
        :recipient: Recipient of the coins
        :amount: The amount of coins send. Default is 1.0
    """
    # transaction = {
    #     "sender" : sender,
    #     "recipient": recipient,
    #     "amount": amount
    # }

    transaction = OrderedDict([("sender", sender), ("recipient", recipient), ("amount", amount)])
    
    if verify_transaction(transaction):
        open_transactions.append(transaction)
        participants.add(sender)
        participants.add(recipient)
        save_data()
        return True 
    return False 


def mine_block():
    last_block = blockchain[-1] # gets last value
    hashed_block = hash_block(last_block)
    proof = proof_of_work()
    
    reward_transaction = OrderedDict([("sender","MINING"),("recipient", owner),("amount",MINING_REWARD)])
    
    copied_transactions = open_transactions[:]
    copied_transactions.append(reward_transaction)
    block = {
        "previous_hash": hashed_block, 
        "index": len(blockchain), 
        "transactions": copied_transactions,
        "proof" : proof,
    }
    
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
    tx_sender = [[tx["amount"] for tx in block["transactions"] if tx["sender"] == participant] for block in blockchain]
    open_tx_sender = [tx["amount"] for tx in open_transactions if tx["sender"] == participant]
    tx_sender.append(open_tx_sender)
    
    amount_sent = reduce(lambda tx_sum, tx_amt: tx_sum +sum(tx_amt) if len(tx_amt) > 0 else tx_sum + 0, tx_sender, 0)
    tx_recipient = [[tx["amount"] for tx in block["transactions"] if tx["recipient"] == participant] for block in blockchain]
    amount_recieved = reduce(lambda tx_sum, tx_amt: tx_sum + sum(tx_amt) if len(tx_amt) > 0 else tx_sum + 0, tx_recipient, 0)
   
    return amount_recieved - amount_sent


def verify_chain():
    """Verifies the current blockchain and returns True if valid, False if not valid."""
    for (index, block) in enumerate(blockchain):  # creates tuple with index
        if index == 0:
            continue
        if block["previous_hash"] != hash_block(blockchain[index -1]):
            return False 
        if not valid_proof(block["transactions"][:-1], block["previous_hash"], block["proof"]):
            print("Proof of work is invalid")
            return False 
    return True 


def verify_all_transactions():
    """Verifies all open transactions."""
    return all([verify_transaction(tx) for tx in open_transactions])

load_data()

waiting_for_input = True 
while waiting_for_input:
    print("Please choose")
    print("1: Add a new transaction")
    print("2: Output the blockchain blocks")
    print("3: Mine a new block.")
    print("4: Output Participants")
    print("5: check transaction validity")
    print("h: Manipulate blockhain blocks")
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
        print(participants)
    elif user_choice == "5":
        if verify_all_transactions():
            print("All Transactions are valid.")
        else:
            print("There are invalid transactions.")
    elif user_choice == "h":
        if len(blockchain) >= 1:
            blockchain[0] = {
                "previous_hash": "", 
                "index": 0, 
                "transactions": [{"sender": "Chris", "recipient": "Omar", "amount": 55.50}]
            }
    elif user_choice == "q":
        waiting_for_input = False 
    else:
       print("Invalid input. Please pick a valid input.")
    if not verify_chain():
        print_blockchain_elements()
        print("Invalid blockchain.")
        break
    print(f"Balance of Yusuf {get_balance('Yusuf'):6.2f}")
else:
    # executes when loop finishes
    print("User left")


print("DONE!!")