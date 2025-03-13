# import okx.Trade as Trade
# import json
# import okx.Account as Account
# from lib.index import get_account_mode
# from lib.order import place_limit_order
# from lib.acount import get_account_balance
from lib.strategy import Strategy
from datetime import datetime

# 创建策略
strategy = Strategy()   

# 注册回调
def callback(data, direction):
    timeStamp, open, high, low, close, volume, turn_over, turn_over_rate, count = data
    print("--------------------------")
    print("官式引线大法触发")
    print(f"时间：{datetime.fromtimestamp(int(timeStamp) / 1000).strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"开盘价：{open}")
    print(f"最高价：{high}")
    print(f"最低价：{low}")
    print(f"收盘价：{close}")
    # direction long print 做多，short print 做空
    print(f"方向：{'做多' if direction == 'long' else '做空'}")
strategy.register_callback(callback)

# 执行策略
strategy.run()


