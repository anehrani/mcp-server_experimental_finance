# Quick Start Guide - YFinance MCP Server

## ✅ Setup Complete!

Your MCP server has been successfully migrated from Indian stocks (sfinance) to US stocks (yfinance).

## Test Results

✅ Dependencies installed via `uv sync`  
✅ YFinance working (tested with AAPL)  
✅ Server starts without errors  
✅ No Python syntax errors  

## Quick Test

```bash
# Activate virtual environment
source .venv/bin/activate

# Test yfinance integration
python afinance_test.py

# Expected output:
# Stock Info: Apple Inc.
# Current Price: 273.4
# Historical Data Shape: (20, 7)
# Latest Close: 273.39...
# Income Statement Shape: (39, 5)
```

## Configure Claude Desktop

### 1. Find your config file:

**macOS:**
```bash
open ~/Library/Application\ Support/Claude/
# Edit claude_desktop_config.json
```

**Windows:**
```cmd
explorer %APPDATA%\Claude
# Edit claude_desktop_config.json
```

### 2. Add this configuration:

**macOS:**
```json
{
  "mcpServers": {
    "yfinance": {
      "command": "bash",
      "args": [
        "-c",
        "cd /Users/alinehrani/projects/git_anehrani/mcp-server_experimental_finance && source .venv/bin/activate && python afinance_server.py"
      ]
    }
  }
}
```

**Windows:**
```json
{
  "mcpServers": {
    "yfinance": {
      "command": "cmd",
      "args": [
        "/c",
        "cd /d C:\\path\\to\\mcp-server_experimental_finance && .venv\\Scripts\\activate && python afinance_server.py"
      ]
    }
  }
}
```

### 3. Restart Claude Desktop

Close and reopen Claude Desktop to load the new server.

## Test with Claude

Try these queries in Claude:

### Basic Stock Info
```
Get stock info for AAPL
Get stock info for MSFT
Get stock info for GOOGL
```

### Historical Data
```
Get historical data for TSLA with period 1y
Get historical data for NVDA with period 6mo and interval 1wk
```

### Financial Analysis
```
Get financials for AAPL
Get earnings for MSFT
Get dividends for JNJ
```

### Market Intelligence
```
Get news for TSLA count 5
Get analyst recommendations for AMZN
Search stocks with query "Tesla"
```

### Multiple Stocks
```
Get multiple quotes for AAPL,GOOGL,MSFT,AMZN
Compare AAPL, MSFT, and GOOGL
```

### Index Analysis
```
Get stock info for ^GSPC
Get historical data for ^DJI with period 1y
Analyze the S&P 500 performance this year
```

## Available Tools

1. **get_stock_info** - Comprehensive stock information
2. **get_historical_data** - Historical OHLCV data
3. **get_financials** - Income statement, balance sheet, cash flow
4. **get_earnings** - Annual and quarterly earnings
5. **get_dividends** - Dividend history
6. **get_splits** - Stock split history
7. **get_news** - Recent news articles
8. **get_recommendations** - Analyst recommendations
9. **search_stocks** - Search by company name or ticker
10. **get_multiple_quotes** - Batch quotes for multiple stocks
11. **get_cache_stats** - Cache statistics
12. **clear_cache** - Clear cached data

## Popular Stock Symbols

### Tech Giants (FAANG+)
- AAPL - Apple
- GOOGL - Alphabet (Google)
- MSFT - Microsoft
- AMZN - Amazon
- META - Meta (Facebook)
- NVDA - NVIDIA
- TSLA - Tesla

### Financial
- JPM - JPMorgan Chase
- BAC - Bank of America
- GS - Goldman Sachs
- V - Visa
- MA - Mastercard

### Major Indices
- ^GSPC - S&P 500
- ^DJI - Dow Jones
- ^IXIC - NASDAQ Composite
- ^RUT - Russell 2000

### Popular ETFs
- SPY - S&P 500 ETF
- QQQ - NASDAQ-100 ETF
- IWM - Russell 2000 ETF
- VOO - Vanguard S&P 500 ETF

## Troubleshooting

### Server not appearing in Claude?
1. Check config file path is correct
2. Verify JSON syntax (use jsonlint.com)
3. Make sure path to project is absolute
4. Restart Claude Desktop completely

### Connection errors?
1. Check virtual environment is activated
2. Verify dependencies: `uv sync`
3. Test manually: `python afinance_server.py`
4. Check logs: `cat yfinance_server.log`

### Symbol not found?
- Use US stock symbols (AAPL not AAPL.NS)
- Check symbol on Yahoo Finance website first
- Try search_stocks tool to find correct symbol

## Next Steps

1. ✅ Server is ready to use
2. Configure Claude Desktop (see above)
3. Restart Claude Desktop
4. Start asking about US stocks!

## Migration Complete! 🎉

Your server has been successfully migrated from:
- **Indian stocks** (NSE/BSE via screener.in)
- **US stocks** (NYSE/NASDAQ via Yahoo Finance)

Key improvements:
- ✅ No authentication needed
- ✅ No browser/Chrome required
- ✅ More data sources (news, recommendations, dividends)
- ✅ Historical price data
- ✅ Real-time quotes
- ✅ Search functionality

For detailed migration notes, see [MIGRATION_SUMMARY.md](MIGRATION_SUMMARY.md)
