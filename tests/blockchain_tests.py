import sys
sys.path.append(sys.path[0] + '/src')

from unittest import TestCase

from src.blockchain import Blockchain
from src import constant

PUBLIC_KEY = '30819f300d06092a864886f70d010101050003818d0030818902818100d99c9347b6ecd418b1df48012201c5bd2869a707e45dee91a5c63027dc8020210aa4cf6e34e81fc200f29c893add94fefbf37594a964641fc52f8905280c4d93457d4cee5fb216a09a9e8688c62e26bc9e962357c019c5e6c73818f155b87ccaa70059cfa0698c85f5d982bef73bc84e6dfac540cf4f43308b799b8439c1011d0203010001'
PRIVATE_KEY = '3082025b02010002818100d99c9347b6ecd418b1df48012201c5bd2869a707e45dee91a5c63027dc8020210aa4cf6e34e81fc200f29c893add94fefbf37594a964641fc52f8905280c4d93457d4cee5fb216a09a9e8688c62e26bc9e962357c019c5e6c73818f155b87ccaa70059cfa0698c85f5d982bef73bc84e6dfac540cf4f43308b799b8439c1011d02030100010281802b55c5f2a317f888ce6b33909e30122bc02f8206cd507360e7cd56eba93a8eab65ce3a4cad1688b47eb1d1c0764b880f5b273984185398a8c700d75d828328b34bffe18565d9145a0db7aef152a9452642acc0518ccfa224287ba38fabb93a51f0da4db17b82a0ca12b6b69ff1c7b172061ce60ae9665b064ee21490e5cd0215024100db115ac3a95d00bdeabb429f841100d2786ab0849753eed0e0208020e8fe2e5d7e171d69d7552a9adee2840e846e56a6b1452c3a7b7c330f02595b3479f815cf024100fe4c5fe8c71d1e746d83b9bd9021d1fd6027090382321421f432ffabc713fca58cf1d116108e493a7b98854be96c761300a891f281db40ffdb9edc09cb29e15302404ca9f3209c299ef3d7acb6f10a0fc540e2c13b8afb46754205dd79d98a90417b987fd05c54ee4a1daeb888cc67ce1166fe8c9da0cdcc36361f7553f4b6667a830240675e845e0b123b1ef8a5630b3b5b84108ad55344a9d7d1773bdcbf31046b8b7780238bea7c305a73fb69b445774d2f71ea029bd108182803d9326a1f51066521024052b9850ce79b3b2f2eeb481999d65426089fa3680fd35568e5010ba0121e37cf10c64ecc20843a26a09c5d5eefbb35a43061cd33b7adca63965d7dbfcedf6544'

class BlockchainTest(TestCase):
    def setUp(self):
        self.blockchain = Blockchain()

class BlockchainSetupTests(BlockchainTest):
    def test_init(self):
        self.assertEqual(self.blockchain.current_transactions, [])
        self.assertEqual(self.blockchain.peers, set())
        self.assertEqual(len(self.blockchain.chain), 1)

class BlockchainBlockTests(BlockchainTest):
    def test_add_block_with_prev_hash_provided(self):
        result = self.blockchain.add_block(10, 20)
        block_dict = {
            'index': 2,
            'timestamp': self.blockchain.last_block.timestamp,
            'transactions': [],
            'proof': 10,
            'prev_hash': 20
        }
        self.assertEqual(result, block_dict)

    def test_add_block_with_no_prev_hash_provided(self):
        result = self.blockchain.add_block(10)
        block_dict = {
            'index': 2,
            'timestamp': self.blockchain.last_block.timestamp,
            'transactions': [],
            'proof': 10,
            'prev_hash': self.blockchain.chain[0].hash
        }
        self.assertEqual(result, block_dict)

    def test_last_block_points_to_end(self):
        self.assertEqual(self.blockchain.last_block, 
            self.blockchain.chain[0])

        self.blockchain.add_block(10, 20)

        self.assertEqual(self.blockchain.last_block, 
            self.blockchain.chain[1])

class BlockchainTransactionTests(BlockchainTest):
    def test_add_miner_transaction(self):
        result = self.blockchain.add_transaction(constant.MINER_KEY, 
            'receiver', 3, PRIVATE_KEY)
        self.assertEqual(result, 2)

    def test_add_regular_transaction_with_valid_private_key_succeeds(self):
        result = self.blockchain.add_transaction(PUBLIC_KEY, 'receiver', 3,
            PRIVATE_KEY)
        self.assertEqual(result, 2)

    def test_add_regular_transaction_with_invalid_private_key_fails(self):
        result = self.blockchain.add_transaction(PUBLIC_KEY, 'receiver', 3,
            PUBLIC_KEY)
        self.assertEqual(result, -1)

class BlockchainPeerTests(BlockchainTest):
    def test_add_peer_succeeds(self):
        result1 = self.blockchain.add_peer('http://127.0.0.1:9000')
        result2 = self.blockchain.add_peer('http://127.0.0.1:9001')

        self.assertTrue(result1)
        self.assertTrue(result2)

        self.assertIn('127.0.0.1:9000', self.blockchain.peers)
        self.assertIn('127.0.0.1:9001', self.blockchain.peers)

    def test_add_peer_fails(self):
        result = self.blockchain.add_peer('/127.0.0.1:9000')
        self.assertFalse(result)
        self.assertNotIn('127.0.0.1:9000', self.blockchain.peers)

    def test_peers_idempotent(self):
        self.assertEqual(len(self.blockchain.peers), 0)
        self.blockchain.add_peer('http://127.0.0.1:9000')

        self.assertEqual(len(self.blockchain.peers), 1)
        self.blockchain.add_peer('http://127.0.0.1:9000')

        self.assertEqual(len(self.blockchain.peers), 1)

class BlockchainProofTests(BlockchainTest):
    def test_proof_of_work(self):
        self.assertEqual(self.blockchain.proof_of_work(100), 33575)