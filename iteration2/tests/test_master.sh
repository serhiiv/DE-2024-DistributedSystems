#!/bin/bash

# View mesages on servers
bash view_rl.sh

# Add a first message
curl --json '{"text":"message 0"}' --request POST http://127.0.0.1:8000

# View mesages on servers
bash view_rl.sh
