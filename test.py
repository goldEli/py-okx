
import lib.email as email
from lib.config import get_email_info
import lib.market as market
from lib.order import place_market_order

symbol = "ETH-USDT-SWAP"
current_price = market.get_current_price(symbol)
print(current_price)

place_market_order(symbol, "long", current_price['last_price'])

