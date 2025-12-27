import json
import asyncio
import os
from typing import List, Dict, Any, Optional
import pandas as pd
import time
from datetime import datetime, timedelta

import mcp.types as types
from mcp.server import Server
import mcp.server.stdio

# Import yfinance for US market data
import yfinance as yf

from dotenv import load_dotenv
load_dotenv()

import logging

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler(),
        logging.FileHandler('yfinance_server.log')
    ]
)
logger = logging.getLogger(__name__)


# Create server
server = Server("yfinance-server")

# Ticker cache with expiration
ticker_cache = {}
CACHE_EXPIRY_HOURS = 24  # Cache tickers for 24 hours

def get_ticker_yfinance(symbol: str):
    """Get yfinance ticker object with caching"""
    global ticker_cache
    
    symbol = symbol.upper()
    current_time = datetime.now()
    
    # Check if ticker exists in cache and is not expired
    if symbol in ticker_cache:
        cached_ticker, cache_time = ticker_cache[symbol]
        if current_time - cache_time < timedelta(hours=CACHE_EXPIRY_HOURS):
            logger.info(f"Using cached ticker for {symbol}")
            return cached_ticker
        else:
            logger.info(f"Cache expired for {symbol}, fetching new ticker")
            del ticker_cache[symbol]
    
    # Create new ticker and cache it
    logger.info(f"Creating new ticker for {symbol}...")
    start_time = time.time()
    
    ticker = yf.Ticker(symbol)
    
    end_time = time.time()
    logger.info(f"Ticker creation for {symbol} took {end_time - start_time:.2f} seconds")
    
    # Cache the ticker with current timestamp
    ticker_cache[symbol] = (ticker, current_time)
    
    return ticker



def clear_expired_cache():
    """Clear expired cache entries"""
    global ticker_cache
    current_time = datetime.now()
    expired_symbols = []
    
    for symbol, (ticker, cache_time) in ticker_cache.items():
        if current_time - cache_time >= timedelta(hours=CACHE_EXPIRY_HOURS):
            expired_symbols.append(symbol)
    
    for symbol in expired_symbols:
        del ticker_cache[symbol]
        logger.info(f"Cleared expired cache for {symbol}")

def get_cache_stats():
    """Get cache statistics"""
    current_time = datetime.now()
    active_cache = 0
    expired_cache = 0
    
    for symbol, (ticker, cache_time) in ticker_cache.items():
        if current_time - cache_time < timedelta(hours=CACHE_EXPIRY_HOURS):
            active_cache += 1
        else:
            expired_cache += 1
    
    stats = {
        "active_cache_entries": active_cache,
        "expired_cache_entries": expired_cache,
        "total_cache_entries": len(ticker_cache),
        "cache_expiry_hours": CACHE_EXPIRY_HOURS
    }
    logger.debug(f"Cache stats: {stats}")
    return stats

def df_to_json(df: pd.DataFrame) -> str:
    """Convert DataFrame to JSON string"""
    if df.empty:
        return json.dumps({"error": "No data available"})
    return df.to_json(orient='records', indent=2)

@server.list_prompts()
async def list_prompts() -> List[types.Prompt]:
    """List available prompt templates for stock analysis"""
    return [
        types.Prompt(
            name="stock_analysis",
            description="Get comprehensive analysis for a US stock",
            arguments=[
                types.PromptArgument(
                    name="symbol",
                    description="Stock ticker symbol (e.g., AAPL, GOOGL, MSFT)",
                    required=True
                )
            ]
        ),
        types.Prompt(
            name="market_comparison",
            description="Compare multiple US stocks",
            arguments=[
                types.PromptArgument(
                    name="symbols",
                    description="Comma-separated stock symbols (e.g., AAPL,GOOGL,MSFT)",
                    required=True
                )
            ]
        ),
        types.Prompt(
            name="sp500_analysis",
            description="Analyze S&P 500 index and major components",
            arguments=[
                types.PromptArgument(
                    name="timeframe",
                    description="Analysis timeframe (e.g., 1mo, 3mo, 1y)",
                    required=False
                )
            ]
        )
    ]

