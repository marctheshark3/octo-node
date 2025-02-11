#!/usr/bin/env python3
import hashlib
import sys
import os

def generate_hash(data):
    """Generate hash using Blake2b with 32-byte digest size."""
    if isinstance(data, str):
        data = data.encode()
    print(f"\nData being hashed (hex):", data.hex())
    print(f"Data being hashed (repr):", repr(data))
    print(f"Data length:", len(data))
    return hashlib.blake2b(data, digest_size=32).hexdigest()

def verify_node_api(node_number):
    """Verify API key and hash for a specific node."""
    api_key_file = f'config/ergo-{node_number}.api.key'
    conf_file = f'config/ergo-{node_number}.conf'
    
    # Check if files exist
    if not os.path.exists(api_key_file) or not os.path.exists(conf_file):
        print(f"Error: Configuration files for node {node_number} not found")
        return
    
    # Read API key
    with open(api_key_file, 'r') as f:
        api_key = f.read().strip()
    
    # Read config file to get hash
    with open(conf_file, 'r') as f:
        config_content = f.read()
        for line in config_content.split('\n'):
            if 'apiKeyHash' in line:
                stored_hash = line.split('"')[1]
                break
        else:
            print("Error: apiKeyHash not found in config file")
            return
    
    # Generate hash from API key
    computed_hash = generate_hash(api_key)
    
    print(f"\nVerifying Node {node_number}:")
    print("-" * 50)
    print(f"API Key: {api_key}")
    print(f"API Key length: {len(api_key)}")
    print(f"Stored Hash:    {stored_hash}")
    print(f"Computed Hash:  {computed_hash}")
    print(f"Match: {stored_hash == computed_hash}")
    print("\nFor curl testing:")
    print(f"curl -H 'api_key: {api_key}' http://localhost:{9500 + node_number - 1}/info")

def main():
    if len(sys.argv) != 2:
        print("Usage: python3 verify_node_api.py <node_number>")
        sys.exit(1)
    
    try:
        node_number = int(sys.argv[1])
        verify_node_api(node_number)
    except ValueError:
        print("Error: Node number must be an integer")
        sys.exit(1)

if __name__ == "__main__":
    main() 