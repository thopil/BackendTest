# Backend Challenge

This API provides a simple interface to find intersections of available
time slots between candidates and interviewers.

Currently it handles only JSON requests and responses which are based
on different storage engines, like memory-based or a database wrapper.

## Getting started

These instructions will get you a copy of the project up and running on your local machine
for development and testing purposes.

### Installing
1. install python3 and virtualenv
2. eventually upgrade virtualenv:
    pip install --upgrade virtualenv
3. create virtualenv with:
    virtualenv -p python3 <env_name>
4. activate virtualenv:
    source <env_name>/bin/activate
5. install additional packages:
    pip install -r requirements.txt
5. start API server which listens on http://localhost:5000 -
    python3 flask_server.py
6. send available slots of interviewers, e.g. from testfile in src-folder:
    curl -vX POST http://localhost:5000/api/v1/slots -d @test_data_interviewer.json --header "Content-Type: application/json"
7. send candidate request including his time slots to API. The API will respond with the commom time slots of
   available interviewers:
    curl -vX GET http://localhost:5000/api/v1/slots/all -d @test_data_candidate.json --header "Content-Type: application/json"
8. to get a better overview how the request structs are built, feel free to run the tests

## License

This project is licensed under the MIT License - see the [LICENSE.md](LICENSE.md) file for details
