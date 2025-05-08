# ONOS MCP Mininet Demo

This repository contains the necessary components to reproduce the environment used in our paper. It combines ONOS SDN controller with Mininet to demonstrate the capabilities of MCP for network control and management.

## Prerequisites

- Docker and Docker Compose installed
- Git (to clone this repository)

## Setup Instructions

1. Clone this repository:
   ```
   git clone <repository-url>
   cd onos-mcp-mininet-demo
   ```

2. Start the environment:
   ```
   docker compose up -d
   ```

   This will start two containers:
   - ONOS SDN controller
   - Mininet network simulator

3. Wait approximately **1-2 minutes** for ONOS to fully initialize before proceeding.

## Accessing Mininet

To enter the Mininet environment:

```
docker exec -it onos-mcp-mininet-demo-mininet-1 /bin/bash
```

Once inside the Mininet container and after ONOS has fully initialized, you can create a simple topology with:

```
sudo mn --topo tree,2,2 --mac --switch ovs,protocols=OpenFlow14 --controller remote,ip=localhost
```

This creates a tree topology with depth 2 and fanout 2, using OpenFlow 1.4, and connects to the ONOS controller running on the host.

## Accessing ONOS UI

The ONOS Web UI is accessible at:
```
http://localhost:8181/onos/ui
```

Default credentials:
- Username: `onos`
- Password: `rocks`

## Installing MCP with Claude Desktop or Cursor

To integrate with MCP, follow these steps:

1. Clone the ONOS MCP server repository:
```
git clone https://anonymous.4open.science/r/onos-mcp-server-07E8
cd onos-mcp-server
```

2. Install any required dependencies for the MCP server (refer to the repository's instructions).

3. Add the ONOS server configuration to your [Claude Desktop](https://modelcontextprotocol.io/quickstart/user) or [Cursor](https://docs.cursor.com/context/model-context-protocol) settings file:

```json
{
  "mcpServers": {
    "onos": {
      "command": "python",
      "args": [
        "src/onos-mcp-server/server.py"
      ],
      "env": {
        "ONOS_API_BASE": "http://localhost:8181/onos/v1",
        "ONOS_USERNAME": "onos",
        "ONOS_PASSWORD": "rocks"
      }
    }
  }
}
```

4. Start your AI assistant with MCP support, and it will be able to interact with your ONOS controller.

## Configuration
The server uses the following environment variables:
- `ONOS_API_BASE`: Base URL for ONOS API (default: http://localhost:8181/onos/v1)
- `ONOS_USERNAME`: Username for ONOS API authentication (default: onos)
- `ONOS_PASSWORD`: Password for ONOS API authentication (default: rocks)
