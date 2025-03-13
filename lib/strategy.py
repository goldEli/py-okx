import time
from lib.market import get_kline_data

# 倍数
multiple = 0.08

# 交易对列表
symbol_list = ['BTC-USDT', 'ETH-USDT', 'SOL-USDT', 'DOGE-USDT', 'XRP-USDT', 'TRUMP-USDT']

# 是否是长上引线
def is_long_upper_shadow(data):
    # str to number
    high = float(data['high'])
    open = float(data['open'])
    close = float(data['close'])
    low = float(data['low'])
    # 1天中最高价
    high_1d = float(data['1d_high'])
    # 1天中最低价
    low_1d = float(data['1d_low'])

    h1 = 0 # 11.331
    h2 = 0 # 10.435
    if open > close:
        h1 = open
        h2 = close
    else:
        h1 = close
        h2 = open

    # 上引线长度
    upper_shadow_length = abs(high - h1) # 12.431 - 11.331 = 1.1
    # 下引线长度
    lower_shadow_length = abs(h2 - low) # 10.435 - 10.425 = 0.01

    # 上引线长度是下引线长度的5倍, 上影线是蜡烛的5倍
    # 1.1 + 11.331 = 12.431
    # 1.1 / 12.431 = 0.0884
    if high > high_1d and (upper_shadow_length / (upper_shadow_length + h1)) > multiple:
        return True

    return False    


# 是否是长下引线
def is_long_lower_shadow(data):
    high = float(data['high'])
    open = float(data['open'])
    close = float(data['close'])
    low = float(data['low'])
    
     #'high': '10.757',       # 最高价
            #'open': '10.683',       # 开盘价
            #'close': '10.726',      # 收盘价
            #'low': '8',        # 最低价
            #'1d_high': '11',    # 日最高价
            #'1d_low': '6'      # 日最低价


    # 1天中最高价
    high_1d = float(data['1d_high'])
    # 1天中最低价
    low_1d = float(data['1d_low'])

    h1 = 0 # 10.726
    h2 = 0 # 10.683
    if open > close:
        h1 = open
        h2 = close
    else:
        h1 = close
        h2 = open

    # 上引线长度
    upper_shadow_length = abs(high - h1)
    # 下引线长度
    lower_shadow_length = abs(h2 - low) # 10.726 - 8 = 2.726

    # 上引线长度是下引线长度的5倍, 上影线是蜡烛的5倍
    if low < low_1d and lower_shadow_length/(lower_shadow_length + h2) > multiple :
        return True

    return False    

class Strategy:
    def __init__(self):
        print("官式引线大法策略初始化完成")
        print("--------------------------------")
        print("监控中。。。")
        self.callback = None
    # 注册回调
    def register_callback(self, callback):
        self.callback = callback


    # 执行策略
    def run(self):
        # 每30秒获取btc数据
        while True:
            for symbol in symbol_list:
                data = get_kline_data(symbol)
                if is_long_upper_shadow(data):
                    self.callback(data, "short")
                elif is_long_lower_shadow(data):
                    self.callback(data, "long")

            time.sleep(30)