@server.get_prompt()
async def get_prompt(name: str, arguments: Dict[str, str] | None) -> types.GetPromptResult:
    """Get specific prompt template"""
    
    if name == "stock_analysis":
        symbol = arguments.get("symbol", "AAPL") if arguments else "AAPL"
        
        return types.GetPromptResult(
            description=f"Comprehensive analysis for {symbol}",
            messages=[
                types.PromptMessage(
                    role="user",
                    content=types.TextContent(
                        type="text",
                        text=f"Please provide a comprehensive analysis of {symbol} including:\n\n" +
                            "- Current stock information (price, market cap, P/E ratio)\n" +
                            "- Financial statements (income statement, balance sheet, cash flow)\n" +
                            "- Recent earnings data\n" +
                            "- Dividend history (if applicable)\n" +
                            "- Recent news and analyst recommendations\n" +
                            "- Year-to-date performance"
                    )
                )
            ]
        )
    
    elif name == "market_comparison":
        symbols = arguments.get("symbols", "AAPL,GOOGL,MSFT") if arguments else "AAPL,GOOGL,MSFT"
        symbol_list = [s.strip() for s in symbols.split(',')]
        
        return types.GetPromptResult(
            description=f"Compare stocks: {symbols}",
            messages=[
                types.PromptMessage(
                    role="user",
                    content=types.TextContent(
                        type="text",
                        text=f"Please compare these stocks: {', '.join(symbol_list)}\n\n" +
                            "Include comparison of:\n" +
                            "- Current prices and market caps\n" +
                            "- P/E ratios and valuation metrics\n" +
                            "- Dividend yields\n" +
                            "- Year-to-date performance\n" +
                            "- Financial health indicators\n" +
                            "- Recent news sentiment"
                    )
                )
            ]
        )
    
    elif name == "sp500_analysis":
        timeframe = arguments.get("timeframe", "1y") if arguments else "1y"
        
        return types.GetPromptResult(
            description=f"S&P 500 analysis over {timeframe}",
            messages=[
                types.PromptMessage(
                    role="user",
                    content=types.TextContent(
                        type="text",
                        text=f"Please analyze the S&P 500 index (^GSPC) over the past {timeframe}:\n\n" +
                            "- Historical price performance\n" +
                            "- Current level and trends\n" +
                            "- Major gainers and losers (if available)\n" +
                            "- Recent market news\n" +
                            "- Key support and resistance levels"
                    )
                )
            ]
        )
    
    else:
        raise ValueError(f"Unknown prompt: {name}")

