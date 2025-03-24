from fastapi import APIRouter, Query, Depends, status, WebSocket, WebSocketDisconnect
from fastapi.responses import JSONResponse
from backend.auth import verify_jwt
import sys, requests, logging, asyncio
sys.path.append(r"E:\stockview\venv\Lib\site-packages")
import yfinance as yf
from datetime import date


router = APIRouter()


logger = logging.getLogger(__name__)

def convert_market_cap_to_cr(market_cap: int) -> str:
    """Converts market cap to crores (Cr) with appropriate formatting."""
    if market_cap is None or market_cap == "N/A":
        return "N/A"

    try:
        market_cap = int(market_cap)  
        billion = market_cap / 1000000000  
        return f"{billion:.2f} Bi"  
    except (ValueError, TypeError):
        return "N/A"  

@router.websocket("/{symbol}")
async def get_stock_data(websocket: WebSocket, symbol: str):
    """WebSocket endpoint to fetch live stock data every second."""
    
    await websocket.accept()

    if "." not in symbol:
        symbol += ".NS"

    try:
        while True:
            stock = yf.Ticker(symbol)
            stock_info = stock.info

            if not stock_info:
                await websocket.send_json({
                    "status_code": 404,
                    "success": False,
                    "data": None,
                    "message": f"Stock {symbol} not found"
                })
                await asyncio.sleep(1)
                continue  # Retry after 1 second

            market_cap_cr = convert_market_cap_to_cr(stock_info.get("marketCap"))

            response_data = {
                "company_name": stock_info.get("longName", "N/A"),
                "symbol": stock_info.get("symbol", "N/A"),
                "current_price": stock_info.get("currentPrice", "N/A"),
                "previous_close": stock_info.get("previousClose", "N/A"),
                "market_cap": market_cap_cr,
                "sector": stock_info.get("sector", "N/A"),
                "industry": stock_info.get("industry", "N/A"),
                "logo_url": stock_info.get("logo_url", ""),
                "52_week_high": stock_info.get("fiftyTwoWeekHigh", "N/A"),
                "52_week_low": stock_info.get("fiftyTwoWeekLow", "N/A"),
                "pe_ratio": stock_info.get("trailingPE", "N/A"),
                "dividendRate": stock_info.get("dividendRate", "N/A"),
            }

            await websocket.send_json({
                "status_code": 200,
                "success": True,
                "data": response_data,
                "message": "Real-time stock data update"
            })

            await asyncio.sleep(1)  # Fetch data every second

    except WebSocketDisconnect:
        logger.info(f"Client disconnected from {symbol}")

    except Exception as e:
        logger.error(f"Error fetching stock data for {symbol}: {e}")

        await websocket.send_json({
            "status_code": 500,
            "success": False,
            "data": None,
            "message": "Internal server error",
        })
    

@router.get("/dividend/{symbol}")
# async def get_stock_dividend(symbol:str, user_email: str= Depends(verify_jwt)):
async def get_stock_dividend(symbol:str):
    try:
        
        if "." not in symbol:
            symbol += ".NS"
            
        stock = yf.Ticker(symbol)
        stock_info = stock.info
        
        if not stock_info:
            return JSONResponse(
                status_code=status.HTTP_404_NOT_FOUND,
                content={
                    "status_code": status.HTTP_404_NOT_FOUND,
                    "success": False,
                    "data": None,
                    "message": f"Stock {symbol} Dividend History not found"
                }
            )
            
        response_data={
            "dividend_yield": stock_info.get("dividendYield", "N/A"),
            "last_dividend": stock_info.get("lastDividendValue", "N/A"),
            "dividend_history": stock.dividends.to_dict()
        }
        
        return JSONResponse(
            status_code = status.HTTP_200_OK,
            content = {
                "status_code": status.HTTP_200_OK,
                "success": True,
                "data": response_data,
                "message": "Stock dividend data retrieved successfully"
            },
        )
        
        
    except Exception as e:
        logger.error(f"Error fetching stock data for {symbol}: {e}")
        error_message = str(e)

        if "404 Client Error" in error_message:
            return JSONResponse(
                status_code=status.HTTP_404_NOT_FOUND,
                content={
                    "status_code": status.HTTP_404_NOT_FOUND,
                    "success": False,
                    "data": None,
                    "message": f"Stock {symbol} dividend historynot found"
                }
            )

        return JSONResponse(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            content={
                "status_code": status.HTTP_500_INTERNAL_SERVER_ERROR,
                "success": False,
                "data": None,
                "message": "Internal server error",
            },
        )
        


