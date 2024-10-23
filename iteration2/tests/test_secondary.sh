#!/bin/bash
#################################
# Test order of messages

curl http://127.0.0.1:8001/

# Add a first message with id = 0
curl --json '{"id": 0, "text":"message 0"}' --request POST http://127.0.0.1:8001

curl http://127.0.0.1:8001/

# Add a third message with id = 2
curl --json '{"id": 2, "text":"message 2"}' --request POST http://127.0.0.1:8001

curl http://127.0.0.1:8001/

# Add a second message with id = 1 and see all three messages
curl --json '{"id": 1, "text":"message 1"}' --request POST http://127.0.0.1:8001

curl http://127.0.0.1:8001/

#################################
# Test delay. Set sleep time to 10 seconds
curl --json '{"sleep": 10}' --request POST http://127.0.0.1:8001/sleep

# Add the fourth message with id = 3 and see 10 secconds delay
time curl --json '{"id": 3, "text": "message 3"}' --request POST http://127.0.0.1:8001

curl http://127.0.0.1:8001/

# Set sleep time to 10 seconds
curl --json '{"sleep": 0}' --request POST http://127.0.0.1:8001/sleep
