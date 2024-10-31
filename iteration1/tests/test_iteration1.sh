#!/bin/bash
# View mesages on servers
docker ps --format '@{{.Names}}${{.Ports}}' | sort | sed 's/@/echo \"/' | sed 's/\$/: $(curl -s /' | sed 's/->8000\/tcp/ | tr -d "\n" \)"/' | bash   

# Test add a "message 0" to master
time curl -s --json '{"text":"message 0"}' --request POST http://127.0.0.1:8000 | tr -d '\n'

# View mesages on servers
docker ps --format '@{{.Names}}${{.Ports}}' | sort | sed 's/@/echo \"/' | sed 's/\$/: $(curl -s /' | sed 's/->8000\/tcp/ | tr -d "\n" \)"/' | bash   

# make delay time to 1 seconds for rl-slave-1
docker exec rl-slave-1 tc qdisc add dev eth0 root netem delay 1000ms
# add a "message 1" to master
time curl -s --json '{"text":"message 1"}' --request POST http://127.0.0.1:8000 | tr -d '\n'

# make delay time to 1 seconds for rl-slave-2
docker exec rl-slave-2 tc qdisc add dev eth0 root netem delay 1000ms
# add a "message 2" to master
time curl -s --json '{"text":"message 2"}' --request POST http://127.0.0.1:8000 | tr -d '\n'

docker exec rl-slave-1 tc qdisc del dev eth0 root
docker exec rl-slave-2 tc qdisc del dev eth0 root

# View mesages on servers
docker ps --format '@{{.Names}}${{.Ports}}' | sort | sed 's/@/echo \"/' | sed 's/\$/: $(curl -s /' | sed 's/->8000\/tcp/ | tr -d "\n" \)"/' | bash   
