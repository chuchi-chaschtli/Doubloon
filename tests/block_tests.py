from unittest import TestCase

import json
import hashlib

from src.block import Block

class BlockTests(TestCase):
    def setUp(self):
        self.block = Block(1, [], 0, 100)
        self.time = self.block.timestamp

    def test_init(self):
        self.assertEqual(self.block.index, 1)
        self.assertEqual(self.block.transactions, [])
        self.assertEqual(self.block.proof, 0)
        self.assertEqual(self.block.prev_hash, 100)

    def test_dict(self):
        block_dict = {
            'index': 1,
            'timestamp': self.time,
            'transactions': [],
            'proof': 0,
            'prev_hash': 100
        }
        self.assertEqual(self.block.dict, block_dict)

    def test_hash(self):
        block_data = json.dumps(self.block.dict, sort_keys=True).encode()
        block_hash = hashlib.sha256(block_data).hexdigest()

        self.assertEqual(len(block_hash), 64)
        self.assertEqual(block_hash, self.block.hash)