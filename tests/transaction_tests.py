from unittest import TestCase

import Crypto.Random
from Crypto.PublicKey import RSA
from binascii import hexlify

from transaction import Transaction

PUBLIC_KEY = '30819f300d06092a864886f70d010101050003818d0030818902818100d99c9347b6ecd418b1df48012201c5bd2869a707e45dee91a5c63027dc8020210aa4cf6e34e81fc200f29c893add94fefbf37594a964641fc52f8905280c4d93457d4cee5fb216a09a9e8688c62e26bc9e962357c019c5e6c73818f155b87ccaa70059cfa0698c85f5d982bef73bc84e6dfac540cf4f43308b799b8439c1011d0203010001'
PRIVATE_KEY = '3082025b02010002818100d99c9347b6ecd418b1df48012201c5bd2869a707e45dee91a5c63027dc8020210aa4cf6e34e81fc200f29c893add94fefbf37594a964641fc52f8905280c4d93457d4cee5fb216a09a9e8688c62e26bc9e962357c019c5e6c73818f155b87ccaa70059cfa0698c85f5d982bef73bc84e6dfac540cf4f43308b799b8439c1011d02030100010281802b55c5f2a317f888ce6b33909e30122bc02f8206cd507360e7cd56eba93a8eab65ce3a4cad1688b47eb1d1c0764b880f5b273984185398a8c700d75d828328b34bffe18565d9145a0db7aef152a9452642acc0518ccfa224287ba38fabb93a51f0da4db17b82a0ca12b6b69ff1c7b172061ce60ae9665b064ee21490e5cd0215024100db115ac3a95d00bdeabb429f841100d2786ab0849753eed0e0208020e8fe2e5d7e171d69d7552a9adee2840e846e56a6b1452c3a7b7c330f02595b3479f815cf024100fe4c5fe8c71d1e746d83b9bd9021d1fd6027090382321421f432ffabc713fca58cf1d116108e493a7b98854be96c761300a891f281db40ffdb9edc09cb29e15302404ca9f3209c299ef3d7acb6f10a0fc540e2c13b8afb46754205dd79d98a90417b987fd05c54ee4a1daeb888cc67ce1166fe8c9da0cdcc36361f7553f4b6667a830240675e845e0b123b1ef8a5630b3b5b84108ad55344a9d7d1773bdcbf31046b8b7780238bea7c305a73fb69b445774d2f71ea029bd108182803d9326a1f51066521024052b9850ce79b3b2f2eeb481999d65426089fa3680fd35568e5010ba0121e37cf10c64ecc20843a26a09c5d5eefbb35a43061cd33b7adca63965d7dbfcedf6544'

class TransactionTests(TestCase):
    def setUp(self):
        self.transaction = Transaction(PUBLIC_KEY, 'receiver', 5)

    def test_init(self):
        self.assertEqual(self.transaction.sender, PUBLIC_KEY)
        self.assertEqual(self.transaction.receiver, 'receiver')
        self.assertEqual(self.transaction.amount, 5)

    def test_dict(self):
        transaction_dict = {
            'sender': PUBLIC_KEY,
            'receiver': 'receiver',
            'amount': 5
        }
        self.assertEqual(self.transaction.dict, transaction_dict)

    def test_verify_sig_passes(self):
        self.assertTrue(self.transaction.verify_signature(PRIVATE_KEY))

    def test_verify_sig_fails(self):
        rng = Crypto.Random.new().read
        priv_key = RSA.generate(1024, rng)
        rand_private_key = hexlify(priv_key.exportKey(format='DER')).decode(
            'utf8')

        self.assertFalse(self.transaction.verify_signature(rand_private_key))