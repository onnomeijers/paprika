from flask import Flask, request
from flask_restful import Resource, Api
from flask_restful import abort
from gevent.wsgi import WSGIServer
from paprika.system.logger.Logger import Logger
from paprika.connectors.DatasourceBuilder import DatasourceBuilder
from paprika.connectors.ConnectorFactory import ConnectorFactory
from paprika.system.Traceback import Traceback

app = Flask(__name__)
api = Api(app)


class UserLogin(Resource):
    def options(self):
        logger = Logger(self)
        logger.trace("", "options called.")

    def post(self):
        paprika_ds = DatasourceBuilder.build('paprika-ds.json')
        connector = ConnectorFactory.create_connector(paprika_ds)
        logger = Logger(self, connector)
        try:
            content = request.get_json(silent=True)
            print content
            return {"message": "ok"}
        except:
            result = Traceback.build()
            print "error"
            abort(500, message='failed', reason=result['message'], backtrace=result['backtrace'])


api.add_resource(UserLogin, '/user/login')


if __name__ == '__main__':
    http_server = WSGIServer(('0.0.0.0', 5002), app)
    http_server.serve_forever()