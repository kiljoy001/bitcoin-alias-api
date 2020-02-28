import bigchaindb_driver
import settings
from . import exceptions


class Asset:
    """Creates, and transfer asset for BigChainDb consumption"""

    URL = settings.AppSettings.get_settings()
    Bdb = bigchaindb_driver.BigchainDB(URL['localhost'])

    def __init__(self, address, public_key, private_key, user_alias):
        self.address = address
        self.pub_key = public_key
        self.prv_key = private_key

        if user_alias == '':
            raise ValueError
        else:
            self.alias = user_alias

        self.alias = user_alias
        self._bitcoin_address_asset_data = dict(data={
            'bitcoin_address': self.address
        })

    @property
    def asset_data(self):
        return self._bitcoin_address_asset_data

    @asset_data.setter
    def asset_data(self, value):
        if value is not None:
            self._bitcoin_address_asset_data = value
        else:
            raise ValueError

    @staticmethod
    def transfer_asset(sending_to_public_key: str, owners_private_key: str, transaction_id: str,
                       new_alias: str = None) -> str:
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
            recipients=sending_to_public_key,
            metadata=metadata,
        )

        # Sign transaction#
        fulfilled_transfer_tx = Asset.Bdb.transactions.fulfill(
            prepared_transfer_tx,
            private_keys=owners_private_key
        )

        return fulfilled_transfer_tx

    def create_asset(self):
        # check alias uniqueness
        if len(self.Bdb.metadata.get(search=self.alias)) > 0:
            raise exceptions.InvalidAliasException
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
        return Asset.Bdb.metadata.get(search=alias)[0]
        # sanity check - should be only one result
        # if len(search_result) == 1:
        #     # get transaction id
        #     return search_result[0]['id']
        # elif len(search_result) == 0:
        #     return search_result
        # else:
        #     # raise hell
        #     raise DuplicateAliasException

    def get_bitcoin_address_by_alias(self, alias):
        # get transaction id from alias
        transaction_id = self.get_id_by_alias(alias)
        search_result = Asset.Bdb.transactions.get(asset_id=transaction_id, operation='CREATE')
        return search_result[0]['asset']['data']['bitcoin_address']

# class ApiUserAsset(Asset):
#     def __init__(self, username, password):
#         self.asset_data = {'data': {
#             'username': username,
#         }}
#         self.metadata = {'password': bcrypt.hashpw(password, bcrypt.gensalt())}
