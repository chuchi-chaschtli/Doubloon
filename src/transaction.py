from binascii import unhexlify

from Crypto.Hash import SHA256
from Crypto.PublicKey.RSA import importKey
from Crypto.Signature.PKCS1_v1_5 import new

class Transaction(object):
    def __init__(self, sender, receiver, amount):
        self.sender = sender
        self.receiver = receiver
        self.amount = amount

    def verify_signature(self, signature):
        """
        Verifies the provided signature corresponds to the transaction 
        object signed by the public key.

        :param signature: <str> signature to verify
        :return: <bool> true if the verification succeeds, false otherwise
        """
        try:
            private_key = importKey(unhexlify(signature))
            public_key = importKey(unhexlify(self.sender))

            signer = new(private_key)
            verifier = new(public_key)

            digest = SHA256.new()
            digest.update(str(self.dict).encode('utf8'))
            sig = signer.sign(digest)

            return verifier.verify(digest, sig)
        except TypeError:
            return False

    @property
    def dict(self):
        return {
            'sender': self.sender,
            'receiver': self.receiver,
            'amount': self.amount
        }