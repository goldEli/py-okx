# import okx.Trade as Trade
# import json
# import okx.Account as Account
# from lib.index import get_account_mode
# from lib.order import place_limit_order
from lib.acount import get_account_balance
from lib.strategy import Strategy
from datetime import datetime
from lib.order import place_market_order

# get_account_balance()

# 创建策略
strategy = Strategy()   

# cache key 为时间戳 value 为 true
cache = {}

# place_market_order('BTC-USDT-SWAP', 'long')

# 是否已经下单
order_status = {
    'is_order': False
}

# 注册回调
def callback(data, direction):
    # 获取时间戳
    timestamp = data['timestamp']
    # 如果时间戳在cache中，则不执行
    if order_status['is_order'] == True:
        return
    if timestamp in cache:
        return
    order_status['is_order'] = True
    # 将时间戳加入cache
    cache[timestamp] = True
    place_market_order(data['symbol'], direction, data['last_price'])
    print("--------------------------")
    print("官式引线大法触发")
    print(f"交易对：{data['symbol']}")
    print(f"时间：{datetime.fromtimestamp(int(data['timestamp']) / 1000).strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"开盘价：{data['open']}")
    print(f"最高价：{data['high']}")
    print(f"最低价：{data['low']}")
    print(f"收盘价：{data['close']}")
    # direction long print 做多，short print 做空
    print(f"方向：{'做多' if direction == 'long' else '做空'}")


strategy.register_callback(callback)

# 执行策略
strategy.run()


