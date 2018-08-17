import hashlib
import requests
from uuid import uuid4
from urllib.parse import urlparse

import constant
from transaction import Transaction
from block import Block

class Blockchain(object):
    def __init__(self):
        self.chain = []
        self.current_transactions = []
        self.peers = set()

        self.add_block(prev_hash = 1, proof = 100)

    def add_block(self, proof, prev_hash = None):
        """
        Creates a new block in the chain.

        :param proof: <int> proof passed by the PoW algorithm.
        :param prev_hash: (Optional) <str> previous block hash
        :return: <dict> representation of the new block
        """
        new_block = Block(
            len(self.chain) + 1, 
            self.current_transactions, 
            proof, 
            prev_hash or self.last_block.hash)

        self.current_transactions = []

        self.chain.append(new_block)
        return new_block.dict

    def add_transaction(self, sender, receiver, amount, signature):
        """
        Constructs a new transaction to proceed to next mined Block.

        :param sender: <str> address key of the sender
        :param receiver: <str> address key of the receiver
        :param amount: <int> transaction amount
        :param signature: the private key signature of the sender
        :return: <index> block index to hold this transaction
        """
        transaction = Transaction(sender, receiver, amount)

        if sender == constant.MINER_KEY or transaction.verify_signature(
            signature):
            self.current_transactions.append(transaction.dict)
            return len(self.chain) + 1

        return -1

    def add_peer(self, address):
        """
        Adds a new node to the list of peers

        :param address: <str> address of the new peer
        """
        url = urlparse(address)
        if url.netloc:
            self.peers.add(url.netloc)
        elif url.path:
            self.peers.add(url.path)
        else:
            raise ValueError('Malformed URL peer')

    def resolve(self):
        """
        Replaces chain with longest one in the network.

        :return: <bool> true if the current chain is replaced, false if the 
        chain is authoritative
        """
        curr_peers = self.peers
        result = None

        min_length = len(self.chain)

        for peer in curr_peers:
            response = requests.get(f'http://{peer}/chain')

            if response.status_code == 200:
                length = response.json()['length']
                chain = response.json()['chain']

                if length > min_length and self.__is_valid_chain(chain):
                    min_length = length
                    result = chain

        if result:
            self.chain = result
            return True
        return False

    def proof_of_work(self, prev):
        """
        Simple proof of work algorithm:
        - given a previous proof x, let x' be the current proof
        - finds a current proof x' such that hash(xx') has 4 trailing zeros

        :param prev: <int> the previous proof
        :return: <int> the current proof
        """
        nonce = 0
        while not self.__is_valid_proof(prev, nonce):
            nonce += 1
        return nonce

    @property
    def last_block(self):
        return self.chain[-1]

    @staticmethod
    def __is_valid_chain(self, chain):
        """
        Determines a given blockchain is valid

        :param chain: <list> a blockchain
        :return: <bool> true if valid, false otherwise
        """
        block_ptr = chain[0]
        current_index = 1
        while current_index < len(chain):
            curr_block = chain[current_index]

            if curr_block.prev_hash != block_ptr.hash:
                return False
            
            if self.__is_valid_proof(block_ptr.proof, curr_block.proof):
                return False

            block_ptr = curr_block
            current_index += 1
        return True

    @staticmethod
    def __is_valid_proof(prev, nonce):
        """
        Validates a proof by checking if the hash of the previous and the 
        current contain 4 trailing zeros

        :param prev: <int> previous proof
        :param nonce: <int> current proof
        :return: <bool> True if correct, false otherwise
        """
        guess = f'{prev}{nonce}'.encode()
        hash_guess = hashlib.sha256(guess).hexdigest()
        return hash_guess[-4:] == '0000'