import time
from lib.market import get_kline_data
from lib.config import get_symbol_list
from datetime import datetime
import threading
from lib.acount import get_account_balance

# 倍数
multiple = 0.008
# multiple = 0.001

bias = 0.97

# 交易对列表
# 'TRUMP-USDT'
symbol_list = get_symbol_list()
# symbol_list = ['ETH-USDT-SWAP']

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
        if amplitude < 0.08:
            self.amplitude = 0.003
            return
        self.amplitude = 0.005

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

        # 上引线长度是下引线长度的5倍, 上影线是蜡烛的5倍
        # 1.1 + 11.331 = 12.431
        # 1.1 / 12.431 = 0.0884
        # if high > high_1d * bias and (upper_shadow_length / (upper_shadow_length + h1)) > multiple:
        if (upper_shadow_length / high) > multiple:
            self.set_amplitude(upper_shadow_length / high)
        # if (upper_shadow_length / (upper_shadow_length + h1)) > multiple:
            return True

        return False    


    # 是否是长下引线
    def is_long_lower_shadow(self, data):
        high = float(data['high'])
        open = float(data['open'])
        close = float(data['close'])
        low = float(data['low'])

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
        # print(low * bias, low_1d, lower_shadow_length/(lower_shadow_length + h2), multiple)
        # if low * bias < low_1d  and lower_shadow_length/(lower_shadow_length + h2) > multiple :
        if lower_shadow_length/(lower_shadow_length + h2) > multiple :
            self.set_amplitude(lower_shadow_length/(lower_shadow_length + h2))
            return True

        return False    


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
                if self.is_long_upper_shadow(data):
                    self.callback(data, "short", self.amplitude)
                    self.print_kline_data(data)
                if self.is_long_lower_shadow(data):
                    self.callback(data, "long", self.amplitude)
                    self.print_kline_data(data)
            time.sleep(1)

    # print kline data
    def print_kline_data(self, data):
        print("--------------kline data------------------")
        print(f"symbol：{data['symbol']}")
        print(f"open：{data['open']}")
        print(f"close：{data['close']}")
        print(f"high：{data['high']}")
        print(f"low：{data['low']}")
        print(f"是否是上引线：{self.is_long_upper_shadow(data)}")
        print(f"是否是下引线：{self.is_long_lower_shadow(data)}")
        print(f"振幅：{self.amplitude}")
        print("--------------kline data------------------")

    def print_time(self):
        while True:
            print(f"当前时间：{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
            get_account_balance()
            time.sleep(8 * 60 * 60) # 8小时打印一次

