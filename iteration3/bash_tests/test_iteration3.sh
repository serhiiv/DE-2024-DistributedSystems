#!/bin/bash
#############################
# Self-check acceptance test script:
# Start M + S1 + S2
# check messages on M:[], S1:[], S2:[]
# set delay time for S1 in 1 second
# set delay time for S2 in 3 seconds
# send (Msg0, w=1) - Ok, 0 sec.
# check messages on M:[Msg0], S1:[], S2:[]
# wait 2 sec/
# check messages on M:[Msg0], S1:[Msg0], S2:[]
# wait 2 sec/
# check messages on M:[Msg0], S1:[Msg0], S2:[Msg0]
# 
# send (Msg1, w=2) - Ok, 1 sec.
# check messages on M:[Msg0, Msg1], S1:[Msg0, Msg1], S2:[Msg0]
# wait 3 sec/
# check messages on M:[Msg0, Msg1], S1:[Msg0, Msg1], S2:[Msg0, Msg1]
# 
# send (Msg2, w=3) - Ok, 3 sec.
# check messages on M:[Msg0, Msg1, Msg2], S1:[Msg0, Msg1, Msg2], S2:[Msg0, Msg1, Msg2]
# 
# set delay time for S1 in 3 seconds
# send (Msg3, w=1) - Ok, 0 sec.
# check messages on M:[Msg0, Msg1, Msg2, Msg3], S1:[Msg0, Msg1, Msg2], S2:[Msg0, Msg1, Msg2]
# 
# wait 1 sec/
# set delay time for S1 in 0 seconds
# set delay time for S2 in 0 seconds
# send (Msg4, w=3) - Ok, 0 sec.
# check messages on M:[Msg0, Msg1, Msg2, Msg3, Msg4], S1:[Msg0, Msg1, Msg2], S2:[Msg0, Msg1, Msg2]
# wait 3 sec/
# check messages on M:[Msg0, Msg1, Msg2, Msg3, Msg4], S1:[Msg0, Msg1, Msg2, Msg3, Msg4], S2:[Msg0, Msg1, Msg2, Msg3, Msg4]


# Step by step


# check messages on M:[], S1:[], S2:[]
docker ps --format '@{{.Names}}${{.Ports}}' | sort | sed 's/@/echo \"/' | sed 's/\$/: $(curl -s /' | sed 's/->8000\/tcp/ | tr -d "\n" \)"/' | bash

# set delay time for S1 in 1 second
curl -s --json '{"time": 1}' --request POST http://127.0.0.1:8001/sleep


# set delay time for S2 in 3 seconds
curl -s --json '{"time": 3}' --request POST http://127.0.0.1:8002/sleep


# send (Msg0, w=1) - Ok, 0 sec.
time curl -s --json '{"wc": 1, "text": "Msg0"}' --request POST http://127.0.0.1:8000


# check messages on M:[Msg0], S1:[], S2:[]
docker ps --format '@{{.Names}}${{.Ports}}' | sort | sed 's/@/echo \"/' | sed 's/\$/: $(curl -s /' | sed 's/->8000\/tcp/ | tr -d "\n" \)"/' | bash

# wait 2 sec/
sleep 2

# check messages on M:[Msg0], S1:[Msg0], S2:[]
docker ps --format '@{{.Names}}${{.Ports}}' | sort | sed 's/@/echo \"/' | sed 's/\$/: $(curl -s /' | sed 's/->8000\/tcp/ | tr -d "\n" \)"/' | bash

# wait 2 sec/
sleep 2

# check messages on M:[Msg0], S1:[Msg0], S2:[Msg0]
docker ps --format '@{{.Names}}${{.Ports}}' | sort | sed 's/@/echo \"/' | sed 's/\$/: $(curl -s /' | sed 's/->8000\/tcp/ | tr -d "\n" \)"/' | bash




# send (Msg1, w=2) - Ok, 1 sec.
time curl -s --json '{"wc": 2, "text": "Msg1"}' --request POST http://127.0.0.1:8000


# check messages on M:[Msg0, Msg1], S1:[Msg0, Msg1], S2:[Msg0]
docker ps --format '@{{.Names}}${{.Ports}}' | sort | sed 's/@/echo \"/' | sed 's/\$/: $(curl -s /' | sed 's/->8000\/tcp/ | tr -d "\n" \)"/' | bash

# wait 3 sec/
sleep 3

# check messages on M:[Msg0, Msg1], S1:[Msg0, Msg1], S2:[Msg0, Msg1]
docker ps --format '@{{.Names}}${{.Ports}}' | sort | sed 's/@/echo \"/' | sed 's/\$/: $(curl -s /' | sed 's/->8000\/tcp/ | tr -d "\n" \)"/' | bash



# send (Msg2, w=3) - Ok, 3 sec.
time curl -s --json '{"wc": 3, "text": "Msg2"}' --request POST http://127.0.0.1:8000


# check messages on M:[Msg0, Msg1, Msg2], S1:[Msg0, Msg1, Msg2], S2:[Msg0, Msg1, Msg2]
docker ps --format '@{{.Names}}${{.Ports}}' | sort | sed 's/@/echo \"/' | sed 's/\$/: $(curl -s /' | sed 's/->8000\/tcp/ | tr -d "\n" \)"/' | bash



# set delay time for S1 in 3 seconds
curl -s --json '{"time": 3}' --request POST http://127.0.0.1:8001/sleep


# send (Msg3, w=1) - Ok, 0 sec.
time curl -s --json '{"wc": 1, "text": "Msg3"}' --request POST http://127.0.0.1:8000


# check messages on M:[Msg0, Msg1, Msg2, Msg3], S1:[Msg0, Msg1, Msg2], S2:[Msg0, Msg1, Msg2]
docker ps --format '@{{.Names}}${{.Ports}}' | sort | sed 's/@/echo \"/' | sed 's/\$/: $(curl -s /' | sed 's/->8000\/tcp/ | tr -d "\n" \)"/' | bash



# wait 1 sec/
sleep 1

# set delay time for S1 in 0 seconds
curl -s --json '{"time": 0}' --request POST http://127.0.0.1:8001/sleep


# set delay time for S2 in 0 seconds
curl -s --json '{"time": 0}' --request POST http://127.0.0.1:8002/sleep


# send (Msg4, w=3) - Ok, 0 sec.
time curl -s --json '{"wc": 3, "text": "Msg4"}' --request POST http://127.0.0.1:8000


# check messages on M:[Msg0, Msg1, Msg2, Msg3, Msg4], S1:[Msg0, Msg1, Msg2], S2:[Msg0, Msg1, Msg2]
docker ps --format '@{{.Names}}${{.Ports}}' | sort | sed 's/@/echo \"/' | sed 's/\$/: $(curl -s /' | sed 's/->8000\/tcp/ | tr -d "\n" \)"/' | bash

# wait 3 sec/
sleep 3

# check messages on M:[Msg0, Msg1, Msg2, Msg3, Msg4], S1:[Msg0, Msg1, Msg2, Msg3, Msg4], S2:[Msg0, Msg1, Msg2, Msg3, Msg4]
docker ps --format '@{{.Names}}${{.Ports}}' | sort | sed 's/@/echo \"/' | sed 's/\$/: $(curl -s /' | sed 's/->8000\/tcp/ | tr -d "\n" \)"/' | bash
