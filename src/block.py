import hashlib
import json
from time import time

class Block(object):
    def __init__(self, index, transactions, proof, prev_hash):
        self.index = index
        self.timestamp = time()
        self.transactions = transactions
        self.proof = proof
        self.prev_hash = prev_hash

    @property
    def hash(self):
        """
        Creates an SHA-256 block hash

        :param block: <dict> block
        :return: <str> hash
        """
        block_json = json.dumps(self.dict, sort_keys=True)
        return hashlib.sha256(block_json.encode()).hexdigest()

    @property
    def dict(self):
        """
        Grabs a json-friendly representation of the block

        :return: <dict> for the block
        """
        return {
            'index': self.index,
            'timestamp': self.timestamp,
            'transactions': self.transactions,
            'proof': self.proof,
            'prev_hash': self.prev_hash
        }