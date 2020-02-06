from .bitcoin_address_format_checker import Checker


def test_good_address():
    chk = Checker('1AMb4wcaZ7wZDLJ8frgjX9UZwcXs2mWRW8')
    assert chk.check_address() is True


def test_bad_checksum_address():
    chk = Checker('12Mb4wcaZ7wZDLJ8frgjX9UZwcXs2mWRW6')
    assert chk.check_address() is False


def test_short_address():
    chk = Checker('1AMb4wcaZ7wZDLJ8')
    assert chk.check_address() is False


def test_long_address():
    chk = Checker('12Mb4wcaZ7wZDLJ8frgjX9UZwcXs2mWRW61AMb4wcaZ7wZDLJ8frgjX9UZwcXs2mWRW8')
    assert chk.check_address() is False

# class FormatCheckerTests(TestCase, ABC):
#     GOOD_ADDRESS = '1AMb4wcaZ7wZDLJ8frgjX9UZwcXs2mWRW8'
#     BAD_CHECKSUM = '12Mb4wcaZ7wZDLJ8frgjX9UZwcXs2mWRW6'
#     TOO_SHORT = '1AMb4wcaZ7wZDLJ8'
#     BLANK = ''
#
#     def __init__(self):
#         self.chk = Checker()
#
#     def test_good_address(self):
#         self.chk.update_address(FormatCheckerTests.GOOD_ADDRESS)
#         self.assertTrue(self.chk.check_address())
#
#     def test_bad_address(self):
#         self.chk.update_address(FormatCheckerTests.BAD_CHECKSUM)
#         self.assertFalse(self.chk.check_address())
#
#     def test_short_address(self):
#         self.chk.update_address(FormatCheckerTests.TOO_SHORT)
#         self.assertFalse(self.chk.check_address())
#
#     def test_blank_entry(self):
#         self.chk.update_address(FormatCheckerTests.BLANK)
#         self.assertFalse(self.chk.check_address())
#
#
# class CreateUserTests(TestCase, ABC):
#     BDB = BigchainDB(app_settings['bigchainurl'])
#
#     def setUp(self):
#         self.user1 = User('John Q. Public', '1AMb4wcaZ7wZDLJ8frgjX9UZwcXs2mWRW8')
#
#     def test_user_properties(self):
#         self.assertTrue(self.user1.Alias == 'John Q. Public')
#         self.assertFalse(self.user1.BitcoinAddress == '1Ab4wcaZ7wZDLJ8rgjX9UZwcXs2mWRW8')
#         self.assertFalse(self.user1.KeyPair is None)
#
#


# class CreateAssetTests(TestCase, ABC):
#
#     BDB = BigchainDB(app_settings['bigchainurl'])
#     PRIVATE_KEY = '855wuFfcwYnS3NqijD9z9yDiBreERpLkBudLyXiwR6K5'
#     PUBLIC_KEY = '5cDbUCR38avXsQoZmM5diVvn63epKEr6U9HGE236YkTL'
#
#     def setUp(self):
#         self.user1 = User('John Q. Public', '1AMb4wcaZ7wZDLJ8frgjX9UZwcXs2mWRW8')
#         self.user2 = User('Betty Anne Brown', '1AVz6VazARMTHgXpSQ3J2trTiAEWFikNT5')
#         self.user3 = User('Learn-Learn Fruit', '12cfBAvvMQjhgZS2XkxKhrQLCuSin8vkK8')
#
#     def test_asset_is_signed(self):
#         # create asset
#         asset = Asset(self.user1.BitcoinAddress, CreateAssetTests.PUBLIC_KEY, CreateAssetTests.PRIVATE_KEY,
#                       self.user1.Alias)
#         signed_asset = asset.create_asset()
#         self.assertTrue(signed_asset is not None)
#         self.assertTrue(len(signed_asset) > 0)
#
#     def test_asset_will_transfer(self):
#         asset = Asset(self.user1.BitcoinAddress, self.user1.KeyPair.public_key, self.user1.KeyPair.private_key,
#                       self.user1.Alias)
#         signed_asset = asset.create_asset()
#
#         # send asset
#         on_chain = CreateAssetTests.BDB.transactions.send_commit(signed_asset)
#         # first transfer
#         transfer1 = asset.transfer_asset(self.user2.KeyPair.public_key, self.user1.KeyPair.private_key,
#                                          asset.get_id_by_alias('John Q. Public'))
#         # send on chain (transfer1)
#         transfer_commit1 = CreateAssetTests.BDB.transactions.send_commit(transfer1)
#         transfer2 = asset.transfer_asset(self.user3.KeyPair.public_key, self.user2.KeyPair.private_key,
#                                          asset.get_id_by_alias('Betty Anne Brown'), 'kill the beat')
#         # send on chain (transfer2)
#         transfer_commit2 = CreateAssetTests.BDB.transactions.send_commit(transfer2)
#
#         # check signed asset is the same as on chain (transaction confirmation)
#         self.assertTrue(signed_asset == on_chain)
#         # check if transfer happened
#         self.assertTrue(transfer1 == transfer_commit1)
#         self.assertTrue(transfer2 == transfer_commit2)
#         # check if alias update works
#         self.assertTrue(asset.get_id_by_alias('kill the beat') == signed_asset['id'])
