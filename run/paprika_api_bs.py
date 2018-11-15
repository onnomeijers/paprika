from flask import Flask, request
from flask_restful import Resource, Api
from nl.oxyma.repositories.ScheduledEventRepository import ScheduledEventRepository
from nl.oxyma.repositories.LocationRepository import LocationRepository
from nl.oxyma.connectors.DatasourceBuilder import DatasourceBuilder
from gevent.wsgi import WSGIServer


app = Flask(__name__)
api = Api(app)


class ScheduledEvent(Resource):
    def get(self):
        return {"message": "ok"}

    def post(self):
        content = request.get_json(silent=True)
        hashcode = content['hashcode']
        paprika_ds = DatasourceBuilder.build('paprika-ds.json')
        scheduler = ScheduledEventRepository(paprika_ds)
        scheduled_event = scheduler.find_by_hashcode(hashcode)
        return scheduled_event, 200, \
                {'Access-Control-Allow-Origin': '*',
                 'Access-Control-Allow-Methods': 'POST,GET,OPTIONS',
                 'Access - Control - Max - Age' : 1000,
                 'Access-Control-Allow-Headers': 'origin, x-csrftoken, content-type, accept'}

    def options(self):
        return {'Result': 'Ok'}, 200, \
                {'Access-Control-Allow-Origin': '*',
                 'Access-Control-Allow-Methods': 'POST,GET,OPTIONS',
                 'Access - Control - Max - Age' : 1000,
                 'Access-Control-Allow-Headers': 'origin, x-csrftoken, content-type, accept'}


class Location(Resource):
    def post(self):
        content = request.get_json(silent=True)
        hashcode = content['hashcode']
        paprika_ds = DatasourceBuilder.build('paprika-ds.json')
        locator = LocationRepository(paprika_ds)
        location = locator.find_by_hashcode(hashcode)
        return location, 200, \
                {'Access-Control-Allow-Origin': '*',
                 'Access-Control-Allow-Methods': 'POST,GET,OPTIONS',
                 'Access - Control - Max - Age' : 1000,
                 'Access-Control-Allow-Headers': 'origin, x-csrftoken, content-type, accept'}

    def options(self):
        return {'Result': 'Ok'}, 200, \
                {'Access-Control-Allow-Origin': '*',
                 'Access-Control-Allow-Methods': 'POST,GET,OPTIONS',
                 'Access - Control - Max - Age' : 1000,
                 'Access-Control-Allow-Headers': 'origin, x-csrftoken, content-type, accept'}


class PostLocation(Resource):
    def post(self):
        print "request.get_data", request.get_data()
        content = request.get_json(silent=True)

        paprika_ds = DatasourceBuilder.build('paprika-ds.json')
        locator = LocationRepository(paprika_ds)
        locator.update(content)

        print "request.get_json", content
        return {'message': 'ok'}, 200, \
                {'Access-Control-Allow-Origin': '*',
                 'Access-Control-Allow-Methods': 'POST,GET,OPTIONS',
                 'Access - Control - Max - Age': 86400,
                 'Access-Control-Allow-Headers': 'origin, x-csrftoken, content-type, accept'}

    def options(self):
        return {'Result': 'Ok'}, 200, \
                {'Access-Control-Allow-Origin': '*',
                 'Access-Control-Allow-Methods': 'POST,GET,OPTIONS',
                 'Access - Control - Max - Age': 86400,
                 'Access-Control-Allow-Headers': 'origin, x-csrftoken, content-type, accept'}


api.add_resource(ScheduledEvent, '/event')
api.add_resource(Location, '/location')
api.add_resource(PostLocation, '/location/post')

if __name__ == '__main__':
    http_server = WSGIServer(('127.0.0.1', 5002), app)