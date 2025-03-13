
import okx.MarketData as MarketData
from lib.config import get_okx_info
from datetime import datetime
api_key, secret_key, passphrase, flag = get_okx_info()
market_api = MarketData.MarketAPI(api_key, secret_key, passphrase, flag)


def get_kline_data_1d(symbol):
    # symbol = 'BTC-USDT'  # 交易对
    timeframe = '1D'     # 时间周期（1 小时）
    limit = 1          # 获取的 K 线数量（最多 100 条）

    # 调用 API 获取 K 线数据
    candles = market_api.get_candlesticks(instId=symbol, bar=timeframe, limit=limit)



    data = candles['data'][0]

    return data


def get_1d_high_low(symbol):
    timestamp, open, high, low, close, volume, turn_over, turn_over_rate, count = get_kline_data_1d(symbol)
    return {
        '1d_high': high,
        '1d_low': low
    }


# 获取btc k线 15分钟
def get_kline_data(symbol):
    # 获取 BTC-USDT 的 1 小时 K 线数据
    # symbol = 'BTC-USDT'  # 交易对
    symbol = symbol  # 交易对
    timeframe = '15m'     # 时间周期（1 小时）
    limit = 5          # 获取的 K 线数量（最多 100 条）

    # 调用 API 获取 K 线数据
    candles = market_api.get_candlesticks(instId=symbol, bar=timeframe, limit=limit)

    # 第2根K线
    second_candle = candles['data'][1]

    timestamp, open, high, low, close, volume, turn_over, turn_over_rate, count = second_candle

    # 获取1天中最高价和最低价
    data_1d = get_1d_high_low(symbol)


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
        '1d_low': data_1d['1d_low']
    }
