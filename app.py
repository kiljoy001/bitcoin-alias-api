import sys
from flask import Flask
from flask_restful import Api, Resource, reqparse
from bigchaindb_driver import BigchainDB
from settings import AppSettings

sys.path.append('./Asset_Handling/')
from Asset_Handling.exceptions import InvalidAliasException

app = Flask(__name__)
api = Api(app)
settings = AppSettings.get_settings()


class Query(Resource):
    BDB = BigchainDB(settings['bigchainurl'])

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
            json_return = {
                'txid': transaction_id['metadata'],
            }

            return json_return, 201

        except ValueError:
            # Todo: change to json
            return "Value error", 400

        except InvalidAliasException:
            # Todo: change to json
            return "Alias already exists!", 400

    # Todo: this method can be removed, since signed transactions are being accepted, no need to make a special endpoint
    def update(self):
        try:
            parser = reqparse.RequestParser()
            parser.add_argument('signed_transaction')
            params = parser.parse_args()
            Query.BDB.transactions.send_commit(params['signed_transaction'])

        except:
            return "Transaction error!", 400


# Todo: Warning: Silently ignoring app.run() because the application is run from the flask command line executable.  \
#  Consider putting app.run() behind an if __name__ == "__main__" guard to silence this warning.

# TODO: Change endpoint from root to /Query
api.add_resource(Query, '/')
if settings['debug_on'] == 'True':
    app.run(debug=True)
else:
    app.run(debug=False)
