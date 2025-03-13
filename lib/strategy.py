import time
from lib.market import get_btc_data

# 倍数
multiple = 5

# 是否是长上引线
def is_long_upper_shadow(data):
    # str to number
    high = float(data['high'])
    open = float(data['open'])
    close = float(data['close'])
    low = float(data['low'])

    h1 = 0
    h2 = 0
    if open > close:
        h1 = open
        h2 = close
    else:
        h1 = close
        h2 = open

    # 上引线长度
    upper_shadow_length = abs(high - h1)
    # 下引线长度
    lower_shadow_length = abs(h2 - low)
    # 蜡烛长度取绝对值
    candle_length = abs(open - close)

    # 上引线长度是下引线长度的5倍, 上影线是蜡烛的5倍
    if upper_shadow_length > lower_shadow_length * multiple and upper_shadow_length > candle_length * multiple:
        return True

    return False    


# 是否是长下引线
def is_long_lower_shadow(data):
    high = float(data['high'])
    open = float(data['open'])
    close = float(data['close'])
    low = float(data['low'])


    h1 = 0
    h2 = 0
    if open > close:
        h1 = open
        h2 = close
    else:
        h1 = close
        h2 = open

    # 下引线长度
    lower_shadow_length =  abs(h2 - low) # 50
    # 上引线长度
    upper_shadow_length = abs(high - h1) # 10
    # 蜡烛长度
    candle_length = abs(close - open) # 10

    # 上引线长度是下引线长度的5倍, 上影线是蜡烛的5倍
    if lower_shadow_length > upper_shadow_length * multiple and lower_shadow_length > candle_length * multiple:
        return True

    return False    

class Strategy:
    def __init__(self):
        print("官式引线大法策略初始化完成")
        print("策略描述：")
        print("1. 每30秒获取btc数据")
        print("2. 判断是否出现长上引线")
        print("3. 判断是否出现长下引线")
        print("4. 如果出现长上引线，则空单")
        print("5. 如果出现长下引线，则多单")
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
            data = get_btc_data()
            timeStamp, open, high, low, close, volume, turn_over, turn_over_rate, count = data
            if is_long_upper_shadow({'high': high, 'open': open, 'close': close, 'low': low}):
                self.callback(data, "short")

            if is_long_lower_shadow({'high': high, 'open': open, 'close': close, 'low': low}):
                self.callback(data, "long")

            time.sleep(30)

