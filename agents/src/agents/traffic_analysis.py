import asyncio

from agents import Agent, Runner
from agents.mcp import MCPServerStdio

async def main():
    async with MCPServerStdio(
        cache_tools_list=True,  # Cache the tools list, for demonstration
        params={
            "command": "/root/.local/bin/uv",
            "args": [
                "--directory", "/root/onos-mcp-server/src/onos_mcp_server",
                "run", "server.py"
            ],
            "env": {"ONOS_API_BASE": "onos"}
        },
    ) as onos_mcp_server:
        # Create a new agent specialized for traffic analysis
        agent = Agent(
            name="TrafficAnalyzer",
            instructions="You are an expert traffic analysis agent. Provide detailed insights into network traffic patterns, detect anomalies, and suggest optimizations for traffic flow.",
            mcp_servers=[onos_mcp_server]
        )

        # Run the agent with a traffic analysis command
        result = await Runner.run(agent, "Analyze current network traffic and identify any bottlenecks or unusual patterns.")
        print(result.final_output)

if __name__ == "__main__":
    asyncio.run(main())
    