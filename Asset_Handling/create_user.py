from bigchaindb_driver.crypto import generate_keypair
from .bitcoin_address_format_checker import Checker


class User:

    """
    Creates a user object that joins the alias and bitcoin address.
    """

    def __init__(self, alias):
        self.KeyPair = generate_keypair()
        self.BitcoinAddress = ''
        self.Alias = alias

    def generate_keys(self):
        # Create key pair if none exists
        if self.KeyPair is None:
            self.KeyPair = generate_keypair()
        else:
            pass

    def show_keys(self):
        # shows keys for the user
        return [self.KeyPair.public_key, self.KeyPair.private_key]

    def set_keys(self, public_key, private_key):
        self.public_key = public_key
        self.private_key = private_key

    def set_bitcoin_address(self, bitcoin_address):
        # Set the bitcoin address and alias
        check_if_valid = Checker(bitcoin_address)
        if check_if_valid.check_address():
            self.BitcoinAddress = bitcoin_address
        else:
            return ValueError
