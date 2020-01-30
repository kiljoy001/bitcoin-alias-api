from bigchaindb_driver.crypto import generate_keypair
from .bitcoin_address_format_checker import Checker


class User:
    """
    Creates a user object that joins the alias and bitcoin address.
    """

    def __init__(self, alias, bitcoin_address):
        self.KeyPair = generate_keypair()
        self.BitcoinAddress = User.check_bitcoin_address(bitcoin_address)
        self.Alias = alias

    @classmethod
    def check_bitcoin_address(cls, bitcoin_address):
        check_if_valid = Checker(bitcoin_address)
        if check_if_valid.check_address():
            return bitcoin_address
        else:
            # sound the alarm, the address is flawed
            raise ValueError
