'''
Created on 15 Oct 2018

@author: thomaspilz
'''

#curl --header "Content-Type: application/json" --request POST --data '{"name":"test_user","slots": [["2018-10-12 10:00:00", "2018-10-12 11:00:00"]]}' http://localhost:5000/api/v1/resources/slots
#curl -vX POST http://localhost:5000/api/v1/resources/slots -d @test_data_interviewer.json --header "Content-Type: application/json"
#curl -vX GET http://localhost:5000/api/v1/resources/slots/all -d @test_data_candidate.json --header "Content-Type: application/json"

import flask
from flask import request, jsonify
from storage_factory import StorageFactory
import json

app = flask.Flask(__name__)
app.config["DEBUG"] = True

storage = StorageFactory('memory_storage').create_storage()



@app.route('/', methods=['GET'])
def home():
    return '''<h1>Slots API</h1>'''


@app.route('/api/v1/resources/slots/all', methods=['GET'])
def api_slots_all():
    if request.json:
        result = storage.get_free_slots(request.json, 'Sarah', 'Philip')
        print(result)
        all_slots = list(result)
    else:
        all_slots = list(storage.get_all_slots())
    return jsonify(all_slots)


@app.route('/api/v1/resources/slots/<name>', methods=['GET'])
def api_slots_by_name(name):
    results = storage.get_slots_by_name(name)
    return jsonify(results)

@app.route('/api/v1/resources/slots/<name>', methods=['POST'])
def api_set_slots_by_name():
    if not request.json or not 'slots' in request.json:
        return 'Error: No post data provided'

    slots = request.json.get('slots')
    name = request.json.get('name')
    storage.set_slots_by_name(name, slots)
    return json.dumps({'success':True}), 200, {'ContentType':'application/json'}

@app.route('/api/v1/resources/slots', methods=['POST'])
def api_set_slots():
    for name, slots in request.json.items():
        storage.set_slots_by_name(name, slots)
    return json.dumps({'success':True}), 200, {'ContentType':'application/json'}

app.run()
