# YFinance MCP Server

A Model Context Protocol (MCP) server that provides access to US stock market data via Yahoo Finance. Built on top of the [yfinance package](https://github.com/ranaroussi/yfinance).

## Prerequisites

- Python 3.11 or higher
- Internet connection for Yahoo Finance API

## Installation

1. **Clone and setup**
   ```bash
   git clone <your-repo-url>
   cd mcp-server_experimental_finance
   python -m venv .venv
   ```

2. **Activate virtual environment**
   ```bash
   # Windows
   .venv\Scripts\activate
   
   # macOS/Linux
   source .venv/bin/activate
   ```

3. **Install dependencies**
   ```bash
   pip install -e .
   ```

## Configuration

### Option 1: Virtual Environment Activation (Recommended)

**Windows:**
```json
{
  "mcpServers": {
    "yfinance": {
      "command": "cmd",
      "args": [
        "/c",
        "cd /d C:\\path\\to\\your\\project\\mcp-server_experimental_finance && .venv\\Scripts\\activate && python afinance_server.py"
      ]
    }
  }
}
```

**macOS/Linux:**
```json
{
  "mcpServers": {
    "yfinance": {
      "command": "bash",
      "args": [
        "-c",
        "cd /path/to/your/project/mcp-server_experimental_finance && source .venv/bin/activate && python afinance_server.py"
      ]
    }
  }
}
```

### Option 2: Direct Python Path

**Windows:**
```json
{
  "mcpServers": {
    "yfinance": {
      "command": "C:\\path\\to\\your\\project\\mcp-server_experimental_finance\\.venv\\Scripts\\python.exe",
      "args": [
        "C:\\path\\to\\your\\project\\mcp-server_experimental_finance\\afinance_server.py"
      ]
    }
  }
}
```
        "SCREENER_EMAIL": "your-email@example.com",
        "SCREENER_PASSWORD": "YourPassword123",
        "CHROME_PATH": "C:\\Program Files\\Google\\Chrome\\Application\\chrome.exe",
        "SCREENER_URL": "https://www.screener.in/"
      }
    }
  }
}
```

**macOS/Linux:**
```json
{
  "mcpServers": {
    "sfinance": {
      "command": "/path/to/your/project/sfinance-mcp-server/.venv/bin/python",
      "args": [
        "/path/to/your/project/sfinance-mcp-server/sfinance_server.py"
**macOS:**
```json
{
  "mcpServers": {
    "yfinance": {
      "command": "/path/to/your/project/mcp-server_experimental_finance/.venv/bin/python",
      "args": [
        "/path/to/your/project/mcp-server_experimental_finance/afinance_server.py"
      ]
    }
  }
}
```

## Configuration File Locations

- **Windows**: `%APPDATA%\Claude\claude_desktop_config.json`
- **macOS**: `~/Library/Application Support/Claude/claude_desktop_config.json`

## Required Changes

1. Replace path placeholders with your actual project path
2. Restart Claude Desktop after configuration

## Features

- **Stock Analysis**: Company info, financial statements, earnings, dividends, splits
- **Market Data**: Historical prices, real-time quotes, news, analyst recommendations
- **US Market Focus**: S&P 500, NASDAQ, NYSE, and other US exchanges
- **Multiple Stock Support**: Compare multiple stocks simultaneously

## Usage

### Stock Analysis
```
Get stock info for AAPL
Get historical data for MSFT with period 1y
Get financials for GOOGL
Get earnings for TSLA
```

### Market Data
```
Get news for NVDA count 5
Get analyst recommendations for AMZN
Search stocks with query "Apple"
Get multiple quotes for AAPL,GOOGL,MSFT
```

### Index Analysis
```
Get stock info for ^GSPC (S&P 500)
Get historical data for ^DJI (Dow Jones)
Get stock info for ^IXIC (NASDAQ)
```

## Available Tools

### Stock Information
- `get_stock_info` - Comprehensive stock information including price, P/E, market cap, financials
- `get_historical_data` - Historical OHLCV data with flexible periods and intervals
- `get_financials` - Income statement, balance sheet, and cash flow (annual or quarterly)
- `get_earnings` - Annual and quarterly earnings data

### Corporate Actions
- `get_dividends` - Dividend payment history
- `get_splits` - Stock split history

### Market Intelligence
- `get_news` - Recent news articles
- `get_recommendations` - Analyst recommendations and ratings
- `search_stocks` - Search by company name or ticker
- `get_multiple_quotes` - Batch quotes for multiple stocks

### Utilities
- `get_cache_stats` - Cache information
- `clear_cache` - Clear cache for fresh data

## Prompt Templates

- **Stock Analysis** - Comprehensive analysis of a US stock
- **Market Comparison** - Compare multiple stocks
- **S&P 500 Analysis** - Analyze the S&P 500 index and trends

## Supported Symbols

### Major US Stocks
- Tech: AAPL, GOOGL, MSFT, AMZN, META, NVDA, TSLA
- Finance: JPM, BAC, GS, MS, C, WFC
- Healthcare: JNJ, UNH, PFE, ABBV, MRK
- Consumer: WMT, HD, MCD, NKE, SBUX

### Major Indices
- ^GSPC - S&P 500
- ^DJI - Dow Jones Industrial Average
- ^IXIC - NASDAQ Composite
- ^RUT - Russell 2000

### ETFs
- SPY, QQQ, IWM, DIA, VOO, VTI, etc.

## Dependencies

- [yfinance](https://github.com/ranaroussi/yfinance) - Yahoo Finance API
- MCP - Model Context Protocol
- pandas - Data handling
- python-dotenv - Environment variables

## License

MIT License

## Disclaimer

For educational purposes only. Always verify financial data from official sources before making investment decisions. This tool uses Yahoo Finance's publicly available API.