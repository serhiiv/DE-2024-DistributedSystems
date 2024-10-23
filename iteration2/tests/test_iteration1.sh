#!/bin/bash
# View mesages on servers 
curl http://127.0.0.1:8000

curl http://127.0.0.1:8001

curl http://127.0.0.1:8002

#################################
# Test add a "message 0" to master
curl --json '{"text":"message 0"}' --request POST http://127.0.0.1:8000

# View mesages on servers 
curl http://127.0.0.1:8000

curl http://127.0.0.1:8001

curl http://127.0.0.1:8002

#################################
# Try to add a "message 1" to master with sleep time to 10 seconds on secondary1
curl --json '{"sleep": 10}' --request POST http://127.0.0.1:8001/sleep
time curl --json '{"text":"message 1"}' --request POST http://127.0.0.1:8000

# View mesages on servers 
curl http://127.0.0.1:8000

curl http://127.0.0.1:8001

curl http://127.0.0.1:8002


#################################
# Try to add a "message 2" to master with sleep time to 10 seconds on secondary1 and secondary2
curl --json '{"sleep": 10}' --request POST http://127.0.0.1:8002/sleep
time curl --json '{"text":"message 2"}' --request POST http://127.0.0.1:8000

# View mesages on servers 
curl http://127.0.0.1:8000

curl http://127.0.0.1:8001

curl http://127.0.0.1:8002

#################################
# Add a "message 3" to master without sleeping
curl --json '{"sleep": 0}' --request POST http://127.0.0.1:8001/sleep
curl --json '{"sleep": 0}' --request POST http://127.0.0.1:8002/sleep
time curl --json '{"text":"message 3"}' --request POST http://127.0.0.1:8000

# View mesages on servers 
curl http://127.0.0.1:8000

curl http://127.0.0.1:8001

curl http://127.0.0.1:8002

