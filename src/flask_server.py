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
from exceptions.bad_request import BadRequest

app = flask.Flask(__name__)
app.config["DEBUG"] = True

storage = StorageFactory('memory_storage').create_storage()

#-- GET

@app.route('/', methods=['GET'])
def home():
    return '''<h1>Slots API</h1>'''

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
    if not results:
        raise BadRequest('Name of interviewer not found', 40001, { 'ext': 1 })
    return jsonify(results)

@app.route('/api/v1/interviewer/all', methods=['GET'])
def api_interviewer_all():
    results = storage.get_interviewer()
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

#-- error handling
@app.errorhandler(Exception)
def unhandled_exception(e):
    app.logger.error('Unhandled Exception: %s', (e))
    return {'message': 'Internal Server Error'}, 500

@app.errorhandler(BadRequest)
def handle_bad_request(error):
    """Catch BadRequest exception globally, serialize into JSON, and respond with 400."""
    payload = dict(error.payload or ())
    payload['status'] = error.status
    payload['message'] = error.message
    return jsonify(payload), 400

app.run()
