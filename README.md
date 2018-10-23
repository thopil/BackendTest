# Backend Challenge

This API provides a simple interface to find intersections of available
time slots between candidates and interviewers.

Currently it handles only JSON requests through the HTTP protocol and responses which are based
on different storage engines, like memory-based or a database wrapper.

## Getting started

These instructions will get you an overview of the project up and running on your local machine
for development and testing purposes.

Interviewers and his appropiate slots will be stored.
Candidates send a request including free slots and a list of interviewers.


### Installing
1. install python3 and virtualenv
2. eventually upgrade virtualenv:
```
    pip install --upgrade virtualenv
```
3. create virtualenv with:
```
    virtualenv -p python3 <env_name>
```
4. activate virtualenv:
```
    source <env_name>/bin/activate
```
5. install additional packages:
```
    pip install -r requirements.txt
```
5. start API server which listens on http://localhost:5000
```
    python3 src/flask_server.py
```
6. to get a better overview how the request structs are built, feel free to run the tests

### Usage (Complete flow)

A complete flow including all HTTP methods can be executed by (started server required)

```
./src/test/test_json_files/fixture.sh
```

### Usage (Naive approach)

1. http://localhost:5000/api/v1/interviewer
2. http://localhost:5000/api/v1/slots/interviewer_1
3. send available slots of interviewers, e.g. from testfiles in src/test/test_json_files:<br />
```
    curl -X POST http://localhost:5000/api/v1/slots -d @test_data_interviewer.json --header "Content-Type: application/json"
```
4. send candidate request including his time slots to API. The API will respond with the commom time slots of
   available interviewers:<br />
   ```
    curl -X GET http://localhost:5000/api/v1/slots -d @test_data_candidate_carl.json --header "Content-Type: application/json"
    ```
    or<br />
    ```
    curl -X GET http://localhost:5000/api/v1/slots -d @test_data_candidate_tom.json --header "Content-Type: application/json"
    ```

### Usage (Experimental approach)

Also an additional experimental approach with numpy was implemented.
Just send a POST request to the server by <br />
```
    curl -X GET http://localhost:5000/api/v1/slots_np -d @test_data_np.json --header "Content-Type: application/json"
```

### Structure of JSON requests

Datetime strings have to be in format "YYYY-mm-dd HH:MM:SS"
1. to POST new slots

```javascript
{ "interviewer_1": [["slot_start", "slot_end"], [...]],
  "interviewer_2": [[...]] }
```
2. GET available slots for a list of interviewer

```javascript
{ "interviewer": ["interviewer_1", "interviewer_2", ...],
  "candidate":{
      "name": "name",
      "slots": [["slot_start", "slot_end"], [...]]
  }
 }
```
## License

This project is licensed under the MIT License - see the [LICENSE.md](LICENSE.md) file for details
