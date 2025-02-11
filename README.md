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

Each node has its own API key located in the `config` directory:
- Node 1: `config/ergo-1.api.key`
- Node 2: `config/ergo-2.api.key`
etc.

Example API call:
```bash
# Get the API key
API_KEY=$(cat config/ergo-1.api.key)

# Make a request to node 1
curl -H "api_key: $API_KEY" http://localhost:9500/info
```

## Managing API Keys

### Generate a New API Key
You can generate a new API key and its corresponding hash using the included utility:

```bash
# Generate a random API key
python3 generate_api_key.py

# Use a specific API key
python3 generate_api_key.py --key "your-custom-key"
```

### Update a Node's API Key
To update a specific node's API key:

1. Generate a new key and hash:
```bash
python3 generate_api_key.py > new_key.txt
```

2. Update the node's configuration:
```bash
# Get the new API key
NEW_KEY=$(head -n 3 new_key.txt | tail -n 1 | cut -d' ' -f3)

# Get the hash
NEW_HASH=$(grep "apiKeyHash" new_key.txt | cut -d'"' -f2)

# Update the API key file
echo $NEW_KEY > config/ergo-1.api.key  # Replace 1 with your node number

# Update the configuration file
sed -i "s/apiKeyHash = .*/apiKeyHash = \"$NEW_HASH\"/" config/ergo-1.conf
```

3. Restart the specific node:
```bash
docker-compose -f docker-compose-multi.yml restart ergo-node-1
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
