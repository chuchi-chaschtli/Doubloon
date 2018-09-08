import Crypto.Random
from Crypto.PublicKey import RSA
from binascii import hexlify

class Wallet(object):
    def __init__(self, id):
        self.id = id

        rng = Crypto.Random.new().read
        self.pri_key = RSA.generate(1024, rng)
        self.pub_key = self.pri_key.publickey()

    @property
    def dict(self):
        """
        Grabs a json-friendly representation of the wallet

        :return: <dict> for the wallet
        """
        return {
            'id': self.id,
            'private_key': self.__key_string(self.pri_key),
            'public_key': self.__key_string(self.pub_key)
        }

    def __key_string(self, key):
        """
        Grabs the decoded RSA key.

        :param key: <key> the RSA key
        :return: <str> the decoded hexlified string.
        """
        return hexlify(key.exportKey(format='DER')).decode()