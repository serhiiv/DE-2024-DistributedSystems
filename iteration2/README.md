List o commands

docker build -t serhii714/ds:iter2 .

docker compose -f dev_compose.yaml up -d 

docker compose down

docker exec second-node-2 tc qdisc add dev eth0 root netem delay 300ms

docker exec second-node-2 tc qdisc del dev eth0 root


docker ps --format '{{.Ports}} {{.Names}}' | sort

curl -s 0.0.0.0:8000/secondaries | tr -d '\n' 