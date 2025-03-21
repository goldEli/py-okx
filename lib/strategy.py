import time
from lib.market import get_kline_data
from lib.config import get_symbol_list
from datetime import datetime
import threading
from lib.acount import get_account_balance
from lib.strategy_utils import is_top_upper_strategy, is_normal_upper_strategy, is_bottom_lower_strategy, is_normal_lower_strategy

# 倍数
multiple = 0.02
top_multiple = 0.004
top_bias = 0.998

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
    def set_amplitude(self):
        self.amplitude = 0.003
        # if amplitude < 0.08:
        #     self.amplitude = 0.003
        #     return
        # self.amplitude = 0.005

    # 是否是长上引线
    def is_long_upper_shadow(self, data):

        # 冲顶上影线
        if is_top_upper_strategy(data):
            self.set_amplitude()
            return True, "冲顶上影线"
        
        
        if is_normal_upper_strategy(data):
            self.set_amplitude()
            return True, "普通上影线"

        return False, None    


    # 是否是长下引线
    def is_long_lower_shadow(self, data):

        # 冲底下影线 
        if is_bottom_lower_strategy(data):
            self.set_amplitude()
            return True, "冲底下影线"

        # 普通下影线
        if is_normal_lower_strategy(data):
            self.set_amplitude()
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

