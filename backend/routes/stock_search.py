from fastapi import APIRouter, Query, Depends
from fastapi.responses import JSONResponse
# import yfinance
from backend.auth import verify_jwt
import sys, requests
sys.path.append(r"E:\stockview\venv\Lib\site-packages")
import yfinance as yf


router = APIRouter()


@router.get("/{symbol}")
async def get_stock_data(symbol: str, user_email: str = Depends(verify_jwt)):
    try:
        stock = yf.Ticker(symbol)
        stock_info = stock.info
        
        
        if not stock_info:
            return JSONResponse(status_code=404, content={"detail":"Stock not found"})
        
        return{
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
        
    except Exception as e:
        return JSONResponse(status_code=500, content={"detail":str(e)})
    

@router.get("/dividend/{symbol}")
async def get_stock_dividend(symbol:str, user_email: str= Depends(verify_jwt)):
    try:
        stock = yf.Ticker(symbol)
        stock_info = stock.info
        
        if not stock_info:
            return JSONResponse(status_code=404, content={"detail":"Stock dividend history not found"})
        return{
            "dividend_yield": stock_info.get("dividendYield", "N/A"),
            "last_dividend": stock_info.get("lastDividendValue", "N/A"),
            "dividend_history": stock.dividends.to_dict()
        }
    except Exception as e:
        return JSONResponse(status_code=500, content={"detail":str(e)})
        
    
@router.get("/history/{symbol}")
async def get_stock_history(symbol:str, period:str = Query ('1mo', regex="^(1d|5d|1mo|3mo|6mo|1y|2y|5y|10y|ytd|max)$"), user_email: str = Depends(verify_jwt)):
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
async def get_index( user_email: str= Depends(verify_jwt)):
    try:
        nifty50 = yf.Ticker("^NSEI")
        sensex = yf.Ticker("^BSESN")
        bank_nifty = yf.Ticker("^NSEBANK")
        usd_inr = yf.Ticker("USDINR=X")
        
        nifty_price = round(nifty50.history(period="1d")["Close"].iloc[-1], 2)
        sensex_price = round(sensex.history(period="1d")["Close"].iloc[-1], 2)
        bank_nifty_price = round(bank_nifty.history(period="1d")["Close"].iloc[-1], 2)
        usd_inr_price = round(usd_inr.history(period="1d")["Close"].iloc[-1], 2)
        
        nifty_prev_close = round(nifty50.info.get("previousClose", 0), 2)
        sensex_prev_close = round(sensex.info.get("previousClose", 0), 2)
        bank_nifty_prev_close = round(bank_nifty.info.get("previousClose", 0), 2)
        usd_inr_prev_close = round(usd_inr.info.get("previousClose", 0), 2)

        # Calculate percentage change
        def calculate_change(current, prev):
            return round(((current - prev) / prev) * 100, 2) if prev else "N/A"

        return {
            "Nifty 50": {"Price": nifty_price, "Change (%)": calculate_change(nifty_price, nifty_prev_close)},
            "Sensex": {"Price": sensex_price, "Change (%)": calculate_change(sensex_price, sensex_prev_close)},
            "Bank Nifty": {"Price": bank_nifty_price, "Change (%)": calculate_change(bank_nifty_price, bank_nifty_prev_close)},
            "USD/INR": {"Price": usd_inr_price, "Change (%)": calculate_change(usd_inr_price, usd_inr_prev_close)}
        }
        
    except Exception as e:
        return JSONResponse(status_code=500, content={"detail":str(e)})
    




        