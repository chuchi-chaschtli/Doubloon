import hashlib
import json
from time import time
from uuid import uuid4

class Blockchain(object):
    def __init__(self):
        self.chain = []
        self.current_transactions = []

        self.add_block(prev_hash = 1, proof = 100)

    def add_block(self, proof, prev_hash = None):
        """
        Creates a new block in the chain.

        :param proof: <int> proof passed by the PoW algorithm.
        :param prev_hash: (Optional) <str> previous block hash
        :return: <dict> representation of the new block
        """
        new_block = {
            'index': len(self.chain) + 1,
            'timestamp': time(),
            'transactions': self.current_transactions,
            'proof': proof,
            'prev_hash': prev_hash or self.hash(self.chain[-1])
        }

        self.current_transactions = []

        self.chain.append(new_block)
        return new_block

    def add_transaction(self, sender, receiver, amt):
        """
        Constructs a new transaction to proceed to next mined Block.

        :param sender: <str> address of the Sender
        :param receiver: <str> address of the Receiver
        :param amt: <double> transaction amount
        :return: <index> block index to hold this transaction
        """
        self.current_transactions.append({
            'sender': sender, 
            'receiver': receiver, 
            'amount': amt
        })
        return self.last_block['index'] + 1

    def proof_of_work(self, prev):
        """
        Simple proof of work algorithm:
        - given a previous proof x, let x' be the current proof
        - finds a current proof x' such that hash(xx') has 4 trailing zeros

        :param prev: <int> the previous proof
        :return: <int> the current proof
        """
        curr = 0
        while not self.is_valid_proof(prev, curr):
            curr += 1
        return curr

    @staticmethod
    def is_valid_proof(prev, curr):
        """
        Validates a proof by checking if the hash of the previous and the current contain 4 trailing zeros

        :param prev: <int> previous proof
        :param curr: <int> current proof
        :return: <bool> True if correct, false otherwise
        """
        guess = f'{prev}{curr}'.encode()
        hash_guess = hashlib.sha256(guess).hexdigest()
        return hash_guess[-4:] == '0000'

    @staticmethod
    def hash(block):
        """
        Creates an SHA-256 block hash

        :param block: <dict> block
        :return: <str> hash
        """
        block_json = json.dumps(block, sort_keys=True)
        return hashlib.sha256(block_json.encode()).hexdigest()

    @property
    def last_block(self):
        return self.chain[-1]

