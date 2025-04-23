
from datetime import datetime
from lib.email import send_email_for_trigger_rsi_macd
from lib.market import get_candles, get_current_price
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

# RSI 指标计算
def calculate_rsi(candles, period=56):
    close_prices = np.array([float(candle['close']) for candle in candles])
    rsi = talib.RSI(close_prices, timeperiod=period)
    return rsi

# 随机指标计算
def calculate_stochastic(candles, fastk_period=56, slowk_period=12, slowd_period=12):
    high_prices = np.array([float(candle['high']) for candle in candles])
    low_prices = np.array([float(candle['low']) for candle in candles])
    close_prices = np.array([float(candle['close']) for candle in candles])
    k, d = talib.STOCH(high_prices, low_prices, close_prices,
                       fastk_period=fastk_period,
                       slowk_period=slowk_period,
                       slowd_period=slowd_period)
    return k, d


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
        rsi = calculate_rsi(candles)
        k_line, d_line = calculate_stochastic(candles)
        
        # 获取最新指标值
        latest_macd = macd_line[-1]
        latest_signal = signal_line[-1]
        latest_histogram = macd_histogram[-1]
        latest_rsi = rsi[-1]
        latest_k = k_line[-1]
        latest_d = d_line[-1]
        
        # 判断逻辑
        long_signal = False
        short_signal = False
        print("RSI:", latest_rsi)
        print("随机K:", latest_k)
        print("随机D:", latest_d)
        print("MACD:", latest_macd)
        print("Signal:", latest_signal)
        print("Histogram:", latest_histogram)
        print("------------------------")
        
        # MACD金叉(快线上穿慢线)且RSI超卖(小于10)且随机指标超卖
        if latest_macd > latest_signal and latest_k < 10 and latest_d < 10:
            print("做多信号")
            print("RSI:", latest_rsi)
            print("随机K:", latest_k)
            print("随机D:", latest_d)
            print("latest_macd:", latest_macd)
            print("latest_signal:", latest_signal)
            print("Histogram:", latest_histogram)
            print("------------------------")
            long_signal = True
            return long_signal, short_signal
        
        # MACD死叉(快线下穿慢线)且RSI超买(大于90)且随机指标超买
        if latest_macd < latest_signal and  latest_k > 90 and latest_d > 90:
            print("做空信号")
            print("RSI:", latest_rsi)
            print("随机K:", latest_k)
            print("随机D:", latest_d)
            print("latest_macd:", latest_macd)
            print("latest_signal:", latest_signal)
            print("Histogram:", latest_histogram)
            print("------------------------")
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
def convertTimestamp(timestamp_str):

    # 1. 转换为整数（毫秒）
    timestamp = int(timestamp_str)

    # 2. 转换为 datetime 对象（UTC 时间）
    dt = datetime.fromtimestamp(timestamp / 1000)

    # 3. 格式化为字符串（例如：YYYY-MM-DD HH:MM:SS）
    formatted_time = dt.strftime("%Y-%m-%d %H:%M:%S")
    return formatted_time

def getLastedCandle(candles):
    if len(candles) > 0:
        lastedCandle = candles[-1]
        # print("最新K线:")
        # # print("时间:", convertTimestamp(lastedCandle['timestamp']))
        # print("时间:", lastedCandle['timestamp'])
        # print("开盘价:", lastedCandle['open'])
        # print("收盘价:", lastedCandle['close'])
        # print("最高价:", lastedCandle['high'])
        # print("最低价:", lastedCandle['low'])
        # print("成交量:", lastedCandle['volume'])
        # # print("成交额:", lastedCandle['turnover'])
        # print("------------------------")
        return lastedCandle
    else:
        return None

def getYearMouthDayHourMinuteSecond(timestamp_str):

    # 1. 转换为整数（毫秒）
    timestamp = int(timestamp_str)

    # 2. 转换为 datetime 对象（UTC 时间）
    dt = datetime.fromtimestamp(timestamp / 1000)

    year = dt.strftime("%Y")
    month = dt.strftime("%m")
    day = dt.strftime("%d")
    hour = dt.strftime("%H")
    return year + month + day + hour

cacheData = {}


interval = 0.5
def fetch_candles_periodically(symbol):
    try:
        while True:
            # result = get_candles(symbol)
            result = get_candles(symbol, "1m")
            long_signal, short_signal = handle_candles(result)
            # long_signal = True
            # short_signal = False
            if long_signal is not None and short_signal is not None:  # 添加None检查
                if long_signal or short_signal:
                    lastedCandle = getLastedCandle(result)
                    currentTime = convertTimestamp(lastedCandle['timestamp'])
                    currentTimeStr = getYearMouthDayHourMinuteSecond(lastedCandle['timestamp'])
                    if currentTimeStr in cacheData:
                        continue
                    cacheData[currentTimeStr] = True
                    # version = "2.0.0"
                    direction = "long" if long_signal else "short"
                    # data = result[-1]
                    d = get_current_price(symbol)
                    do_order(symbol, d, direction)
                    print_signals(long_signal, short_signal)


                    email_str = f"""
                    macd+rsi 
                    symbol：{symbol}
                    currentPrice：{lastedCandle['close']}
                    high：{lastedCandle['high']}
                    low：{lastedCandle['low']}
                    open：{lastedCandle['open']}
                    currentTime：{currentTime}
                    """
                    send_email_for_trigger_rsi_macd(email_str)
            time.sleep(interval)
          
    except KeyboardInterrupt:
        print("\n程序已停止")

# 每秒调用一次 get_candles
if __name__ == "__main__":
    symbol = "ETH-USDT-SWAP"
    fetch_candles_periodically(symbol)
