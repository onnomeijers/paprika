from flask import Flask
from flask import render_template
from flask import request
from flask import redirect
from flask import url_for
from paprika.connectors.DatasourceBuilder import DatasourceBuilder
from paprika.connectors.ConnectorFactory import ConnectorFactory
from paprika.repositories.FileRepository import FileRepository
from paprika.repositories.EventRepository import EventRepository
from paprika.repositories.ScheduledEventRepository import ScheduledEventRepository
from paprika.repositories.LocationRepository import LocationRepository

app = Flask(__name__)

@app.route('/')
def index():
    paprika_ds = DatasourceBuilder.build('paprika-ds.json')
    connector = ConnectorFactory.create_connector(paprika_ds)
    event_repository = EventRepository(connector)
    events = event_repository.states()
    connector.close()
    return render_template('index.html', events=events)



@app.route('/schedular')
def show_scheduled_events():
    paprika = DatasourceBuilder.build('paprika-ds.json')
    schedular = ScheduledEventRepository(paprika)
    scheduled_events = schedular.list_all()
    repetitions = [{"name": "HOURS"}, {"name": "MINUTES"}, {"name": "DAYS"}]
    event = {"repetition": "DAYS", "intermission": "1", "url": "", "expected": "", "datasource": "", "db_call": "", "type": "add"}
    return render_template('schedular.html', repetitions=repetitions, scheduled_events=scheduled_events, event=event)


@app.route('/schedular/persist', methods=['POST'])
def persist_scheduled_event():
    method = request.form['submit']

    message = {}
    message['repetition'] = request.form['repetition']
    message['intermission'] = request.form['intermission']
    message['url'] = request.form['url']
    message['expected'] = request.form['expected']
    message['datasource'] = request.form['datasource']
    message['db_call'] = request.form['db_call']
    message['hashcode'] = request.form['hashcode']

    if method == 'add':
        paprika = DatasourceBuilder.build('paprika-ds.json')
        schedular = ScheduledEventRepository(paprika)
        schedular.insert(message)

    if method == 'update':
        paprika = DatasourceBuilder.build('paprika-ds.json')
        schedular = ScheduledEventRepository(paprika)
        schedular.update(message)

    return redirect(url_for('show_scheduled_events'))


@app.route('/schedular/edit')
def edit_scheduled_event():
    hashcode = request.args.get('hashcode', '')
    paprika = DatasourceBuilder.build('paprika-ds.json')
    schedular = ScheduledEventRepository(paprika)

    event = schedular.find_by_hashcode(hashcode)[0]
    event['type'] = 'update'
    repetitions = [{"name": "HOURS"}, {"name": "MINUTES"}, {"name": "DAYS"}]
    scheduled_events = schedular.list_all()
    return render_template('schedular.html', repetitions=repetitions, scheduled_events=scheduled_events, event=event)


@app.route('/schedular/hold', methods=['GET'])
def hold_scheduled_event():
    message={}
    message['id'] = request.args.get('id', '')
    message['active'] = 0
    paprika = DatasourceBuilder.build('paprika-ds.json')
    schedular = ScheduledEventRepository(paprika)
    schedular.hold(message)
    return redirect(url_for('show_scheduled_events'))


@app.route('/schedular/release', methods=['GET'])
def release_scheduled_event():
    message={}
    message['id'] = request.args.get('id', '')
    message['active'] = 1
    paprika = DatasourceBuilder.build('paprika-ds.json')
    schedular = ScheduledEventRepository(paprika)
    schedular.hold(message)
    return redirect(url_for('show_scheduled_events'))


@app.route('/schedular/delete', methods=['GET'])
def delete_scheduled_event():
    message={}
    message['id'] = request.args.get('id', '')
    paprika = DatasourceBuilder.build('paprika-ds.json')
    schedular = ScheduledEventRepository(paprika)
    schedular.delete(message)
    return redirect(url_for('show_scheduled_events'))


@app.route('/scanner')
def show_locations():
    paprika = DatasourceBuilder.build('paprika-ds.json')
    locator = LocationRepository(paprika)
    locations = locator.list_all()
    location = {"url": "", "patterns": "", "recursive": "0", "depth": "-1", "type": "add"}
    return render_template('scanner.html', locations=locations, location=location)


@app.route('/scanner/hold', methods=['GET'])
def hold_location():
    message={}
    message['hashcode'] = request.args.get('hashcode', '')
    message['active'] = 0
    paprika = DatasourceBuilder.build('paprika-ds.json')
    locator = LocationRepository(paprika)
    locator.hold(message)
    return redirect(url_for('show_locations'))


@app.route('/scanner/release', methods=['GET'])
def release_location():
    message={}
    message['hashcode'] = request.args.get('hashcode', '')
    message['active'] = 1
    paprika = DatasourceBuilder.build('paprika-ds.json')
    locator = LocationRepository(paprika)
    locator.hold(message)
    return redirect(url_for('show_locations'))


@app.route('/scanner/delete', methods=['GET'])
def delete_location():
    message={}
    message['hashcode'] = request.args.get('hashcode', '')
    paprika = DatasourceBuilder.build('paprika-ds.json')
    locator = LocationRepository(paprika)
    locator.delete(message)
    return redirect(url_for('show_locations'))


@app.route('/scanner/edit')
def edit_location():
    hashcode = request.args.get('hashcode', '')
    paprika = DatasourceBuilder.build('paprika-ds.json')
    locator = LocationRepository(paprika)

    location = locator.find_by_hashcode(hashcode)[0]
    location['type'] = 'update'

    locations = locator.list_all()
    return render_template('scanner.html', locations=locations, location=location)


@app.route('/scanner/persist', methods=['POST'])
def persist_location():
    method = request.form['submit']

    message = {}
    message['url'] = request.form['url']
    message['patterns'] = request.form['patterns']
    message['recursive'] = request.form['recursive']
    message['depth'] = request.form['depth']
    message['hashcode'] = request.form['hashcode']

    if method == 'add':
        paprika = DatasourceBuilder.build('paprika-ds.json')
        locator = LocationRepository(paprika)
        locator.insert(message)

    if method == 'update':
        paprika = DatasourceBuilder.build('paprika-ds.json')
        locator = LocationRepository(paprika)
        locator.update(message)

    return redirect(url_for('show_locations'))


@app.route('/files')
def show_files():
    paprika = DatasourceBuilder.build('paprika-ds.json')
    registry = FileRepository(paprika)
    files = registry.list()
    return render_template('files.html', files=files)


@app.route('/events')
def show_events():
    paprika = DatasourceBuilder.build('paprika-ds.json')
    event_repository = EventRepository(paprika)
    events = event_repository.list()
    return render_template('events.html', events=events)


if __name__ == '__main__':
    app.run(debug=True, port=5001)
