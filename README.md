# Octo-Node: Multi-Node Ergo Network Setup

A tool for easily setting up and managing multiple Ergo nodes in a containerized environment. This project allows you to spin up any number of Ergo nodes, each with its own configuration and API endpoint.

## Features

- Dynamic node generation (specify any number of nodes)
- Containerized setup using Docker
- Automatic API key generation for each node
- Isolated storage for each node
- Configurable ports for API and P2P networking
- Easy setup and management scripts

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
| Node 1     | 9100     | 9200     |
| Node 2     | 9101     | 9201     |
| Node 3     | 9102     | 9202     |
| Node 4     | 9103     | 9203     |
| Node 5     | 9104     | 9204     |
| Node 6     | 9105     | 9205     |

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
curl -H "api_key: $API_KEY" http://localhost:9100/info
```

## Directory Structure

```
.
├── config/                 # Node configurations and API keys
├── .ergo-*/               # Node data directories
├── generate_configs.py     # Configuration generator
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

## Security Notes

- API keys are automatically generated and stored in the `config` directory
- Each node runs in its own container with isolated storage
- Configuration files and API keys are git-ignored by default
- Make sure to secure your API endpoints if exposing to the internet

## Contributing

1. Fork the repository
2. Create your feature branch
3. Commit your changes
4. Push to the branch
5. Create a new Pull Request

## License

This project is licensed under the MIT License - see the LICENSE file for details.
