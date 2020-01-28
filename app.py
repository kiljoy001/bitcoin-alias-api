import sys
from flask import Flask
from flask_restful import Api, Resource, reqparse
from bigchaindb_driver import BigchainDB
from settings import AppSettings
from flask_jwt import JWT, jwt_required, current_identity

sys.path.append('./Asset_Handling/')
from Asset_Handling.exceptions import InvalidAliasException

app = Flask(__name__)
api = Api(app)
settings = AppSettings.get_settings()
app.secret_key = settings['secret_key']


class Query(Resource):
    BDB = BigchainDB(settings['bigchainurl'])

    # TODO: add jwt auth to this
    @jwt_required()
    def get(self):
        parser = reqparse.RequestParser()
        parser.add_argument('alias')
        params = parser.parse_args()

        if len(Query.BDB.metadata.get(search=params['alias'])) > 0:
            return {'alias': Query.BDB.metadata.get(params['alias'])}, 200
        else:
            return {'result': "No results found"}, 404

    def post(self):
        # TODO: create a test payload and use postman to test if it accepts signed transactions
        try:
            parser = reqparse.RequestParser()
            parser.add_argument('signed_transaction')
            params = parser.parse_args()
            transaction_id = Query.BDB.transactions.send_commit(params['signed_transaction'])
            return {'transaction_id': transaction_id['metadata']}, 201

        except ValueError:
            return {'result': "Value error"}, 400

        except InvalidAliasException:
            return {'result': "Alias already exists!"}, 400


api.add_resource(Query, '/Query')
if settings['debug_on'] == 'True':
    if __name__ == "__main__":
        app.run(debug=True)
else:
    if __name__ == "__main__":
        app.run(debug=False)
