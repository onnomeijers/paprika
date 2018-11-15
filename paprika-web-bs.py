import json

from flask import Flask
from flask import render_template
from flask import request
from flask_restful import Resource, Api
from flask_restful import abort

from paprika.connectors.DatasourceBuilder import DatasourceBuilder
from paprika.connectors.ConnectorFactory import ConnectorFactory
from paprika.repositories.EventRepository import EventRepository
from paprika.repositories.HookRepository import HookRepository
from paprika.repositories.SessionRepository import SessionRepository
from paprika.repositories.UserRepository import UserRepository
from paprika.system.Traceback import Traceback

app = Flask(__name__)
api = Api(app)


@app.route('/', methods=['GET', 'POST'])
def index():
    paprika_ds = DatasourceBuilder.build('paprika-ds.json')
    connector = ConnectorFactory.create_connector(paprika_ds)
    event_repository = EventRepository(connector)
    events = event_repository.states()
    return render_template('index_bs.html', events=events)

class HookList(Resource):
    def post(self):
        logger = Logger(self)
        try:
            content = request.get_json(silent=True)
            logger.trace("", json.dumps(content))

            paprika = DatasourceBuilder.find('paprika-ds')
            session_repository = SessionRepository(paprika)
            session = session_repository.find_by_hashcode(content)

            if not session:
                abort(400, message='failed')

            hook_repository = HookRepository(paprika)
            hooks = hook_repository.list()
            logger.trace("", json.dumps(hooks))
            return hooks;
        except:
            result = Traceback.build()
            logger.fatal('', result['message'], result['backtrace'])
            abort(500, message='failed', reason=result['message'], backtrace=result['backtrace'])


class UserLogin(Resource):
    def options(self):
        logger = Logger(self)
        logger.trace('', 'options called.')

    def post(self):
        logger = Logger(self)
        try:
            content = request.get_json(silent=True)
            logger.trace("", json.dumps(content))

            paprika = DatasourceBuilder.find('paprika-ds')
            user_repository = UserRepository(paprika)
            result = user_repository.login(content['username'], content['password'])
            logger.trace("", str(result))
            return {"message": "ok", "session": result}
        except:
            result = Traceback.build()
            logger.fatal('', result['message'], result['backtrace'])
            abort(500, message='failed', reason=result['message'], backtrace=result['backtrace'])


api.add_resource(UserLogin, '/user/login')
api.add_resource(HookList, '/hook/list')


if __name__ == '__main__':
    app.run(debug=True, port=5001)