def get_interval(period: str):
    if period in ['1d', '5d']:
        return "1m"
    elif period in ['1mo', '3mo', '6mo']:
        return "1d"
    else:
        return "1d" 
    
    
@router.get("/history/{symbol}")
# async def get_stock_history(symbol:str, period:str = Query ('1mo', regex="^(1d|5d|1mo|3mo|6mo|1y|2y|5y|10y|ytd|max)$"), user_email: str = Depends(verify_jwt)):
async def get_stock_history(symbol:str, period:str = Query ('1d', regex="^(1d|5d|1mo|3mo|6mo|1y|2y|5y)$")):
    try:
        
        if "." not in symbol:
            symbol += ".NS"
            
        stock = yf.Ticker(symbol)
        interval = get_interval(period)
        history = stock.history(period=period, interval=interval)
        
        if history.empty:
            return JSONResponse(status_code=404, content={'detail':"No historical data found"})
        
        return {
            "symbol": symbol,
            "dates": history.index.strftime("%Y-%m-%d %H:%M:%S").tolist(),
            "open": [round(x,2) for x in history["Open"].tolist()],
            "high": [round(x,2) for x in history["High"].tolist()],
            "low": [round(x,2) for x in history["Low"].tolist()],
            "close": [round(x,2) for x in history["Close"].tolist()], #use this data for creating line chart
            "volume": [round(x,2) for x in history["Volume"].tolist()]
        }
    except Exception as e:
        return JSONResponse(status_code=500, content={'details':str(e)})


@router.websocket("/impindex/")
# async def get_index( user_email: str= Depends(verify_jwt)):
async def get_index(websocket: WebSocket):
    await websocket.accept()
    try:
        tickers = {
            "Nifty 50": "^NSEI",
            "Sensex": "^BSESN",
            "Bank Nifty": "^NSEBANK",
            "USD/INR": "USDINR=X",
            "India VIX": "^INDIAVIX",
            "Nifty IT": "^CNXIT",
            "Nifty Auto": "^CNXAUTO",
            # "Gold MXC": "^GOLDM.NS",
            # "Silver MCX": "^SILVERM.NS",
        }

        async def get_price(ticker_symbol):
            try:
                loop = asyncio.get_event_loop()
                ticker = await loop.run_in_executor(None, lambda: yf.Ticker(ticker_symbol))
                history = await loop.run_in_executor(None, lambda: ticker.history(period="1d"))
                
                if history.empty:
                    return None
                return round(history["Close"].iloc[-1], 2)
            except Exception as e:
                logger.error(f"Error fetching price for {ticker_symbol}: {e}")
                return None

        async def get_previous_close(ticker_symbol):
            try:
                loop = asyncio.get_event_loop()
                ticker = await loop.run_in_executor(None, lambda: yf.Ticker(ticker_symbol))
                info = await loop.run_in_executor(None, lambda: ticker.info)
                prev_close = info.get("previousClose", 0)
                
                return round(prev_close, 2) if prev_close else None
            except Exception as e:
                logger.error(f"Error fetching previous close for {ticker_symbol}: {e}")
                return None

        def calculate_change(current, prev):
            if current is None or prev is None or prev == 0:
                return "N/A"
            return round(((current - prev) / prev) * 100, 2)

        while True:
            response_data = {}
            for name, symbol in tickers.items():
                price = await get_price(symbol)
                prev_close = await get_previous_close(symbol)

                if price is not None and prev_close is not None:
                    response_data[name] = {
                        "Price": price,
                        "Change (%)": calculate_change(price, prev_close)
                    }
                else:
                    response_data[name] = {
                        "Price": "N/A",
                        "Change (%)": "N/A"
                    }

            await websocket.send_json({
                "status_code": 200,
                "success": True,
                "data": response_data,
                "message": "Index data retrieved successfully"
            })
            
            await asyncio.sleep(1)  # Keep sending data every second

    except Exception as e:
        logger.error(f"Error fetching index data: {e}")
        await websocket.send_json({
            "status_code": 500,
            "success": False,
            "data": None,
            "message": f"Internal server error: {e}"
        })



        
    