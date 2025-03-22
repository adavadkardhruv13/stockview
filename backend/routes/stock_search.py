from fastapi import APIRouter, Query, Depends, status
from fastapi.responses import JSONResponse
# import yfinance
from backend.auth import verify_jwt
import sys, requests, logging
sys.path.append(r"E:\stockview\venv\Lib\site-packages")
import yfinance as yf


router = APIRouter()


logger = logging.getLogger(__name__)

@router.get("/{symbol}")
# async def get_stock_data(symbol: str, user_email: str = Depends(verify_jwt)):
async def get_stock_data(symbol: str):
    try:
        stock = yf.Ticker(symbol)
        stock_info = stock.info
        
        
        if not stock_info:
            return JSONResponse(
                status_code=status.HTTP_404_NOT_FOUND,
                content={
                    "status_code": status.HTTP_404_NOT_FOUND,
                    "success": False,
                    "data": None,
                    "message": f"Stock {symbol} not found"
                }
            )
        
        response_data = {
            "company_name": stock_info.get("longName", "N/A"),
            "symbol": stock_info.get("symbol", "N/A"),
            "current_price": stock_info.get("currentPrice", "N/A"),
            "previous_close": stock_info.get("previousClose", "N/A"),
            "market_cap": stock_info.get("marketCap", "N/A"),
            "sector": stock_info.get("sector", "N/A"),
            "industry": stock_info.get("industry", "N/A"),
            "logo_url": stock_info.get("logo_url", ""),
            "52_week_high": stock_info.get("fiftyTwoWeekHigh", "N/A"),
            "52_week_low": stock_info.get("fiftyTwoWeekLow", "N/A"),
            "pe_ratio": stock_info.get("trailingPE", "N/A"),
            "dividendRate": stock_info.get("dividendRate", "N/A"),
        }
        
        return JSONResponse(
            status_code = status.HTTP_200_OK,
            content = {
                "status_code": status.HTTP_200_OK,
                "success": True,
                "data": response_data,
                "message": "Stock data retrieved successfully"
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
                    "message": f"Stock {symbol} not found"
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
    

@router.get("/dividend/{symbol}")
# async def get_stock_dividend(symbol:str, user_email: str= Depends(verify_jwt)):
async def get_stock_dividend(symbol:str):
    try:
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
        
    
@router.get("/history/{symbol}")
# async def get_stock_history(symbol:str, period:str = Query ('1mo', regex="^(1d|5d|1mo|3mo|6mo|1y|2y|5y|10y|ytd|max)$"), user_email: str = Depends(verify_jwt)):
async def get_stock_history(symbol:str, period:str = Query ('1mo', regex="^(1d|5d|1mo|3mo|6mo|1y|2y|5y|10y|ytd|max)$")):
    try:
        stock = yf.Ticker(symbol)
        history = stock.history(period=period)
        
        if history.empty:
            return JSONResponse(status_code=404, content={'detail':"No historical data found"})
        
        return {
            "symbol": symbol,
            "dates": history.index.strftime("%Y-%m-%d").tolist(),
            "open": history["Open"].tolist(),
            "high": history["High"].tolist(),
            "low": history["Low"].tolist(),
            "close": history["Close"].tolist(),
            "volume": history["Volume"].tolist()
        }
    except Exception as e:
        return JSONResponse(status_code=500, content={'details':str(e)})


@router.get("/impindex/")
# async def get_index( user_email: str= Depends(verify_jwt)):
async def get_index():
    try:
        tickers = {
            "Nifty 50": "^NSEI",
            "Sensex": "^BSESN",
            "Bank Nifty": "^NSEBANK",
            "USD/INR": "USDINR",
        }

        def get_price(ticker_symbol):
            try:
                ticker = yf.Ticker(ticker_symbol)
                history = ticker.history(period="1d")
                if history.empty:
                    return None  # Return None if no data
                return round(history["Close"].iloc[-1], 2)
            except Exception as e:
                logger.error(f"Error fetching price for {ticker_symbol}: {e}")
                return None

        def get_previous_close(ticker_symbol):
            try:
                ticker = yf.Ticker(ticker_symbol)
                prev_close = ticker.info.get("previousClose", 0)
                return round(prev_close, 2) if prev_close else None
            except Exception as e:
                logger.error(f"Error fetching previous close for {ticker_symbol}: {e}")
                return None

        def calculate_change(current, prev):
            if current is None or prev is None or prev == 0:
                return "N/A"
            return round(((current - prev) / prev) * 100, 2)

        response_data = {}
        for name, symbol in tickers.items():
            price = get_price(symbol)
            prev_close = get_previous_close(symbol)

            if price is not None and prev_close is not None:
                response_data[name] = {"Price": price, "Change (%)": calculate_change(price, prev_close)}
            else:
                response_data[name] = {"Price": "N/A", "Change (%)": "N/A"}

        return JSONResponse(
            status_code=status.HTTP_200_OK,
            content={
                "status_code": status.HTTP_200_OK,
                "success": True,
                "data": response_data,
                "message": "Index data retrieved successfully"
            }
        )

    except Exception as e:
        logger.error(f"Error fetching index data: {e}")
        return JSONResponse(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            content={
                "status_code": status.HTTP_500_INTERNAL_SERVER_ERROR,
                "success": False,
                "data": None,
                "message": f"Internal server error: {e}"
            }
        )




        