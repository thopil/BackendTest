#!/usr/bin/python3
# -*- coding: utf-8 -*-

'''
Created on 15 Oct 2018

@author: tp
'''

import json
import flask
from flask import request, jsonify

from src.storage.storage_factory import StorageFactory
from src.roles.candidate import Candidate
from src.roles.interviewer import Interviewer
from src.exceptions.bad_request import BadRequest

app = flask.Flask(__name__)
app.config["DEBUG"] = True

storage = StorageFactory('memory_storage').create_storage()

#-- GET

@app.route('/', methods=['GET'])
def home():
    return '''<h1>Slots API</h1>'''

@app.route('/api/v1/slots', methods=['GET'])
def api_slots_all():
    all_slots = []
    if request.json:
        interviewer = request.json.get('interviewer')
        candidate_json = request.json.get('candidate')
        if interviewer is None or candidate_json is None:
            raise BadRequest('Please check your json data', 400)
        candidate = Candidate(candidate_json.get('name'))
        candidate.set_requested_slots(candidate_json.get('slots'))
        result = storage.get_free_slots(candidate, *interviewer)
        if result is not None:
            all_slots = list(result)
        else:
            return json.dumps({'success': False,
                               'message': 'No slots for %s found' % interviewer}), 200, {'ContentType':'application/json'}
    else:
        all_slots = list(storage.get_all_slots())
    return jsonify(all_slots)

@app.route('/api/v1/slots_np', methods=['POST'])
def api_set_slots_all_np():
    if request.json:
        interviewers = request.json.get('interviewer')
        candidates = request.json.get('candidates')
        if interviewers is None or candidates is None:
            raise BadRequest('Please check your json data', 400)
        storage.set_free_slots_np(candidates, interviewers)
    return json.dumps({'success':True, 'message': 'Slots successfully set!'}), 200, {'ContentType':'application/json'}


@app.route('/api/v1/slots_np', methods=['GET'])
def api_slots_all_np():
    all_slots = []
    get_params = request.args.get
    if get_params:
        candidates = request.args.get('candidates')
        interviewers = request.args.get('interviewers')
        result = storage.get_free_slots_np(candidates, interviewers)
        if result is not None:
            all_slots = list(result)
        else:
            return json.dumps({'success': False,
                               'message': 'No slots for %s found' % interviewers.keys()}), 200, {'ContentType':'application/json'}
    else:
        all_slots = list(storage.get_all_slots())
    return jsonify(all_slots)

@app.route('/api/v1/slots/<name>', methods=['GET'])
def api_slots_by_name(name):
    results = storage.get_slots_by_name(name)
    return jsonify(results)

@app.route('/api/v1/interviewer', methods=['GET'])
def api_interviewer_all():
    results = storage.get_interviewer()
    return jsonify(results)

#-- DELETE

@app.route('/api/v1/interviewer/<name>', methods=['DELETE'])
def api_delete_by_interviewer(name):
    success = storage.del_slots_by_interviewer(name)
    return jsonify({'success': success, 'message': 'deleted'})

#-- POST

@app.route('/api/v1/slots', methods=['POST'])
def api_set_slots():
    for name, slots in request.json.items():
        interviewer = Interviewer(name)
        storage.set_slots_by_interviewer(interviewer, slots)
    return json.dumps({'success':True, 'message': 'Slots successfully set!'}), 200, {'ContentType':'application/json'}

#-- PUT
@app.route('/api/v1/slots', methods=['PUT'])
def api_update_slots_by_name():
    success = False
    if request.json:
        for name, slots in request.json.items():
            success = storage.update_slots_by_interviewer(name, slots)
        return json.dumps({'success':success, 'message': 'Slots successfully updated!'}), 200, {'ContentType':'application/json'}
    return json.dumps({'success': success, 'message': 'No JSON data set!'}), 200, {'ContentType':'application/json'}

#-- error handling
@app.errorhandler(Exception)
def unhandled_exception(e):
    #app.logger.error('Unhandled Exception: %s', (e))
    return jsonify({'message': 'Internal Server Error: %s' % str(e)}), 500

@app.errorhandler(BadRequest)
def handle_bad_request(error):
    """Catch BadRequest exception globally, serialize into JSON, and respond with 400."""
    payload = dict(error.payload or ())
    payload['status'] = error.status
    payload['message'] = error.message
    return jsonify(payload), 400

@app.errorhandler(404)
def page_not_found(e):
    return jsonify({'message': '404 Not found'}), 404

if __name__ == '__main__':
    app.run()
