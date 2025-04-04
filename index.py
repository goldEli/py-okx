# import okx.Trade as Trade
# import json
# import okx.Account as Account
# from lib.index import get_account_mode
# from lib.order import place_limit_order
from lib.acount import get_account_balance
from lib.strategy import Strategy
from datetime import datetime
from lib.order import place_market_order
from lib.email import send_email_for_trigger
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


# place_market_order('BTC-USDT-SWAP', 'long', 1900.11)

# 注册回调
def callback(options):

    data = options['data']
    direction = options['direction']
    amplitude = options['amplitude']
    msg = options['msg']
    # 获取时间戳
    timestamp = data['timestamp']
    # 如果时间戳在cache中，则不执行
    # if order_status['is_order'] == True:
    #     return
    if timestamp in cache:
        return
    # order_status['is_order'] = True
    version = "2.0.0"
    place_market_order(data, direction, version, amplitude)
    # 将时间戳加入cache
    cache[timestamp] = True
    print("--------------------------")
    print("官式引线大法触发")
    print(f"版本：{version}")
    print(f"策略：{msg}")
    print(f"交易对：{data['symbol']}")
    print(f"时间：{datetime.fromtimestamp(int(data['timestamp']) / 1000).strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"最新价：{data['last_price']}")
    print(f"开盘价：{data['open']}")
    print(f"最高价：{data['high']}")
    print(f"最低价：{data['low']}")
    print(f"收盘价：{data['close']}")
    # direction long print 做多，short print 做空
    print(f"方向：{'做多' if direction == 'long' else '做空'}")


strategy.register_callback(callback)

# 执行策略
strategy.run()


