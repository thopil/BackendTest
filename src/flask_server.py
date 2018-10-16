'''
Created on 15 Oct 2018

@author: thomaspilz
'''

#curl -vX POST http://localhost:5000/api/v1/slots -d @test_data_interviewer.json --header "Content-Type: application/json"
#curl -vX GET http://localhost:5000/api/v1/slots/all -d @test_data_candidate.json --header "Content-Type: application/json"

import json

import flask
from flask import request, jsonify
from storage_factory import StorageFactory
from roles.candidate import Candidate
from roles.interviewer import Interviewer

app = flask.Flask(__name__)
app.config["DEBUG"] = True

storage = StorageFactory('memory_storage').create_storage()

#-- GET

@app.route('/', methods=['GET'])
def home():
    return '''<h1>Slots API</h1>
    <p>Please send first POST request e.g. with cUrl<br />
    curl -vX POST http://localhost:5000/api/v1/slots -d @test_data_interviewer.json --header "Content-Type: application/json"
    </p><p>Then you could send a GET with <br />
    curl -vX GET http://localhost:5000/api/v1/slots/all -d @test_data_candidate.json --header "Content-Type: application/json"
    '''

@app.route('/api/v1/slots/all', methods=['GET'])
def api_slots_all():
    all_slots = []
    if request.json:
        interviewer = request.json.get('interviewer')
        candidate_json = request.json.get('candidate')
        candidate = Candidate(candidate_json.get('name'))
        candidate.set_requested_slots(candidate_json.get('slots'))
        result = storage.get_free_slots(candidate, *interviewer)
        if result is not None:
            all_slots = list(result)
    else:
        all_slots = list(storage.get_all_slots())
    return jsonify(all_slots)

@app.route('/api/v1/slots/<name>', methods=['GET'])
def api_slots_by_name(name):
    results = storage.get_slots_by_name(name)
    return jsonify(results)

#-- POST

@app.route('/api/v1/slots/<name>', methods=['POST'])
def api_set_slots_by_name():
    if not request.json or not 'slots' in request.json:
        return 'Error: No post data provided'

    slots = request.json.get('slots')
    name = request.json.get('name')
    interviewer = Interviewer(name)
    storage.set_slots_by_interviewer(interviewer, slots)
    return json.dumps({'success':True}), 200, {'ContentType':'application/json'}

@app.route('/api/v1/slots', methods=['POST'])
def api_set_slots():
    for name, slots in request.json.items():
        interviewer = Interviewer(name)
        storage.set_slots_by_interviewer(interviewer, slots)
    return json.dumps({'success':True}), 200, {'ContentType':'application/json'}

app.run()
