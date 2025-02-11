#!/usr/bin/env python3
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
