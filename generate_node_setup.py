#!/usr/bin/env python3
import os
import sys
import json
import hashlib
import random

def generate_docker_compose(num_nodes):
    """Generate docker-compose file for N nodes."""
    template = """version: '3'
services:
  ergo-node-1: &ergo-node-template
    image: bellsoft/liberica-openjdk-alpine
    restart: unless-stopped
    volumes:      
      - ./.ergo-1:/ergo/.ergo
      - ./config/ergo-1.conf:/app/ergo.conf
      - ./ergo-5.0.14.jar:/app/ergo.jar
    ports:
      - "9500:9053"
      - "9600:9030"
    working_dir: /app
    command: java -jar -Xmx2G ergo.jar --mainnet -c ergo.conf
"""
    
    # Add additional nodes
    for i in range(2, num_nodes + 1):
        node_config = f"""
  ergo-node-{i}:
    <<: *ergo-node-template
    volumes:      
      - ./.ergo-{i}:/ergo/.ergo
      - ./config/ergo-{i}.conf:/app/ergo.conf
      - ./ergo-5.0.14.jar:/app/ergo.jar
    ports:
      - "{9500 + i - 1}:9053"
      - "{9600 + i - 1}:9030"
"""
        template += node_config
    
    with open('docker-compose-multi.yml', 'w') as f:
        f.write(template)

def generate_setup_script(num_nodes):
    """Generate setup script for N nodes."""
    script = f"""#!/bin/bash

# Download Ergo node if not present
if [ ! -f "ergo-5.0.14.jar" ]; then
    echo "Downloading Ergo node..."
    wget https://github.com/ergoplatform/ergo/releases/download/v5.0.14/ergo-5.0.14.jar
fi

# Create config directory
mkdir -p config

# Generate configurations for all nodes
python3 generate_configs.py {num_nodes}

# Create data directories for each node
for i in $(seq 1 {num_nodes}); do
    mkdir -p .ergo-$i
done

# Start all nodes
docker-compose -f docker-compose-multi.yml up -d

echo "All Ergo nodes have been started!"
echo "Access the nodes at:"
"""
    
    # Add node access information
    for i in range(1, num_nodes + 1):
        script += f'echo "Node {i}: http://localhost:{9500 + i - 1}"\n'
    
    script += """
echo ""
echo "API keys can be found in the config directory:"
echo "config/ergo-*.api.key"
"""
    
    with open('setup-multi-node.sh', 'w') as f:
        f.write(script)
    os.chmod('setup-multi-node.sh', 0o755)  # Make executable

def modify_config_generator(num_nodes):
    """Generate the configuration generator script."""
    with open('generate_configs.py', 'w') as f:
        f.write('''#!/usr/bin/env python3
import os
import sys
import json
import hashlib
import random

BASE_CONFIG = """ergo {
  networkType = "mainnet"
  directory = "/ergo/.ergo"
  node {
    mining = false
    rebroadcastCount = 10000
    offlineGeneration = false
    maxTransactionCost = 4900000
    utxo {
      utxoBootstrap = false
      storingUtxoSnapshots = 2
      p2pUtxoSnapshots = 2
    }
    wallet.secretStorage.secretDir = ${ergo.directory}"/wallet/keystore"
  }
}
scorex {
  network {
    bindAddress = "0.0.0.0:9030"
    nodeName = "ergo-mainnet-node-NUMBER"
    knownPeers = [
      "213.239.193.208:9030",
      "159.65.11.55:9030",
      "165.227.26.175:9030",
      "159.89.116.15:9030",
      "136.244.110.145:9030",
      "94.130.108.35:9030",
      "51.75.147.1:9020",
      "221.165.214.185:9030",
      "217.182.197.196:9030",
      "173.212.220.9:9030",
      "176.9.65.58:9130",
      "213.152.106.56:9030"
    ]
    maxConnections = 500
  }
  restApi {
    apiKeyHash = "APIHASH"
    bindAddress = "0.0.0.0:9053"
  }
}"""

def generate_api_key():
    """Generate a random API key and its hash."""
    api_key = ''.join(random.choices('0123456789abcdef', k=64))
    api_hash = hashlib.sha256(api_key.encode()).hexdigest()
    return api_key, api_hash

def create_config_directory():
    """Create config directory if it doesn't exist."""
    os.makedirs('config', exist_ok=True)

def generate_node_config(node_number):
    """Generate configuration for a specific node."""
    api_key, api_hash = generate_api_key()
    
    # Create node-specific configuration
    config = BASE_CONFIG.replace('NUMBER', str(node_number))
    config = config.replace('APIHASH', api_hash)
    
    # Save configuration
    with open(f'config/ergo-{node_number}.conf', 'w') as f:
        f.write(config)
    
    # Save API key to a separate file
    with open(f'config/ergo-{node_number}.api.key', 'w') as f:
        f.write(api_key)

def main():
    """Generate configurations for N nodes."""
    if len(sys.argv) != 2:
        print("Usage: python3 generate_configs.py <number_of_nodes>")
        sys.exit(1)
    
    num_nodes = int(sys.argv[1])
    create_config_directory()
    for i in range(1, num_nodes + 1):
        generate_node_config(i)
        print(f"Generated configuration for node {i}")

if __name__ == "__main__":
    main()
''')
    os.chmod('generate_configs.py', 0o755)  # Make executable

def main():
    if len(sys.argv) != 2:
        print("Usage: python3 generate_node_setup.py <number_of_nodes>")
        sys.exit(1)
    
    try:
        num_nodes = int(sys.argv[1])
        if num_nodes < 1:
            raise ValueError("Number of nodes must be positive")
    except ValueError as e:
        print(f"Error: {e}")
        sys.exit(1)
    
    print(f"Generating setup for {num_nodes} nodes...")
    generate_docker_compose(num_nodes)
    generate_setup_script(num_nodes)
    modify_config_generator(num_nodes)
    print("Done! You can now run ./setup-multi-node.sh to start your nodes")

if __name__ == "__main__":
    main() 