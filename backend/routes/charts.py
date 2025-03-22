import sys
import matplotlib.pyplot as plt
sys.path.append(r"E:\vault\venv\Lib\site-packages")
import plotly.graph_objects as go
from io import BytesIO
import base64
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi import APIRouter
import yfinance as yf
import requests

router = APIRouter()

@router.get('/{symbol}')
def get_stock_chart(symbol: str, period:str = '1mo'):
    try:
        stock = yf.Ticker(symbol)
        history = stock.history(period=period)
        
        if history.empty:
            return JSONResponse(status_code=404, content={'detail':'No history found'})
        
        fig = go.Figure(
            data = [go.Candlestick(
                x=history.index,
                open=history["Open"],
                high=history["High"],
                low=history["Low"],
                close=history["Close"]
                
            )]
        )
        
        fig.update_layout(title=f"{symbol} Stock Price", xaxis_title = "Date", yaxis_title="Price")
        return HTMLResponse(fig.to_html())
    
    except Exception as e:
        return JSONResponse(status_code=500,content={'detail':str(e)}) 
    
@router.get("/moving-average/{symbol}")
def get_moving_average_chart(symbol:str, period:str = "6mo"):
    try:
        stock = yf.Ticker(symbol)
        history = stock.history(period = period)
        
        if history.empty:
            return JSONResponse(status_code=404, content={'detail':'No history found'})
        
        
        history["MA50"] = history["Close"].rolling(window=50).mean()
        history["MA200"] = history["Close"].rolling(window=200).mean()
        
        plt.plot(history["Close"], color = 'blue', label = 'Stock Price')
        plt.plot(history["MA50"], color = 'orange', label = '50 Days MA', linestyle = "--")
        plt.plot(history["MA200"], color = 'black', label = '200 Days MA', linestyle = "--")
        plt.legend()
        plt.title(f"{symbol} Moving Day Average")
        plt.xlabel("Days")
        plt.ylabel("Price")
        
        buffer = BytesIO()
        plt.savefig(buffer, format="png")
        buffer.seek(0)
        img_base64 = base64.b64encode(buffer.getvalue()).decode()
        plt.close()

        # Generate HTML Response
        html_content = f"""
        <html>
        <head>
            <title>{symbol} Moving Average Chart</title>
        </head>
        <body>
            <h2>{symbol} Moving Average Chart ({period})</h2>
            <img src="data:image/png;base64,{img_base64}" alt="Moving Average Chart">
        </body>
        </html>
        """

        return HTMLResponse(content=html_content)


    except Exception as e:
        return JSONResponse(status_code=500, content={"detail": str(e)})
    


