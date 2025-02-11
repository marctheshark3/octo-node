#!/usr/bin/env python3
import hashlib
import random
import argparse

def generate_hash(data):
    """Generate hash using Blake2b with 32-byte digest size."""
    if isinstance(data, str):
        data = data.encode()
    return hashlib.blake2b(data, digest_size=32).hexdigest()

def generate_random_key():
    """Generate a random 64-character hexadecimal API key."""
    return ''.join(random.choices('0123456789abcdef', k=64))

def main():
    parser = argparse.ArgumentParser(description='Generate Ergo node API key and hash')
    parser.add_argument('--key', help='Use specific API key instead of generating random one')
    args = parser.parse_args()

    if args.key:
        api_key = args.key
        print("Using provided API key")
    else:
        api_key = generate_random_key()
        print("Generated random API key")

    api_hash = generate_hash(api_key)
    
    print("\nAPI Key Details:")
    print("-" * 50)
    print(f"API Key: {api_key}")
    print(f"Hash:    {api_hash}")
    print("-" * 50)
    print("\nTo use this in your ergo.conf:")
    print('apiKeyHash = "' + api_hash + '"')

if __name__ == "__main__":
    main() 