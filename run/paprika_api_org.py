from flask import Flask, request
from flask_restful import Resource, Api
from flask_restful import abort
from nl.oxyma.connectors.DatasourceBuilder import DatasourceBuilder
from nl.oxyma.repositories.EventRepository import EventRepository
from nl.oxyma.api.FileScheduledMonitor import FileScheduledMonitor
from nl.oxyma.api.EventScheduledMonitor import EventScheduledMonitor
from nl.oxyma.api.FileUnzip import FileUnzip
from nl.oxyma.api.OracleImport import OracleImport
from nl.oxyma.api.OracleExport import OracleExport
from nl.oxyma.api.FileCopy import FileCopy
from nl.oxyma.api.CalendarAdd import CalendarAdd
from nl.oxyma.api.SilverpopMailing import SilverpopMailing
from nl.oxyma.api.FileOracleSchedule import FileOracleSchedule
from nl.oxyma.api.FileOracleImport import FileOracleImport
from nl.oxyma.api.FileWaitMonitor import FileWaitMonitor
from nl.oxyma.api.Clang.ClangGroupSizes import ClangGroupsizes
from nl.oxyma.api.Clang.ClangMailSummaries import ClangMailSummaries
from nl.oxyma.messaging.Message import Message


import sys
import traceback

app = Flask(__name__)
api = Api(app)


class PostStream(Resource):
    def post(self):
        try:
            content = request.get_json(silent=True)
            paprika_ds = DatasourceBuilder.build('paprika-ds.json')

            Message.enqueue(payload,'streamer', 'nl.oxyma.consumers.')

        except:
            result = Traceback.build()
            abort(500, state='FAILED', message=result['message'], backtrace=result['backtrace'])


class EventList(Resource):
    def post(self):

        try:
            content = request.get_json(silent=True)

            paprika_ds = DatasourceBuilder.build('paprika-ds.json')
            repository = EventRepository(paprika_ds)
            event = repository.get_by_hashcode(content['hashcode'])

            event['state'] = 'PROCESSING'
            repository.state(event)

            events = repository.list()

            event['state'] = 'PROCESSED'
            repository.state(event)

            repository.close()
            return events
        except:
            type_, value_, traceback_ = sys.exc_info()
            ex = traceback.format_exception(type_, value_, traceback_)
            print ex


api.add_resource(EventList, '/event')
api.add_resource(CalendarAdd, '/calendar/add')
api.add_resource(SilverpopMailing, '/silverpop/mailing')
api.add_resource(OracleImport, '/oracle/import')
api.add_resource(OracleExport, '/oracle/export')
api.add_resource(FileWaitMonitor, '/monitor/file/wait')
api.add_resource(FileScheduledMonitor, '/monitor/file/scheduled')
api.add_resource(EventScheduledMonitor, '/monitor/event/scheduled')
api.add_resource(FileCopy, '/file/copy')
api.add_resource(FileUnzip, '/file/unzip')
api.add_resource(FileOracleSchedule, '/file/oracle/schedule')
api.add_resource(FileOracleImport, '/file/oracle/import')
api.add_resource(ClangGroupsizes, '/clang/groupsizes')
api.add_resource(ClangMailSummaries, '/clang/mailsummaries')

if __name__ == '__main__':
    app.run(debug=True, threaded=True)
