"""Traffic Analysis Agent.

This module provides an AI agent specialized in analyzing network traffic patterns.
It can detect anomalies, identify bottlenecks, and suggest optimizations.
"""

import asyncio

from agents import Agent, Runner
from agents.mcp import MCPServerStdio

async def main():
    """Run the traffic analysis agent."""
    async with MCPServerStdio(
        cache_tools_list=True,  # Cache the tools list, for demonstration
        params={
            "command": "/root/.local/bin/uv",
            "args": [
                "--directory", "/root/onos-mcp-server/src/onos_mcp_server",
                "run", "server.py"
            ],
            "env": {"ONOS_API_BASE": "http://onos:8181/onos/v1"}
        },
    ) as onos_mcp_server:
        # Create a new agent specialized for traffic analysis
        agent = Agent(
            name="NetworkTroubleshooter",
            instructions="You are a network troubleshooting agent. Diagnose connectivity issues between hosts in a Mininet environment, focusing on why 'h1 ping h2' might be stuck.",
            mcp_servers=[onos_mcp_server]
        )

        # Run the agent with a troubleshooting command
        result = await Runner.run(agent, "Diagnose why 'h1 ping h2' is stuck in Mininet and suggest possible solutions.")
        print(result.final_output)

if __name__ == "__main__":
    asyncio.run(main())
