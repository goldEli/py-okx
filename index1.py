
from lib.email import send_email_for_trigger_rsi_macd
from lib.market import get_candles
import time
from lib.order import do_order
import talib
import numpy as np

# MACD 指标计算
def calculate_macd(candles, short_period=12, long_period=26, signal_period=9):
    close_prices = np.array([float(candle['close']) for candle in candles])
    macd, signal, hist = talib.MACD(close_prices, 
                                  fastperiod=short_period,
                                  slowperiod=long_period,
                                  signalperiod=signal_period)
    return macd, signal, hist
# RSI 计算
def calculate_rsi(candles, period=14):
    close_prices = np.array([float(candle['close']) for candle in candles])
    rsi = talib.RSI(close_prices, timeperiod=period)
    return rsi[-1] if rsi is not None and len(rsi) > 0 else 50  # 默认返回50作为中性值

def handle_candles(candles):
    try:
        # 确保candles是列表且不为空
        if not isinstance(candles, list) or len(candles) == 0:
            print("无效的蜡烛数据格式")
            return False, False
            
        # 检查第一个蜡烛数据是否包含所需字段
        first_candle = candles[0]
        required_fields = ['close', 'timestamp']
        if not all(field in first_candle for field in required_fields):
            print("蜡烛数据缺少必要字段")
            return False, False
            
        # 计算技术指标
        macd_line, signal_line, macd_histogram = calculate_macd(candles)
        rsi = calculate_rsi(candles)  # 直接传入candles数据，而不是[float(candle['close'])...]
        
        # 获取最新指标值
        latest_macd = macd_line[-1]
        latest_signal = signal_line[-1]
        latest_histogram = macd_histogram[-1]
        latest_rsi = rsi
        
        # 判断逻辑
        long_signal = False
        short_signal = False
        
        # MACD金叉(快线上穿慢线)且RSI超卖(小于30)
        if latest_macd > latest_signal and latest_rsi < 30:
            long_signal = True
            return long_signal, short_signal
        
        # MACD死叉(快线下穿慢线)且RSI超买(大于70)
        if latest_macd < latest_signal and latest_rsi > 70:
            short_signal = True
            return long_signal, short_signal
        # 默认返回False, False
        return False, False
    except Exception as e:
        print(f"处理蜡烛数据时出错: {e}")
        return False, False

def print_signals(long_signal, short_signal):
    if long_signal:
        print("做多信号: 是")
    if short_signal:
        print("做空信号: 是")
    print("------------------------")

# 2025-01-01 00:00:00
def convertTimestamp(timestamp):
    timestamp = int(timestamp)
    time_local = time.localtime(timestamp)
    dt = time.strftime("%Y-%m-%d %H:%M:%S", time_local)
    return dt

def getLastedCandle(candles):
    if len(candles) > 0:
        lastedCandle = candles[-1]
        print("最新K线:")
        print("时间:", convertTimestamp(lastedCandle['timestamp']))
        print("开盘价:", lastedCandle['open'])
        print("收盘价:", lastedCandle['close'])
        print("最高价:", lastedCandle['high'])
        print("最低价:", lastedCandle['low'])
        print("成交量:", lastedCandle['volume'])
        print("成交额:", lastedCandle['turnover'])
        print("------------------------")
        return lastedCandle
    else:
        return None

def fetch_candles_periodically(symbol):
    try:
        while True:
            try:
                result = get_candles(symbol)
                long_signal, short_signal = handle_candles(result)
                if long_signal is not None and short_signal is not None:  # 添加None检查
                    if long_signal or short_signal:
                        # version = "2.0.0"
                        direction = "long" if long_signal else "short"
                        data = result[-1]
                        do_order(symbol, data, direction)
                        print_signals(long_signal, short_signal)
                        lastedCandle = getLastedCandle(result)
                        email_str = f"""
                        macd+rsi 
                        symbol：{symbol}
                        currentPrice：{lastedCandle['close']}
                        high：{lastedCandle['high']}
                        low：{lastedCandle['low']}
                        open：{lastedCandle['open']}
                        currentTime：{convertTimestamp(lastedCandle['timestamp'])}
                        """
                        send_email_for_trigger_rsi_macd(email_str)
                time.sleep(1)
            except Exception as e:
                print(f"发生错误: {e}")
                time.sleep(1)
    except KeyboardInterrupt:
        print("\n程序已停止")

# 每秒调用一次 get_candles
if __name__ == "__main__":
    symbol = "ETH-USDT-SWAP"
    fetch_candles_periodically(symbol)
