import okx.Trade as Trade
from lib.config import get_okx_info

api_key, secret_key, passphrase, flag = get_okx_info()

trade_api = Trade.TradeAPI(api_key, secret_key, passphrase, flag)  # test=True 为模拟交易

# 下限价委托单
def place_limit_order():
   # limit order
   result = trade_api.place_order(
           instId="BTC-USDT",
           tdMode="cash",
           side="buy",
           ordType="limit",
           px="19000",
           sz="0.01"
   )
   print(result)

   if result["code"] == "0":
          print("Successful order request，order_id = ",result["data"][0]["ordId"])
   else:
          print("Unsuccessful order request，error_code = ",result["data"][0]["sCode"], ", Error_message = ", result["data"][0]["sMsg"])