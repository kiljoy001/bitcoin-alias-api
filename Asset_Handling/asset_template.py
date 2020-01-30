# import hashlib
# import base58
# import bcrypt
from bigchaindb_driver import BigchainDB
from settings import AppSettings
from .exceptions import InvalidAliasException


class Asset:
    """Creates, and transfer asset for BigChainDb consumption"""

    URL = AppSettings.get_settings()
    Bdb = BigchainDB(URL['bigchainurl'])

    def __init__(self, address, public_key, private_key, user_alias):
        self.address = address
        self.pub_key = public_key
        self.prv_key = private_key
        self.alias = user_alias
        self._bitcoin_address_asset_data = dict(data={
            'bitcoin_address': self.address
        })

    @property
    def asset_data(self):
        return self._bitcoin_address_asset_data

    @ asset_data.setter
    def asset_data(self, value):
        if value is not None:
            self._bitcoin_address_asset_data = value
        else:
            raise ValueError

    @staticmethod
    def transfer_asset(public_key: str, owners_private_key: str, transaction_id: str,
                       new_alias: str = None) -> None:
        # Update asset with new alias#
        creation_tx = Asset.Bdb.transactions.retrieve(transaction_id)
        asset_id = creation_tx['id']
        transfer_asset = {
            'id': asset_id
        }

        # Check if alias is being updated#
        if new_alias is None:
            metadata = creation_tx['metadata']
        else:
            metadata = {'alias_name': new_alias}

        # Transfer Data#
        output_index = 0
        output = creation_tx['outputs'][output_index]
        transfer_input = {
            'fulfillment': output['condition']['details'],
            'fulfills': {
                'output_index': output_index,
                'transaction_id': creation_tx['id'],
            },
            'owners_before': output['public_keys'],
        }

        prepared_transfer_tx = Asset.Bdb.transactions.prepare(
            operation='TRANSFER',
            asset=transfer_asset,
            inputs=transfer_input,
            recipients=public_key,
            metadata=metadata,
        )

        # Sign transaction#
        fulfilled_transfer_tx = Asset.Bdb.transactions.fulfill(
            prepared_transfer_tx,
            private_keys=owners_private_key
        )

        # Send to node#
        Asset.Bdb.transactions.send_commit(fulfilled_transfer_tx)

    def create_asset(self):
        # check alias uniqueness
        if len(self.Bdb.metadata.get(search=self.alias)) > 0:
            raise InvalidAliasException
        else:
            # Create an asset
            prepared_creation_tx = Asset.Bdb.transactions.prepare(
                operation='CREATE',
                signers=self.pub_key,
                asset=self._bitcoin_address_asset_data,
                metadata={'alias_name': self.alias}
            )

            # Sign transaction with private key
            signed_transaction = Asset.Bdb.transactions.fulfill(
                prepared_creation_tx,
                private_keys=self.prv_key
            )
            return signed_transaction

    def get_id_by_alias(self, alias):
        # get alias results
        search_result = Asset.Bdb.metadata.get(search=alias)
        # get transaction id
        return search_result[0]['id']


# class ApiUserAsset(Asset):
#     def __init__(self, username, password):
#         self.asset_data = {'data': {
#             'username': username,
#         }}
#         self.metadata = {'password': bcrypt.hashpw(password, bcrypt.gensalt())}
