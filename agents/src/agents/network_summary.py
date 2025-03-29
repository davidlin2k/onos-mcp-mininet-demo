import asyncio

from agents import Agent, Runner
from agents.mcp import MCPServerStdio

async def main():
    async with MCPServerStdio(
        cache_tools_list=True,  # Cache the tools list, for demonstration
        params={"command": "/root/.local/bin/uv", "args": ["--directory", "/root/onos-mcp-server/src/onos_mcp_server", "run", "server.py"], "env": {"ONOS_API_BASE": "onos"}},
    ) as onos_mcp_server:
        agent = Agent(name="Assistant", instructions="You are a helpful assistant", mcp_servers=[onos_mcp_server])

        result = await Runner.run(agent, "Get the network summary")
        print(result.final_output)


if __name__ == "__main__":
    asyncio.run(main())
