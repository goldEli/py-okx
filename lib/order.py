import okx.Trade as Trade
import okx.Account as Account
from lib.config import get_okx_info
from lib.config import get_coin_config
# from lib.email import send_email_for_trade
from lib.market import get_price_precision
api_key, secret_key, passphrase, flag = get_okx_info()

# print(api_key, secret_key, passphrase, flag)

trade_api = Trade.TradeAPI(api_key, secret_key, passphrase, flag=flag)  

account_api = Account.AccountAPI(api_key, secret_key, passphrase, flag=flag)

# 下限价委托单
def place_limit_order():
   # limit order
   result = trade_api.place_order(
           instId="BTC-USDT-SWAP",
           tdMode="isolated",
           side="buy",
           posSide="long",
           ordType="market",
           # 止盈
           tpOrdPx="100000",
           tpTriggerPx="100000",
           # 止损
           slOrdPx="60000",
           slTriggerPx="60000",
           sz="0.01"
   )
   print(result)

   if result["code"] == "0":
          print("Successful order request，order_id = ",result["data"][0]["ordId"])
   else:
          print("Unsuccessful order request，error_code = ",result["data"][0]["sCode"], ", Error_message = ", result["data"][0]["sMsg"])

# 获取止盈和止损
def get_tp_sl(s, last_price, amplitude):
       if s == "long":
              tpOrdPx = last_price * (1 + amplitude)
              slOrdPx = last_price * (1 - amplitude)
       else:
              tpOrdPx = last_price * (1 - amplitude)
              slOrdPx = last_price * (1 + amplitude)
       return tpOrdPx, slOrdPx

# 下市价委托单
def place_market_order(symbol, s, last_price, amplitude=0.008):
   side = "buy" if s == "long" else "sell"
   posSide = "long" if s == "long" else "short"
   sz = get_coin_config()[symbol]["sz"]

   tpOrdPx, slOrdPx = get_tp_sl(s, last_price, amplitude)

   price_precision = get_price_precision(symbol)

   # 一位小数
   tpOrdPx = round(tpOrdPx, price_precision)
   slOrdPx = round(slOrdPx, price_precision)

   print("开始下单:", symbol, s, last_price, sz)
   print("side", side)
   print("posSide", posSide)
   print("tpOrdPx", tpOrdPx)
   print("slOrdPx", slOrdPx)
   print("--------------------------------")

#    send_email_for_trade(last_price, slOrdPx, tpOrdPx, side, symbol)

   # limit order
   result = trade_api.place_order(
       instId=symbol,
       tdMode="isolated",
       side=side,
       posSide=posSide,
       ordType="market",
       # 止盈
       tpOrdPx=tpOrdPx,
       tpTriggerPx=tpOrdPx,
       # 止损
       slOrdPx=slOrdPx,
       slTriggerPx=slOrdPx,
       sz=sz
       #     pxUsdt="100",
   )
   print(result)

   if result["code"] == "0":
          print("Successful order request，order_id = ",result["data"][0]["ordId"])
   else:
          print("Unsuccessful order request，error_code = ",result["data"][0]["sCode"], ", Error_message = ", result["data"][0]["sMsg"])