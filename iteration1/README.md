## List o commands

Build image
`docker build -t serhii714/ds:iter2 .`

Deploy mode
`docker compose -d`

Developer mode
`docker compose -f dev_compose.yaml up`

Stop dockers
`docker compose down`

Set dalay for rl-slave-1
`docker exec rl-slave-1 tc qdisc add dev eth0 root netem delay 300ms`

Remove dalay for rl-slave-1
`docker exec rl-slave-1 tc qdisc del dev eth0 root`
