from unittest import TestCase

from Crypto.PublicKey import RSA
from binascii import hexlify

from src.wallet import Wallet

class WalletTests(TestCase):
    def setUp(self):
        self.acct = Wallet(1)

    def test_init(self):
        self.assertEqual(self.acct.id, 1)
        self.assertEqual(len(str(self.acct.pri_key)), 48)
        self.assertEqual(len(str(self.acct.pub_key)), 32)

    def test_dict(self):
        wallet_dict = {
            'id': 1,
            'private_key': hexlify(
                self.acct.pri_key.exportKey(format='DER')).decode(),
            'public_key': hexlify(
                self.acct.pub_key.exportKey(format='DER')).decode()
        }

        self.assertEqual(self.acct.dict, wallet_dict)