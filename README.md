# Octo-Node: Multi-Node Ergo Network Setup

A tool for easily setting up and managing multiple Ergo nodes in a containerized environment. This project allows you to spin up any number of Ergo nodes, each with its own configuration and API endpoint.

## Features

- Dynamic node generation (specify any number of nodes)
- Containerized setup using Docker
- Automatic API key generation for each node
- Isolated storage for each node
- Configurable ports for API and P2P networking
- Easy setup and management scripts
- API key management utilities

## Prerequisites

- Docker
- Docker Compose
- Python 3.x
- Bash shell

## Quick Start

1. Clone the repository:
```bash
git clone https://github.com/yourusername/octo-node.git
cd octo-node
```

2. Generate setup for N nodes (example for 6 nodes):
```bash
python3 generate_node_setup.py 6
```

3. Start the nodes:
```bash
./setup-multi-node.sh
```

## Default Port Configuration

The nodes will be accessible at the following ports:

| Node Number | API Port | P2P Port |
|------------|----------|----------|
| Node 1     | 9500     | 9600     |
| Node 2     | 9501     | 9601     |
| Node 3     | 9502     | 9602     |
| Node 4     | 9503     | 9603     |
| Node 5     | 9504     | 9604     |
| Node 6     | 9505     | 9605     |

## API Access

By default, all nodes are configured with the API key "hello". Each node's API key is stored in the `config` directory:
- Node 1: `config/ergo-1.api.key`
- Node 2: `config/ergo-2.api.key`
etc.

Example API call using the default key:
```bash
curl -H "api_key: hello" http://localhost:9500/info
```

The default API key hash for "hello" is:
```
324dcf027dd4a30a932c441f365a25e86b173defa4b8e58948253471b81b72cf
```

### Changing API Keys

You can change the API key for any node using the provided utility script:

```bash
# Generate a random API key for node 1
python3 change_node_key.py --node 1

# Set a specific API key for node 2
python3 change_node_key.py --node 2 --key "your-custom-key"
```

The script will:
1. Update the API key file
2. Update the node's configuration with the correct hash
3. Automatically restart the node to apply the changes

After changing a key, you can access the node using the new key:
```bash
# Get the new API key
API_KEY=$(cat config/ergo-1.api.key)

# Make a request with the new key
curl -H "api_key: $API_KEY" http://localhost:9500/info
```

### Managing API Keys

You can also use the API key utility script to generate new keys or compute hashes:

```bash
# Generate a random API key
python3 generate_api_key.py

# Generate hash for a specific key
python3 generate_api_key.py --key "your-custom-key"
```

The utility will output:
1. The API key
2. The Blake2b hash (32-byte digest)
3. The configuration line for ergo.conf

Example output:
```
API Key Details:
--------------------------------------------------
API Key: your-custom-key
Hash:    324dcf027dd4a30a932c441f365a25e86b173defa4b8e58948253471b81b72cf
--------------------------------------------------

To use this in your ergo.conf:
apiKeyHash = "324dcf027dd4a30a932c441f365a25e86b173defa4b8e58948253471b81b72cf"
```

## Directory Structure

```
.
├── config/                 # Node configurations and API keys
├── .ergo-*/               # Node data directories
├── generate_configs.py     # Configuration generator
├── generate_api_key.py    # API key utility
├── generate_node_setup.py # Main setup generator
├── setup-multi-node.sh    # Setup script
└── docker-compose-multi.yml # Docker compose configuration
```

## Configuration

Each node gets its own:
- Data directory (`.ergo-N/`)
- Configuration file (`config/ergo-N.conf`)
- API key (`config/ergo-N.api.key`)
- Port mappings for API and P2P communication

## Managing Nodes

Start all nodes:
```bash
docker-compose -f docker-compose-multi.yml up -d
```

Stop all nodes:
```bash
docker-compose -f docker-compose-multi.yml down
```

View logs:
```bash
docker-compose -f docker-compose-multi.yml logs -f
```

Start/stop/restart a specific node:
```bash
# Replace N with node number (1-6)
docker-compose -f docker-compose-multi.yml restart ergo-node-N
```

## Security Notes

- API keys are automatically generated and stored in the `config` directory
- Each node runs in its own container with isolated storage
- Configuration files and API keys are git-ignored by default
- Make sure to secure your API endpoints if exposing to the internet
- Use strong API keys in production environments

## Contributing

1. Fork the repository
2. Create your feature branch
3. Commit your changes
4. Push to the branch
5. Create a new Pull Request

## License

This project is licensed under the MIT License - see the LICENSE file for details.
