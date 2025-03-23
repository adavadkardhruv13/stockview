from fastapi import APIRouter, status, Depends
from fastapi.responses import JSONResponse
import requests, os, logging
from dotenv import load_dotenv
from datetime import date, timedelta
import yfinance as yf


router = APIRouter()
load_dotenv()
logger = logging.getLogger(__name__)

NEWS_API_KEY = os.getenv("NEWS_API_KEY")
today_date = date.today().strftime('%Y-%m-%d')
two_days_date = (date.today() - timedelta(days=2)).strftime('%Y-%m-%d')

@router.get("/")
def get_sm_news():
    try:
        
        url = f"https://newsapi.org/v2/everything?q=india+stock+market+nse+bse&from={two_days_date}&to={today_date}&sortBy=publishedAt&apiKey={NEWS_API_KEY}"
        # url=""
        print(url)
        response = requests.get(url)
        news_data = response.json()
        
        if "articles" not in news_data:
            return JSONResponse(status_code=500, content={"detail": "Error fetching news"})
        
        articles=[]
        
        for article in news_data['articles'][:10]:
            articles.append({
                "title": article.get("title", "No Title"),
                "description": article.get("description", "No Description"),
                "url": article.get("url", "#"),
                "image": article.get("urlToImage", ""),
                "published_at": article.get("publishedAt", ""),
                "source": article["source"].get("name", "Unknown Source"),
            })
            
        return JSONResponse(content={"news":articles})
    
    except Exception as e:
        return JSONResponse(status_code=500, content={"detail": str(e)})



@router.get("/news_per_Stock/{symbol}")
async def get_stock_news(symbol: str):
    try:
        
        if "." not in symbol:
            symbol += ".NS"
            
            
        stock = yf.Ticker(symbol)
        news = stock.news

        if not news:
            return JSONResponse(
                status_code=status.HTTP_404_NOT_FOUND,
                content={
                    "status_code": status.HTTP_404_NOT_FOUND,
                    "success": False,
                    "data": None,
                    "message": f"News for stock {symbol} not found",
                },
            )

        return JSONResponse(
            status_code=status.HTTP_200_OK,
            content={
                "status_code": status.HTTP_200_OK,
                "success": True,
                "data": news,
                "message": f"News for stock {symbol} retrieved successfully",
            },
        )

    except Exception as e:
        logger.error(f"Error fetching news for {symbol}: {e}")
        error_message = str(e)

        if "404 Client Error" in error_message:
            return JSONResponse(
                status_code=status.HTTP_404_NOT_FOUND,
                content={
                    "status_code": status.HTTP_404_NOT_FOUND,
                    "success": False,
                    "data": None,
                    "message": f"News for stock {symbol} not found",
                },
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
