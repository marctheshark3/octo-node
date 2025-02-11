#!/usr/bin/env python3
import os
import sys
import hashlib
import argparse

def generate_hash(data):
    """Generate hash using Blake2b with 32-byte digest size."""
    if isinstance(data, str):
        data = data.encode()
    return hashlib.blake2b(data, digest_size=32).hexdigest()

def change_node_key(node_number, new_key=None):
    """Change API key for a specific node."""
    if not os.path.exists('config'):
        print("Error: config directory not found. Are you in the correct directory?")
        sys.exit(1)

    # Generate new key if none provided
    if new_key is None:
        new_key = ''.join(__import__('random').choices('0123456789abcdef', k=64))
    
    # Generate hash
    api_hash = generate_hash(new_key)
    
    # Update API key file
    key_file = f'config/ergo-{node_number}.api.key'
    conf_file = f'config/ergo-{node_number}.conf'
    
    if not os.path.exists(key_file) or not os.path.exists(conf_file):
        print(f"Error: Configuration files for node {node_number} not found.")
        sys.exit(1)
    
    # Update the files
    with open(key_file, 'w') as f:
        f.write(new_key)
    
    # Read config file
    with open(conf_file, 'r') as f:
        config = f.read()
    
    # Update apiKeyHash
    import re
    new_config = re.sub(
        r'apiKeyHash = ".*"',
        f'apiKeyHash = "{api_hash}"',
        config
    )
    
    # Write updated config
    with open(conf_file, 'w') as f:
        f.write(new_config)
    
    print(f"\nAPI key for node {node_number} has been updated:")
    print(f"New API Key: {new_key}")
    print(f"New Hash: {api_hash}")
    print("\nRestarting node...")
    
    # Restart the node
    os.system(f'docker-compose -f docker-compose-multi.yml restart ergo-node-{node_number}')
    print(f"\nNode {node_number} has been restarted with the new API key.")

def main():
    parser = argparse.ArgumentParser(description='Change API key for a specific Ergo node')
    parser.add_argument('--node', type=int, required=True, help='Node number to change key for')
    parser.add_argument('--key', help='New API key (random if not provided)')
    args = parser.parse_args()
    
    change_node_key(args.node, args.key)

if __name__ == "__main__":
    main() 