import yfinance as yf

symbol = "vbl.NS"
stock = yf.Ticker(symbol)
mf_holding = stock.recommendations
recommendations_dict = mf_holding.reset_index().to_dict(orient="records")
main_recommendation = recommendations_dict[2]

buy = main_recommendation['strongBuy'] + main_recommendation['buy']
hold = main_recommendation['hold'] 
sell = main_recommendation['strongSell'] + main_recommendation['sell']

total = buy+hold+sell

buypercent = round((buy / total) * 100, 2)
print(buypercent)
holdpercent = round((hold / total) * 100, 2)
print(holdpercent)
sellpercent = round((sell / total) * 100, 2)
print(sellpercent)

# Determine recommendation
if buypercent > sellpercent and buypercent > holdpercent:
    print(f"{buypercent} BUY")
elif sellpercent > buypercent and sellpercent > holdpercent:
    print(f"{sellpercent}% SELL")
else:
    print(f"{holdpercent} HOLD")
