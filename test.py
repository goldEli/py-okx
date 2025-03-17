
import lib.email as email
from lib.config import get_email_info
import lib.market as market
from lib.order import place_market_order

# symbol = "ETH-USDT-SWAP"
symbol = "BTC-USDT-SWAP"
# symbol = "TRUMP-USDT-SWAP"
# symbol = "SOL-USDT-SWAP"
current_price = market.get_current_price(symbol)
print(current_price)

place_market_order(symbol, "short", current_price['last_price'])
place_market_order(symbol, "long", current_price['last_price'])

