"""Network Summary Agent.

This module provides an AI agent that generates high-level summaries of the ONOS network state.
It uses MCP to communicate with ONOS and provides human-readable network analysis.
"""

import asyncio

from agents import Agent, Runner
from agents.mcp import MCPServerStdio

async def main():
    """Run the network summary agent."""
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
        agent = Agent(name="Assistant", instructions="You are a helpful assistant", mcp_servers=[onos_mcp_server])

        result = await Runner.run(agent, "Get the network summary")
        print(result.final_output)


if __name__ == "__main__":
    asyncio.run(main())