@server.list_tools()
async def list_tools() -> List[types.Tool]:
    return [
        types.Tool(
            name="get_stock_info",
            description="Get comprehensive stock information for US stocks including current price, market cap, P/E ratios, and key financial metrics",
            inputSchema={
                "type": "object",
                "properties": {
                    "symbol": {
                        "type": "string", 
                        "description": "US stock ticker symbol (e.g., AAPL, GOOGL, MSFT, TSLA, ^GSPC for S&P 500)"
                    }
                },
                "required": ["symbol"]
            }
        ),
        types.Tool(
            name="get_historical_data",
            description="Get historical stock price data with flexible time periods and intervals",
            inputSchema={
                "type": "object",
                "properties": {
                    "symbol": {
                        "type": "string", 
                        "description": "US stock ticker symbol (e.g., AAPL, GOOGL, MSFT)"
                    },
                    "period": {
                        "type": "string",
                        "description": "Time period: 1d, 5d, 1mo, 3mo, 6mo, 1y, 2y, 5y, 10y, ytd, max",
                        "default": "1mo"
                    },
                    "interval": {
                        "type": "string",
                        "description": "Data interval: 1m, 2m, 5m, 15m, 30m, 60m, 90m, 1h, 1d, 5d, 1wk, 1mo, 3mo",
                        "default": "1d"
                    }
                },
                "required": ["symbol"]
            }
        ),
        types.Tool(
            name="get_financials",
            description="Get financial statements (income statement, balance sheet, cash flow) for US companies",
            inputSchema={
                "type": "object",
                "properties": {
                    "symbol": {
                        "type": "string", 
                        "description": "US stock ticker symbol (e.g., AAPL, GOOGL, MSFT)"
                    },
                    "quarterly": {
                        "type": "boolean",
                        "description": "Get quarterly data if true, annual if false",
                        "default": False
                    }
                },
                "required": ["symbol"]
            }
        ),
        types.Tool(
            name="get_earnings",
            description="Get earnings data (annual and quarterly) for US companies",
            inputSchema={
                "type": "object",
                "properties": {
                    "symbol": {
                        "type": "string", 
                        "description": "US stock ticker symbol (e.g., AAPL, GOOGL, MSFT)"
                    }
                },
                "required": ["symbol"]
            }
        ),
        types.Tool(
            name="get_dividends",
            description="Get dividend payment history for US stocks",
            inputSchema={
                "type": "object",
                "properties": {
                    "symbol": {
                        "type": "string", 
                        "description": "US stock ticker symbol (e.g., AAPL, MSFT, JNJ)"
                    }
                },
                "required": ["symbol"]
            }
        ),
        types.Tool(
            name="get_splits",
            description="Get stock split history for US stocks",
            inputSchema={
                "type": "object",
                "properties": {
                    "symbol": {
                        "type": "string", 
                        "description": "US stock ticker symbol (e.g., AAPL, TSLA, NVDA)"
                    }
                },
                "required": ["symbol"]
            }
        ),
        types.Tool(
            name="get_news",
            description="Get recent news articles for a US stock",
            inputSchema={
                "type": "object",
                "properties": {
                    "symbol": {
                        "type": "string", 
                        "description": "US stock ticker symbol (e.g., AAPL, GOOGL, MSFT)"
                    },
                    "count": {
                        "type": "integer",
                        "description": "Number of news articles to return (default: 10)",
                        "default": 10
                    }
                },
                "required": ["symbol"]
            }
        ),
        types.Tool(
            name="get_recommendations",
            description="Get analyst recommendations and ratings for US stocks",
            inputSchema={
                "type": "object",
                "properties": {
                    "symbol": {
                        "type": "string", 
                        "description": "US stock ticker symbol (e.g., AAPL, GOOGL, MSFT)"
                    }
                },
                "required": ["symbol"]
            }
        ),
        types.Tool(
            name="search_stocks",
            description="Search for US stocks by company name or ticker symbol",
            inputSchema={
                "type": "object",
                "properties": {
                    "query": {
                        "type": "string",
                        "description": "Search query - company name or ticker (e.g., 'Apple', 'MSFT', 'Tesla')"
                    },
                    "limit": {
                        "type": "integer",
                        "description": "Maximum number of results (default: 10)",
                        "default": 10
                    }
                },
                "required": ["query"]
            }
        ),
        types.Tool(
            name="get_multiple_quotes",
            description="Get current quotes for multiple US stocks at once",
            inputSchema={
                "type": "object",
                "properties": {
                    "symbols": {
                        "type": "array",
                        "items": {"type": "string"},
                        "description": "List of US stock ticker symbols (e.g., ['AAPL', 'GOOGL', 'MSFT'])"
                    }
                },
                "required": ["symbols"]
            }
        ),
        types.Tool(
            name="get_cache_stats",
            description="Get ticker cache statistics and performance info",
            inputSchema={
                "type": "object",
                "properties": {},
                "required": []
            }
        ),
        types.Tool(
            name="clear_cache",
            description="Clear all cached ticker objects (use when you want fresh data)",
            inputSchema={
                "type": "object",
                "properties": {
                    "symbol": {
                        "type": "string",
                        "description": "Optional: specific symbol to clear from cache. If not provided, clears all cache."
                    }
                },
                "required": []
            }
        )
    ]

