#!/bin/bash

# Download Ergo node if not present
if [ ! -f "ergo-5.0.14.jar" ]; then
    echo "Downloading Ergo node..."
    wget https://github.com/ergoplatform/ergo/releases/download/v5.0.14/ergo-5.0.14.jar
fi

# Create config directory
mkdir -p config

# Generate configurations for all nodes
python3 generate_configs.py 6

# Create data directories for each node
for i in $(seq 1 6); do
    mkdir -p .ergo-$i
done

# Start all nodes
docker-compose -f docker-compose-multi.yml up -d

echo "All Ergo nodes have been started!"
echo "Access the nodes at:"
echo "Node 1: http://localhost:9100"
echo "Node 2: http://localhost:9101"
echo "Node 3: http://localhost:9102"
echo "Node 4: http://localhost:9103"
echo "Node 5: http://localhost:9104"
echo "Node 6: http://localhost:9105"

echo ""
echo "API keys can be found in the config directory:"
echo "config/ergo-*.api.key"
