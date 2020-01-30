from abc import ABC
from flask_testing import TestCase
from .bitcoin_address_format_checker import Checker
from .create_user import User
from settings import AppSettings
from bigchaindb_driver import BigchainDB
from .asset_template import Asset

app_settings = AppSettings.get_settings()


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
    BDB = BigchainDB(app_settings['bigchainurl'])

    def setUp(self):
        self.user1 = User('John Q. Public', '1AMb4wcaZ7wZDLJ8frgjX9UZwcXs2mWRW8')

    def test_user_properties(self):
        self.assertTrue(self.user1.Alias == 'John Q. Public')
        self.assertFalse(self.user1.BitcoinAddress == '1Ab4wcaZ7wZDLJ8rgjX9UZwcXs2mWRW8')
        self.assertFalse(self.user1.KeyPair is None)


class CreateAssetTests(TestCase, ABC):
    BDB = BigchainDB(app_settings['bigchainurl'])

    def setUp(self) -> None:
        self.user1 = User('John Q. Public', '1AMb4wcaZ7wZDLJ8frgjX9UZwcXs2mWRW8')
        self.user2 = User('Betty Anne Brown', '1AVz6VazARMTHgXpSQ3J2trTiAEWFikNT5')

    def test_asset_is_signed(self):
        # create asset
        asset = Asset(self.user1.BitcoinAddress, self.user1.KeyPair.public_key, self.user1.KeyPair.private_key,
                      self.user1.Alias)
        signed_asset = asset.create_asset()
        self.assertTrue(signed_asset is not None)
        self.assertTrue(len(signed_asset) > 0)