@server.call_tool()
async def call_tool(name: str, arguments: Dict[str, Any]) -> List[types.TextContent]:
    """Handle tool calls"""
    try:
        # Handle cache management tools first
        if name == "get_cache_stats":
            stats = get_cache_stats()
            return [types.TextContent(type="text", text=json.dumps(stats, indent=2))]
        
        elif name == "clear_cache":
            global ticker_cache
            symbol = arguments.get("symbol")
            
            if symbol:
                symbol = symbol.upper()
                if symbol in ticker_cache:
                    del ticker_cache[symbol]
                    result = {"message": f"Cleared cache for {symbol}"}
                else:
                    result = {"message": f"No cache found for {symbol}"}
            else:
                cache_count = len(ticker_cache)
                ticker_cache.clear()
                result = {"message": f"Cleared all cache ({cache_count} entries)"}
            
            return [types.TextContent(type="text", text=json.dumps(result, indent=2))]
        
        # Handle yfinance tools
        elif name == "get_stock_info":
            symbol = arguments["symbol"].upper()
            clear_expired_cache()
            ticker = get_ticker_yfinance(symbol)
            info = ticker.info
            
            result = {
                "symbol": symbol,
                "name": info.get("longName", ""),
                "current_price": info.get("currentPrice", 0.0),
                "previous_close": info.get("previousClose"),
                "market_cap": info.get("marketCap"),
                "trailing_pe": info.get("trailingPE"),
                "forward_pe": info.get("forwardPE"),
                "peg_ratio": info.get("pegRatio"),
                "price_to_book": info.get("priceToBook"),
                "price_to_sales": info.get("priceToSalesTrailing12Months"),
                "dividend_yield": info.get("dividendYield"),
                "beta": info.get("beta"),
                "52_week_high": info.get("fiftyTwoWeekHigh"),
                "52_week_low": info.get("fiftyTwoWeekLow"),
                "volume": info.get("volume"),
                "avg_volume": info.get("averageVolume"),
                "earnings_per_share": info.get("trailingEps"),
                "debt_to_equity": info.get("debtToEquity"),
                "return_on_equity": info.get("returnOnEquity"),
                "profit_margins": info.get("profitMargins"),
                "operating_margins": info.get("operatingMargins"),
                "revenue_growth": info.get("revenueGrowth"),
                "sector": info.get("sector"),
                "industry": info.get("industry"),
                "country": info.get("country"),
                "website": info.get("website"),
                "business_summary": (info.get("businessSummary", "")[:500] + "..." if info.get("businessSummary") else "")
            }
            return [types.TextContent(type="text", text=json.dumps(result, indent=2))]
        
        elif name == "get_historical_data":
            symbol = arguments["symbol"].upper()
            period = arguments.get("period", "1mo")
            interval = arguments.get("interval", "1d")
            
            clear_expired_cache()
            ticker = get_ticker_yfinance(symbol)
            hist = ticker.history(period=period, interval=interval)
            
            if hist.empty:
                return [types.TextContent(type="text", text=json.dumps({"error": f"No data found for {symbol}"}, indent=2))]
            
            data = []
            for date, row in hist.iterrows():
                data.append({
                    "date": date.strftime("%Y-%m-%d"),
                    "open": float(row["Open"]),
                    "high": float(row["High"]),
                    "low": float(row["Low"]),
                    "close": float(row["Close"]),
                    "volume": int(row["Volume"]) if "Volume" in row else 0,
                })
            
            result = {
                "symbol": symbol,
                "period": period,
                "interval": interval,
                "data": data,
                "count": len(data)
            }
            return [types.TextContent(type="text", text=json.dumps(result, indent=2))]
        
        elif name == "get_financials":
            symbol = arguments["symbol"].upper()
            quarterly = arguments.get("quarterly", False)
            
            clear_expired_cache()
            ticker = get_ticker_yfinance(symbol)
            
            if quarterly:
                income_stmt = ticker.quarterly_income_stmt
                balance_sheet = ticker.quarterly_balance_sheet
                cash_flow = ticker.quarterly_cashflow
            else:
                income_stmt = ticker.income_stmt
                balance_sheet = ticker.balance_sheet
                cash_flow = ticker.cashflow
            
            result = {
                "symbol": symbol,
                "quarterly": quarterly,
                "income_statement": income_stmt.to_dict() if not income_stmt.empty else {},
                "balance_sheet": balance_sheet.to_dict() if not balance_sheet.empty else {},
                "cash_flow": cash_flow.to_dict() if not cash_flow.empty else {}
            }
            return [types.TextContent(type="text", text=json.dumps(result, indent=2, default=str))]
        
        elif name == "get_earnings":
            symbol = arguments["symbol"].upper()
            clear_expired_cache()
            ticker = get_ticker_yfinance(symbol)
            
            annual_income = ticker.income_stmt
            quarterly_income = ticker.quarterly_income_stmt
            
            result = {
                "symbol": symbol,
                "annual_earnings": {},
                "quarterly_earnings": {},
                "note": "Earnings data extracted from income statements (Net Income)"
            }
            
            if annual_income is not None and not annual_income.empty:
                net_income_rows = annual_income[annual_income.index.str.contains("Net Income", case=False, na=False)]
                if not net_income_rows.empty:
                    annual_earnings = {}
                    for date, value in net_income_rows.iloc[0].items():
                        annual_earnings[str(date.date() if hasattr(date, 'date') else date)] = float(value) if pd.notna(value) else None
                    result["annual_earnings"] = annual_earnings
            
            if quarterly_income is not None and not quarterly_income.empty:
                net_income_rows = quarterly_income[quarterly_income.index.str.contains("Net Income", case=False, na=False)]
                if not net_income_rows.empty:
                    quarterly_earnings = {}
                    for date, value in net_income_rows.iloc[0].items():
                        quarterly_earnings[str(date.date() if hasattr(date, 'date') else date)] = float(value) if pd.notna(value) else None
                    result["quarterly_earnings"] = quarterly_earnings
            
            return [types.TextContent(type="text", text=json.dumps(result, indent=2))]
        
        elif name == "get_dividends":
            symbol = arguments["symbol"].upper()
            clear_expired_cache()
            ticker = get_ticker_yfinance(symbol)
            dividends = ticker.dividends
            
            if dividends.empty:
                result = {"symbol": symbol, "dividends": [], "message": "No dividend data available"}
            else:
                dividend_data = []
                for date, dividend in dividends.items():
                    dividend_data.append({
                        "date": date.strftime("%Y-%m-%d"),
                        "dividend": float(dividend)
                    })
                result = {"symbol": symbol, "dividends": dividend_data, "count": len(dividend_data)}
            
            return [types.TextContent(type="text", text=json.dumps(result, indent=2))]
        
        elif name == "get_splits":
            symbol = arguments["symbol"].upper()
            clear_expired_cache()
            ticker = get_ticker_yfinance(symbol)
            splits = ticker.splits
            
            if splits.empty:
                result = {"symbol": symbol, "splits": [], "message": "No split data available"}
            else:
                split_data = []
                for date, split in splits.items():
                    split_data.append({
                        "date": date.strftime("%Y-%m-%d"),
                        "split_ratio": float(split)
                    })
                result = {"symbol": symbol, "splits": split_data, "count": len(split_data)}
            
            return [types.TextContent(type="text", text=json.dumps(result, indent=2))]
        
        elif name == "get_news":
            symbol = arguments["symbol"].upper()
            count = arguments.get("count", 10)
            
            clear_expired_cache()
            ticker = get_ticker_yfinance(symbol)
            news = ticker.news
            
            if not news:
                result = {"symbol": symbol, "news": [], "message": "No news available"}
            else:
                news = news[:count]
                news_data = []
                for article in news:
                    news_data.append({
                        "title": article.get("title", ""),
                        "publisher": article.get("publisher", ""),
                        "link": article.get("link", ""),
                        "published": article.get("providerPublishTime", 0)
                    })
                result = {"symbol": symbol, "news": news_data, "count": len(news_data)}
            
            return [types.TextContent(type="text", text=json.dumps(result, indent=2))]
        
        elif name == "get_recommendations":
            symbol = arguments["symbol"].upper()
            clear_expired_cache()
            ticker = get_ticker_yfinance(symbol)
            recommendations = ticker.recommendations
            
            if recommendations is None or recommendations.empty:
                result = {"symbol": symbol, "recommendations": [], "message": "No recommendations available"}
            else:
                rec_data = []
                for _, row in recommendations.iterrows():
                    rec_data.append({
                        "period": row.get("period", ""),
                        "strong_buy": int(row.get("strongBuy", 0)),
                        "buy": int(row.get("buy", 0)),
                        "hold": int(row.get("hold", 0)),
                        "sell": int(row.get("sell", 0)),
                        "strong_sell": int(row.get("strongSell", 0))
                    })
                result = {"symbol": symbol, "recommendations": rec_data, "count": len(rec_data)}
            
            return [types.TextContent(type="text", text=json.dumps(result, indent=2))]
        
        elif name == "search_stocks":
            query = arguments["query"]
            limit = arguments.get("limit", 10)
            
            search_obj = yf.Search(query, max_results=limit)
            search_results = search_obj.quotes
            
            if not search_results:
                result = {"query": query, "results": [], "message": "No results found"}
            else:
                results = []
                for res in search_results[:limit]:
                    results.append({
                        "symbol": res.get("symbol", ""),
                        "name": res.get("longname", res.get("shortname", "")),
                        "type": res.get("quoteType", ""),
                        "exchange": res.get("exchange", ""),
                        "sector": res.get("sector", ""),
                        "industry": res.get("industry", "")
                    })
                result = {"query": query, "results": results, "count": len(results)}
            
            return [types.TextContent(type="text", text=json.dumps(result, indent=2))]
        
        elif name == "get_multiple_quotes":
            symbols = [s.upper() for s in arguments["symbols"]]
            tickers = yf.Tickers(" ".join(symbols))
            
            results = {}
            for symbol in symbols:
                try:
                    ticker = tickers.tickers[symbol]
                    info = ticker.info
                    results[symbol] = {
                        "symbol": symbol,
                        "name": info.get("longName", ""),
                        "current_price": info.get("currentPrice", 0.0),
                        "previous_close": info.get("previousClose", 0.0),
                        "change": info.get("currentPrice", 0.0) - info.get("previousClose", 0.0),
                        "change_percent": ((info.get("currentPrice", 0.0) - info.get("previousClose", 0.0)) / info.get("previousClose", 1.0)) * 100,
                        "market_cap": info.get("marketCap"),
                        "trailing_pe": info.get("trailingPE"),
                        "forward_pe": info.get("forwardPE")
                    }
                except Exception as e:
                    results[symbol] = {"error": f"Failed to get data for {symbol}: {str(e)}"}
            
            result = {"symbols": symbols, "quotes": results, "count": len(symbols)}
            return [types.TextContent(type="text", text=json.dumps(result, indent=2))]
        
        else:
            raise ValueError(f"Unknown tool: {name}")
                
    except Exception as e:
        import traceback
        error_msg = {
            "error": str(e),
            "traceback": traceback.format_exc()
        }
        return [types.TextContent(type="text", text=json.dumps(error_msg, indent=2))]

# Run the server
async def main():
    async with mcp.server.stdio.stdio_server() as (read_stream, write_stream):
        await server.run(
            read_stream,
            write_stream, 
            server.create_initialization_options()
        )

if __name__ == "__main__":
    asyncio.run(main())