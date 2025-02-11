#!/usr/bin/env python3
import hashlib
import base64

def generate_hash(data):
    """Generate hash using Blake2b with 32-byte digest size."""
    if isinstance(data, str):
        data = data.encode()
    return hashlib.blake2b(data, digest_size=32).hexdigest()

target_hash = "324dcf027dd4a30a932c441f365a25e86b173defa4b8e58948253471b81b72cf"
api_key = "hello"

print(f"Testing API key: '{api_key}'")
print("-" * 50)

# Test plain string
hash_value = generate_hash(api_key)
print(f"Blake2b Hash (32-byte): {hash_value}")
print(f"Expected Hash:         {target_hash}")
print(f"Matches: {hash_value == target_hash}")

# Test with different line endings
print("\nTesting with different line endings:")
for ending in ['\n', '\r\n', '\r']:
    test_key = f"hello{ending}"
    hash_value = generate_hash(test_key)
    print(f"\nWith {ending!r}:")
    print(f"Hash:    {hash_value}")
    print(f"Matches: {hash_value == target_hash}")

print("\nNote: If none of these match, we might need to:")
print("1. Try a different API key")
print("2. Check if there's any special processing in the Ergo node code")
print("3. Look for any configuration preprocessing")

# Let's also show what a new random key would look like
import random
new_api_key = ''.join(random.choices('0123456789abcdef', k=64))
new_hash = generate_hash(new_api_key.encode())
print("\nExample of a new random API key:")
print(f"API Key: {new_api_key}")
print(f"Hash: {new_hash}")

hash_value = generate_hash(api_key)
print(f"API Key: {api_key}")
print(f"Blake2b Hash: {hash_value}")
print(f"Expected Hash: {target_hash}")
print(f"Matches: {hash_value == target_hash}") 