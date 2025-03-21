import time
from lib.market import get_kline_data
from lib.config import get_symbol_list
from datetime import datetime
import threading
from lib.acount import get_account_balance

# 倍数
multiple = 0.02
top_multiple = 0.004
top_bias = 0.998

# 交易对列表
# 'TRUMP-USDT'
symbol_list = get_symbol_list()
# symbol_list = ['ETH-USDT-SWAP']


# print strategy
def print_strategy(msg):
    print("-----------策略----------")
    print(f"策略：{msg}")
    print("-------------------------")

class Strategy:
    def __init__(self):
        print("官式引线大法策略初始化完成")
        print("--------------------------------")
        print(f"监控的交易对：{symbol_list}")
        print("监控中。。。")
        self.callback = None
        # 振幅
        self.amplitude = 0.008
        
    # 注册回调
    def register_callback(self, callback):
        self.callback = callback

    # 设置振幅
    def set_amplitude(self, amplitude):
        self.amplitude = 0.003
        # if amplitude < 0.08:
        #     self.amplitude = 0.003
        #     return
        # self.amplitude = 0.005

    # 是否是长上引线
    def is_long_upper_shadow(self, data):
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
        # 蜡烛长度
        candle_length = abs(h1 - h2) 

        # 是否有上引线
        is_upper = (upper_shadow_length / high) > top_multiple
        # 是否是顶
        is_top = high > high_1d * top_bias
        # 是否是针(上影线是蜡烛的50%)
        is_needle =  upper_shadow_length / candle_length > 0.5

        strategy1 = is_upper and is_top and is_needle
        
        strategy2 = is_top and upper_shadow_length / candle_length > 1
        # 冲顶上影线
        if strategy1 or strategy2:
            self.set_amplitude(1)
            return True, "冲顶上影线"
        
        
        if (upper_shadow_length / high) > multiple:
            self.set_amplitude(upper_shadow_length / high)
            return True, "普通上影线"

        return False, None    


    # 是否是长下引线
    def is_long_lower_shadow(self, data):
        high = float(data['high'])
        open = float(data['open'])
        close = float(data['close'])
        low = float(data['low'])
        low_1d = float(data['1d_low'])
        high_1d = float(data['1d_high'])
        candle_length = abs(open - close)

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

        # 是否有下引线
        is_lower = lower_shadow_length/(lower_shadow_length + h2) > top_multiple
        # 是否是底
        is_bottom = low < low_1d * top_bias
        # 是否是针(下影线是蜡烛的50%)
        is_needle = lower_shadow_length / candle_length > 0.5

        strategy1 = is_lower and is_bottom and is_needle

        strategy2 = is_bottom and lower_shadow_length / candle_length > 1
        # 冲底下影线 
        if strategy1 or strategy2:
            self.set_amplitude(1)
            return True, "冲底下影线"

        # 普通下影线
        if lower_shadow_length/(lower_shadow_length + h2) > multiple:
            self.set_amplitude(lower_shadow_length/(lower_shadow_length + h2))
            return True, "普通下影线"

        return False, None    


    # 执行策略
    def run(self):

        # 每小时打印一次时间
        threading.Thread(target=self.print_time).start()
        # 每30秒获取btc数据
        while True:
            for symbol in symbol_list:
                data = get_kline_data(symbol)
                if data is None:
                    continue
                is_long_upper_shadow, msg = self.is_long_upper_shadow(data)
                if is_long_upper_shadow:
                    self.callback({'data': data, 'direction': "short", 'amplitude': self.amplitude, 'msg': msg})
                is_long_lower_shadow, msg = self.is_long_lower_shadow(data)
                if is_long_lower_shadow:
                    self.callback({'data': data, 'direction': "long", 'amplitude': self.amplitude, 'msg': msg})
            time.sleep(1)


    def print_time(self):
        while True:
            print(f"当前时间：{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
            get_account_balance()
            time.sleep(1 * 60 * 60) # 8小时打印一次

