from fastapi import FastAPI
from .routes.auth_routes import router as auth_router
from backend.routes.stock_search import router as search_router
from backend.routes.charts import router as chart_router
from backend.routes.ipo import router as ipo_router
from backend.routes.mf_search import router as mfs_router
from backend.routes.news import router as news_router
from backend.routes.stock_etc_info import router as stockInfo_router


app = FastAPI(debug=True)

app.include_router(auth_router, prefix = '/auth')
app.include_router(search_router, prefix = '/stock')
app.include_router(chart_router, prefix = '/chart')
app.include_router(ipo_router, prefix = '/ipo')
app.include_router(mfs_router, prefix = '/mutual_funds')
app.include_router(news_router, prefix = '/news')
app.include_router(stockInfo_router, prefix = '/stockInfo')

@app.get("/")
def home():
    return{"Message":"B2B Authentication API is running"}