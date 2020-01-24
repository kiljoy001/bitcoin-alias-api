from abc import ABC
from flask_testing import TestCase
from .bitcoin_address_format_checker import Checker
from .create_user import User


class FormatCheckerTests(TestCase, ABC):
    GOOD_ADDRESS = '1AMb4wcaZ7wZDLJ8frgjX9UZwcXs2mWRW8'
    BAD_CHECKSUM = '12Mb4wcaZ7wZDLJ8frgjX9UZwcXs2mWRW6'
    TOO_SHORT = '1AMb4wcaZ7wZDLJ8'
    BLANK = ''

    def __init__(self):
        self.chk = Checker()

    def test_good_address(self):
        self.chk.update_address(FormatCheckerTests.GOOD_ADDRESS)
        self.assertTrue(self.chk.check_address())

    def test_bad_address(self):
        self.chk.update_address(FormatCheckerTests.BAD_CHECKSUM)
        self.assertFalse(self.chk.check_address())

    def test_short_address(self):
        self.chk.update_address(FormatCheckerTests.TOO_SHORT)
        self.assertFalse(self.chk.check_address())

    def test_blank_entry(self):
        self.chk.update_address(FormatCheckerTests.BLANK)
        self.assertFalse(self.chk.check_address())


class CreateUserTests(TestCase, ABC):

    def setUp(self):
        self.fresh_user = User()
        self.fresh_user.Alias = 'John Q. Public'
        self.fresh_user.BitcoinAddress = '1AMb4wcaZ7wZDLJ8frgjX9UZwcXs2mWRW8'
        self.fresh_user.KeyPair = self.fresh_user.generate_keys()

    def test_user_properties(self):
        self.assertTrue(self.fresh_user.Alias == 'John Q. Public')
        self.assertFalse(self.fresh_user.BitcoinAddress == '1Ab4wcaZ7wZDLJ8rgjX9UZwcXs2mWRW8')
        self.assertFalse(self.fresh_user.KeyPair is None)
