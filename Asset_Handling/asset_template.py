import hashlib
import base58
from bigchaindb_driver import BigchainDB
from .create_user import User
from ..settings import AppSettings
from .exceptions import InvalidAliasException


class Asset:
    """Creates, and transfer asset for BigChainDb consumption"""

    URL = AppSettings.get_settings()
    Bdb = BigchainDB(URL['bigchainurl'])

    def __init__(self, user):
        self.User = user
        self.Asset_Hash = None
        self.bitcoin_address_asset_data = dict(data={
            'asset_hash': self.get_hash(),
            'bitcoin_address': self.User.BitcoinAddress
        })

    def get_hash(self):
        data = self.User.BitcoinAddress + self.User.Alias
        blake_hash = hashlib.blake2b(data.encode()).hexdigest()
        return base58.b58encode(blake_hash).decode()

    @staticmethod
    def transfer_asset(public_key: User, owners_private_key: User, transaction_id: str,
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
            metadata = {'updated_alias': new_alias}

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
        if len(self.Bdb.metadata.get(search=self.User.Alias)) > 0:
            raise InvalidAliasException
        else:
            # Prepare blake2b hash property#
            self.Asset_Hash = self.get_hash()

            # Create an asset
            prepared_creation_tx = Asset.Bdb.transactions.prepare(
                operation='CREATE',
                signers=self.User.KeyPair.public_key,
                asset=self.bitcoin_address_asset_data,
                metadata={'updated_alias': self.User.Alias}
            )

            # Sign transaction with private key
            signed_transaction = Asset.Bdb.transactions.fulfill(
                prepared_creation_tx,
                private_keys=self.User.KeyPair.private_key
            )

            # Send transaction to BigchainDb node
            sent_token = Asset.Bdb.transactions.send_commit(signed_transaction)

            # Return TxId
            return sent_token['id']

    @staticmethod
    def get_id_by_alias(alias):
        # get alias results
        search_result = Asset.Bdb.metadata.get(search=alias)
        # get transaction id
        transaction_id = search_result[0]['id']
        if len(transaction_id) > 0:
            return transaction_id
        else:
            raise InvalidAliasException
