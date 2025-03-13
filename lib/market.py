
import okx.MarketData as MarketData
from lib.config import get_okx_info
from datetime import datetime
api_key, secret_key, passphrase, flag = get_okx_info()
market_api = MarketData.MarketAPI(api_key, secret_key, passphrase, flag)
# 获取btc k线 15分钟
def get_btc_data():
    # 获取 BTC-USDT 的 1 小时 K 线数据
    symbol = 'BTC-USDT'  # 交易对
    timeframe = '15m'     # 时间周期（1 小时）
    limit = 5          # 获取的 K 线数量（最多 100 条）
    

    # 调用 API 获取 K 线数据
    candles = market_api.get_candlesticks(instId=symbol, bar=timeframe, limit=limit)

    # 第2根K线
    second_candle = candles['data'][1]

    timestamp, open, high, low, close, volume, turn_over, turn_over_rate, count = second_candle

    # print time format 2025-03-12 10:00:00
    # print(f"时间：{datetime.fromtimestamp(int(timestamp) / 1000).strftime('%Y-%m-%d %H:%M:%S')}")
    # print(f"开盘价：{open}")
    # print(f"最高价：{high}")
    # print(f"最低价：{low}")
    # print(f"收盘价：{close}")
    # print(f"成交量：{volume}")
    # print(f"成交额：{turn_over}")
    # print(f"成交笔数：{count}")

    return timestamp, open, high, low, close, volume, turn_over, turn_over_rate, count
