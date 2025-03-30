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
three_days_date = (date.today() - timedelta(days=3)).strftime('%Y-%m-%d')

@router.get("/")
def get_sm_news():
    try:
        
        url = f"https://newsapi.org/v2/everything?q=India+stock+market+NSE+BSE&from={three_days_date}&to={today_date}&sortBy=publishedAt&apiKey={NEWS_API_KEY}"
        
        print(url)
        response = requests.get(url)
        news_data = response.json()
        
        if "articles" not in news_data:
            return JSONResponse(status_code=500, content={"detail": "Error fetching news"})
        
        articles=[]
        
        for article in news_data['articles'][:15]:
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
        # Get company name from yfinance
        try:
            stock = yf.Ticker(symbol)
            company_name = stock.info.get("longName") or stock.info.get("shortName") or symbol # Use symbol as fallback
        except Exception as yf_error:
            print(f"yfinance error for {symbol}: {yf_error}")
            company_name = symbol #use the symbol as a fallback.

        if not company_name:
            company_name = symbol #use the symbol as a fallback.

        # Refine query for Indian stocks
        india_market_keywords = "India stock market NSE BSE Sensex Nifty"
        query = f"{company_name} {india_market_keywords}"

        url = f"https://newsapi.org/v2/everything?q={query}&sortBy=publishedAt&apiKey={NEWS_API_KEY}"
        response = requests.get(url)
        news_data = response.json()

        if "articles" not in news_data:
            return JSONResponse(status_code=500, content={"detail": "Error fetching news"})

        articles = []

        for article_data in news_data['articles'][:4]:
            articles.append({
                "title": article_data.get("title", "No Title"),
                "description": article_data.get("description", "No Description"),
                "url": article_data.get("url", "#"),
                "image": article_data.get("urlToImage", ""),
                "published_at": article_data.get("publishedAt", ""),
                "source": article_data["source"].get("name", "Unknown Source"),
            })

        return JSONResponse(content={"news": articles})

    except Exception as e:
        return JSONResponse(status_code=500, content={"detail": str(e)})
#     try:
        
#         if "." not in symbol:
#             symbol += ".NS"
            
            
#         stock = yf.Ticker(symbol)
#         news = stock.news

#         if not news:
#             return JSONResponse(
#                 status_code=status.HTTP_404_NOT_FOUND,
#                 content={
#                     "status_code": status.HTTP_404_NOT_FOUND,
#                     "success": False,
#                     "data": None,
#                     "message": f"News for stock {symbol} not found",
#                 },
#             )

#         return JSONResponse(
#             status_code=status.HTTP_200_OK,
#             content={
#                 "status_code": status.HTTP_200_OK,
#                 "success": True,
#                 "data": news,
#                 "message": f"News for stock {symbol} retrieved successfully",
#             },
#         )

#     except Exception as e:
#         logger.error(f"Error fetching news for {symbol}: {e}")
#         error_message = str(e)

#         if "404 Client Error" in error_message:
#             return JSONResponse(
#                 status_code=status.HTTP_404_NOT_FOUND,
#                 content={
#                     "status_code": status.HTTP_404_NOT_FOUND,
#                     "success": False,
#                     "data": None,
#                     "message": f"News for stock {symbol} not found",
#                 },
#             )

#         return JSONResponse(
#             status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
#             content={
#                 "status_code": status.HTTP_500_INTERNAL_SERVER_ERROR,
#                 "success": False,
#                 "data": None,
#                 "message": "Internal server error",
#             },
#         )
