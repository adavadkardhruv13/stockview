from fastapi import APIRouter, Query, Depends, status
from fastapi.responses import JSONResponse
# import yfinance
from backend.auth import verify_jwt
import sys, requests, logging
import yfinance as yf
from datetime import date


router = APIRouter()
logger = logger = logging.getLogger(__name__)




@router.get("/earning/{symbol}")
async def get_stock_earnings(symbol: str):
    try:
        stock = yf.Ticker(symbol)
        income_stmt = stock.income_stmt
        # print(income_stmt)

        if income_stmt is None or income_stmt.empty:
            return JSONResponse(
                status_code=404,
                content={"detail": f"Earnings data not found for {symbol}"},
            )

        
        if "Gross Profit" not in income_stmt.index:
            return JSONResponse(
                status_code=404,
                content={"detail": f"Gross Profite data not available for {symbol}"},
            )
        
        if "Net Income" not in income_stmt.index:
            return JSONResponse(
                status_code=404,
                content={"detail": f"Net Income data not available for {symbol}"},
            )
            
        net_income = income_stmt.loc["Net Income"].to_dict()
        profit = income_stmt.loc["Gross Profit"].to_dict()


        net_income_crores = {
            str(key):  f"{round(value / 1e7, 2)} Cr" if value is not None else None
            for key, value in net_income.items()
        }
        profit_crores = {
            str(key):  f"{round(value / 1e7, 2)} Cr" if value is not None else None
            for key, value in profit.items()
        }


        net_income_subset = dict(list(net_income_crores.items())[:1])
        profit = dict(list(profit_crores.items())[:1])

        return JSONResponse(
            status_code=200,
            content={
                "status_code": 200,
                "success": True,
                "data": {
                    "net_income":net_income_subset,
                    "Gross Profit": profit
                },
                "message": f"Earnings data retrieved successfully for {symbol} (in Cr)",
            },
        )

    except Exception as e:
        logger.error(f"Error getting earnings data for {symbol}: {e}")
        return JSONResponse(
            status_code=500,
            content={
                "status_code": 500,
                "success": False,
                "data": None,
                "message": f"Internal server error: {e}",
            },
        )
        
        

# yfinance.Ticker.get_mutualfund_holders
# yfinance.Ticker.analyst_price_targets

@router.get("/recommendation/{symbol}")
async def get_recommended(symbol: str):
    try:
        stock = yf.Ticker(symbol)
        recommendations = stock.recommendations  # Fetch stock recommendations

        if recommendations is None or recommendations.empty:
            logger.warning(f"Recommendation data is not available for {symbol}")
            return JSONResponse(
                status_code=status.HTTP_404_NOT_FOUND,
                content={
                    "status_code": status.HTTP_404_NOT_FOUND,
                    "success": False,
                    "data": None,
                    "message": f"Recommendation data not found for {symbol}. Try another stock like AAPL or RELIANCE.NS.",
                },
            )

        # Convert DataFrame to JSON-serializable format
        recommendations_dict = recommendations.reset_index().to_dict(orient="records")

        return JSONResponse(
            status_code=status.HTTP_200_OK,
            content={
                "status_code": status.HTTP_200_OK,
                "success": True,
                "data": recommendations_dict,
                "message": f"Recommendation data retrieved successfully for {symbol}",
            },
        )

    except Exception as e:
        logger.error(f"Error getting recommendation data for {symbol}: {str(e)}")
        return JSONResponse(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            content={
                "status_code": status.HTTP_500_INTERNAL_SERVER_ERROR,
                "success": False,
                "data": None,
                "message": f"Internal server error: {str(e)}",
            },
        )

