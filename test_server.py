import asyncio
from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client

async def test_yfinance_server():
    # Create server parameters
    server_params = StdioServerParameters(
        command="python",
        args=["afinance_server.py"],
        env=None
    )
    
    try:
        async with stdio_client(server_params) as (read, write):
            async with ClientSession(read, write) as session:
                print("Connecting to server...")
                
                # Initialize
                await session.initialize()
                print("✓ Server initialized successfully!")
                
                # Test 1: List tools
                print("\n=== Available Tools ===")
                tools = await session.list_tools()
                for tool in tools.tools:
                    print(f"- {tool.name}: {tool.description}")
                
                # Test 2: Get stock info
                print("\n=== Testing get_stock_info for AAPL ===")
                result = await session.call_tool("get_stock_info", {"symbol": "AAPL"})
                print(result.content[0].text)
                
                # Test 3: Get historical data
                print("\n=== Testing get_historical_data for MSFT ===")
                result = await session.call_tool("get_historical_data", {
                    "symbol": "MSFT",
                    "period": "1mo",
                    "interval": "1d"
                })
                response_text = result.content[0].text
                if len(response_text) > 500:
                    print(response_text[:500] + "...")
                else:
                    print(response_text)
                
                # Test 4: Get multiple quotes
                print("\n=== Testing get_multiple_quotes ===")
                result = await session.call_tool("get_multiple_quotes", {
                    "symbols": ["AAPL", "GOOGL", "MSFT"]
                })
                response_text = result.content[0].text
                if len(response_text) > 500:
                    print(response_text[:500] + "...")
                else:
                    print(response_text)
                
                print("\n✓ All tests completed successfully!")
                
    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    asyncio.run(test_yfinance_server())