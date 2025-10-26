"""
Simple LangGraph application that interacts with the MCP server.
This client connects to the MCP server and uses its tools (web_search, roll_dice, get_news).
From: https://github.com/langchain-ai/langchain-mcp-adapters
"""

import asyncio
from dotenv import load_dotenv
from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client
from langchain.agents import create_agent
# from langgraph.prebuilt import create_react_agent

from langchain_mcp_adapters.tools import load_mcp_tools

# Load environment variables from .env file
load_dotenv()


async def main():
    """Main function to run the LangGraph agent with MCP tools."""
    
    # Configure the MCP server connection
    server_params = StdioServerParameters(
        command="python",          # Use the python interpreter
        args=["server.py"],        # Run this file
        env=None                   # Use current environment variables
    )
    
    # Connect to the MCP server
    async with stdio_client(server_params) as (read, write):
        async with ClientSession(read, write) as session:
            # Initialize the connection
            await session.initialize()
            
            # Load tools from the MCP server
            tools = await load_mcp_tools(session)
            
            print("Connected to MCP server!")
            print(f"Available tools: {[tool.name for tool in tools]}\n")
            
            # Create a ReAct agent with the MCP tools
            agent = create_agent("openai:gpt-4o-mini", tools)
            
            # Example queries to demonstrate the agent
            queries = [
                "What's the latest news about artificial intelligence with positive sentiment?",
                "Roll 2d6 dice for me",
                "Search the web for information about LangChain MCP adapters"
            ]
            
            print("Running example queries...\n")
            print("=" * 100)
            
            for i, query in enumerate(queries, 1):
                print(f"\nQuery {i}: {query}")
                print("-" * 100)
                
                response = await agent.ainvoke({"messages": query})
                
                # Display tool calls if any
                print("\n🔧 Tool Calls Made:")
                for message in response["messages"]:
                    # Check if message has tool calls
                    if hasattr(message, 'tool_calls') and message.tool_calls:
                        for tool_call in message.tool_calls:
                            print(f"  ├─ Tool: {tool_call['name']}")
                            print(f"  │  Args: {tool_call['args']}")
                    # Check if message is a tool response
                    elif hasattr(message, 'name') and message.name:
                        print(f"  └─ Tool Response from: {message.name}")
                
                # Get the last message (agent's response)
                last_message = response["messages"][-1]
                print(f"\n✅ Final Response: {last_message.content}\n")
                print("=" * 100)


if __name__ == "__main__":
    print("Starting LangGraph MCP Client...\n")
    asyncio.run(main())

