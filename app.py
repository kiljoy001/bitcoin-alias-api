import sys
from flask import Flask
from flask_restful import Api, Resource, reqparse
from bigchaindb_driver import BigchainDB
from .settings import AppSettings
from Asset_Handling.create_user import User
from Asset_Handling.asset_template import Asset
from Asset_Handling.exceptions import InvalidAliasException


app = Flask(__name__)
api = Api(app)
settings = AppSettings.get_settings()


class Query(Resource):

    def __init__(self):
        self.bdb = BigchainDB(settings['bigchainurl'])

    def get(self, alias):
        if len(self.bdb.metadata.get(alias)) > 0:
            return self.bdb.metadata.get(alias), 200
        else:
            return "No results", 404

    def post(self):
        try:
            parser = reqparse.RequestParser()
            parser.add_argument('alias')
            parser.add_argument('bitcoin_address')
            params = parser.parse_args()
            new_user = User()
            new_user.set_bitcoin_address_and_alias(params['alias'], params['bitcoin_address'])
            new_asset = Asset(new_user)
            transaction_id = new_asset.create_asset()
            keys = new_user.show_keys()
            json_return = {
                'txid': transaction_id,
                'public_key': keys[0],
                'private_key': keys[1]
            }
            return json_return, 201

        except ValueError:
            return "Value error", 400

        except InvalidAliasException:
            return "Alias already exists!", 400


    def update(self):
        try:
            parser = reqparse.RequestParser()
            parser.add_argument('public_key')
            parser.add_argument('private_key')
            parser.add_argument('current_alias')
            parser.add_argument('updated_alias')
            params = parser.parse_args()
            user_public_key = params['public_key']
            user_private_key = params['private_key']
            user_update = User()
            user_update.public_key = user_public_key
            user_update.private_key = user_private_key
            Asset.transfer_asset()

        except:
            pass
