from binascii import unhexlify

import Crypto
from Crypto.Hash import SHA256
from Crypto.PublicKey import RSA
from Crypto.Signature import PKCS1_v1_5

class Transaction(object):
    def __init__(self, sender, receiver, amount):
        self.sender = sender
        self.receiver = receiver
        self.amount = amount

    def to_dict(self):
        return {
            'sender': self.sender,
            'receiver': self.receiver,
            'amount': self.amount
        }

    def verify_signature(self, signature):
        """
        Verifies the provided signature corresponds to the transaction 
        object signed by the public key.

        :param signature: <str> signature to verify
        :return: <bool> true if the verification succeeds, false otherwise
        """
        private_key = RSA.importKey(unhexlify(signature))
        public_key = RSA.importKey(unhexlify(self.sender))

        signer = PKCS1_v1_5.new(private_key)
        verifier = PKCS1_v1_5.new(public_key)

        digest = SHA256.new()
        digest.update(str(self.to_dict()).encode('utf8'))
        sig = signer.sign(digest)

        return verifier.verify(digest, sig)