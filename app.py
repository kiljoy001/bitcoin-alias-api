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
        # TODO: Need to change this part to accept a signed transaction from the client. This setup is wrong / dangerous
        try:
            parser = reqparse.RequestParser()
            parser.add_argument('signed_transaction')
            params = parser.parse_args()
            transaction_id = self.bdb.transactions.send_commit(params['signed_transaction'])
            json_return = {
                'txid': transaction_id['metadata'],
            }

            return json_return, 201

        except ValueError:
            return "Value error", 400

        except InvalidAliasException:
            return "Alias already exists!", 400

    @property
    def update(self):
        try:
            parser = reqparse.RequestParser()
            parser.add_argument('signed_transaction')
            params = parser.parse_args()
            self.bdb.transactions.send_commit(params['signed_transaction'])

        except:
            return "Transaction error!", 400
