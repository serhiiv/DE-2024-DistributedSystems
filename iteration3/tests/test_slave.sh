#!/bin/bash

# Add a first message with id = 0
time curl -s --json '{"id": 0, "text":"message 0"}' --request POST http://127.0.0.1:8001


curl -s http://127.0.0.1:8001/


# Test delay. 
# Set sleep time to 2 seconds
curl -s --json '{"time": 2}' --request POST http://127.0.0.1:8001/sleep


# Add the message with id = 1 and see 1 secconds delay
time curl -s --json '{"id": 1, "text": "message 1"}' --request POST http://127.0.0.1:8001


curl -s http://127.0.0.1:8001/


# Set sleep time to 0 seconds
curl -s --json '{"time": 0}' --request POST http://127.0.0.1:8001/sleep


# Add the message with id = 2 and see 0 secconds delay
time curl -s --json '{"id": 2, "text": "message 2"}' --request POST http://127.0.0.1:8001


curl -s http://127.0.0.1:8001/

