
import okx.MarketData as MarketData
from lib.config import get_okx_info
from datetime import datetime
api_key, secret_key, passphrase, flag = get_okx_info()
print("数据:实盘" if flag == "0" else "数据:模拟盘")
market_api = MarketData.MarketAPI(flag=flag)


def get_kline_data_1d(symbol):
    # symbol = 'BTC-USDT'  # 交易对
    timeframe = '1D'     # 时间周期（1 小时）
    limit = 1          # 获取的 K 线数量（最多 100 条）

    try:
        # 调用 API 获取 K 线数据
        candles = market_api.get_candlesticks(instId=symbol, bar=timeframe, limit=limit)
    except Exception as e:
        print(f"获取1天K线数据失败{symbol}: {e}")
        return None



    timestamp, open, high, low, close, volume, turn_over, turn_over_rate, count = candles['data'][0]

    return {
        'timestamp': timestamp,
        'open': open,
        'high': high,
        'low': low,
        'close': close,
        'volume': volume,
        'turn_over': turn_over,
        'turn_over_rate': turn_over_rate,
        'count': count
    }


def get_1d_high_low(symbol):
    data = get_kline_data_1d(symbol)
    if data is None:
        return None
    return {
        '1d_high': data['high'],
        '1d_low': data['low']
    }


def get_kline_data(symbol):
    # 获取 BTC-USDT 的 1 小时 K 线数据
    # symbol = 'BTC-USDT'  # 交易对
    symbol = symbol  # 交易对
    timeframe = '15m'     # 时间周期（1 小时）
    limit = 5          # 获取的 K 线数量（最多 100 条）

    try:
        # 调用 API 获取 K 线数据
        candles = market_api.get_candlesticks(instId=symbol, bar=timeframe, limit=limit)
    except Exception as e:
        print(f"获取15分钟K线数据失败{symbol}: {e}")
        return None

    # 第2根K线
    second_candle = candles['data'][1]
    last_candle = candles['data'][0]
    # print(second_candle)

    timestamp, open, high, low, close, volume, turn_over, turn_over_rate, count = second_candle
    last_price = last_candle[4]

    # 获取1天中最高价和最低价
    data_1d = get_1d_high_low(symbol)
    if data_1d is None:
        return None


    return {
        'symbol': symbol,
        'timestamp': timestamp,
        'open': open,
        'high': high,
        'low': low,
        'close': close,
        'volume': volume,
        'turn_over': turn_over,
        'turn_over_rate': turn_over_rate,
        'count': count,
        '1d_high': data_1d['1d_high'],
        '1d_low': data_1d['1d_low'],
        'last_price': float(last_price)
    }


def get_current_price(symbol):
    # 获取 BTC-USDT 的 1 小时 K 线数据
    # symbol = 'BTC-USDT'  # 交易对
    symbol = symbol  # 交易对
    timeframe = '1m'     # 时间周期（1 小时）
    limit = 1          # 获取的 K 线数量（最多 100 条）

    try:
        # 调用 API 获取 K 线数据
        candles = market_api.get_candlesticks(instId=symbol, bar=timeframe, limit=limit)
    except Exception as e:
        print(f"获取1分钟K线数据失败{symbol}: {e}")
        return None

    # 第2根K线
    last_candle = candles['data'][0]
    # print(second_candle)

    last_price = last_candle[4]


    return {
        'last_price': float(last_price)
    }
