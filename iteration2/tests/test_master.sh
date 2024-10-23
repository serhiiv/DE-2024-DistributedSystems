#!/bin/bash
#################################

curl http://127.0.0.1:8000/

# Add a first message
curl --json '{"text":"message 0"}' --request POST http://127.0.0.1:8000

curl http://127.0.0.1:8000/

# Add a second message
curl --json '{"text":"message 1"}' --request POST http://127.0.0.1:8000

curl http://127.0.0.1:8000/
