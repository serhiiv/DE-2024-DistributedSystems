#!/bin/bash
# View mesages on servers 

docker ps --format '@{{.Names}}${{.Ports}}' | sort | sed 's/@/echo \"/' | sed 's/\$/: $(curl -s /' | sed 's/->80\/tcp/\)"/' | bash 
