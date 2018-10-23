curl -X POST http://localhost:5000/api/v1/slots -d @test_data_interviewer.json --header "Content-Type: application/json"
sleep 1
curl -X GET http://localhost:5000/api/v1/slots -d @test_data_candidate_carl.json --header "Content-Type: application/json"
sleep 1
curl -X PUT http://localhost:5000/api/v1/slots -d @test_data_interviewer_update.json --header "Content-Type: application/json"
sleep 1
curl -X GET http://localhost:5000/api/v1/slots -d @test_data_candidate_carl.json --header "Content-Type: application/json"
sleep 1
curl -X GET http://localhost:5000/api/v1/interviewer
sleep 1
curl -X DELETE http://localhost:5000/api/v1/interviewer/Thomas
sleep 1
curl -X GET http://localhost:5000/api/v1/interviewer

