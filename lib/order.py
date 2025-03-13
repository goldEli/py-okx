import okx.Trade as Trade
import okx.Account as Account
from lib.config import get_okx_info
from lib.config import get_coin_config

api_key, secret_key, passphrase, flag = get_okx_info()

trade_api = Trade.TradeAPI(api_key, secret_key, passphrase, flag)  # test=True 为模拟交易

account_api = Account.AccountAPI(api_key, secret_key, passphrase, flag)

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


# 下市价委托单
def place_market_order(symbol, s, last_price):
   side = "buy" if s == "long" else "sell"
   posSide = "long" if s == "long" else "short"
   sz = get_coin_config()[symbol]["sz"]
   print("开始下单:", symbol, s, last_price, sz)

   tpOrdPx = last_price * 1.1 if s == "long" else last_price * 0.9
   slOrdPx = last_price * 0.9 if s == "long" else last_price * 1.1

   # 一位小数
   tpOrdPx = round(tpOrdPx, 1)
   slOrdPx = round(slOrdPx, 1)

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