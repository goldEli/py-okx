
# 获取蜡烛低和高
def get_candle_info(data):
    high = float(data['high'])
    open = float(data['open'])
    close = float(data['close'])
    low = float(data['low'])
    low_1d = float(data['1d_low'])
    high_1d = float(data['1d_high'])

    candle_length = abs(close - open)

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
    
    return h1, h2, candle_length, upper_shadow_length, lower_shadow_length

top_multiple = 0.004
top_bias = 0.998
multiple = 0.02

# 是否是冲顶上影线策略
def is_top_upper_strategy(data):
    high = float(data['high'])
    high_1d = float(data['1d_high'])
    h1, h2, candle_length, upper_shadow_length, lower_shadow_length = get_candle_info(data)

    # 上引线大于下影线x倍数
    is_upper_greater_than_lower = upper_shadow_length > lower_shadow_length * 5
    # 是否有上引线
    is_upper = (upper_shadow_length / high) > top_multiple
    # 是否是顶
    is_top = high > high_1d * top_bias
    # 是否是针(上影线是蜡烛的50%)
    is_needle = candle_length > 0 and upper_shadow_length / candle_length > 1


    strategy1 = is_upper and is_top and is_needle  and is_upper_greater_than_lower
        
    strategy2 = is_top and candle_length > 0 and upper_shadow_length / candle_length > 2 and is_upper_greater_than_lower

    return strategy1 or strategy2

# 是否是普通上影线策略
def is_normal_upper_strategy(data):
    high = float(data['high'])
    h1, h2, candle_length, upper_shadow_length, lower_shadow_length = get_candle_info(data)
    # 上引线大于下影线x倍数
    is_upper_greater_than_lower = upper_shadow_length > lower_shadow_length * 5
    return (upper_shadow_length / high) > multiple and is_upper_greater_than_lower

# 是否是冲底下影线策略
def is_bottom_lower_strategy(data):
    low = float(data['low'])
    low_1d = float(data['1d_low'])
    h1, h2, candle_length, upper_shadow_length, lower_shadow_length = get_candle_info(data)
    # 下引线大于上影线x倍数
    is_lower_greater_than_upper = lower_shadow_length > upper_shadow_length * 5
    # 是否有下引线
    is_lower = lower_shadow_length/(lower_shadow_length + h2) > top_multiple
    # 是否是底
    is_bottom = low < low_1d * top_bias
    # 是否是针(下影线是蜡烛的50%)
    is_needle = candle_length > 0 and lower_shadow_length / candle_length > 1

    strategy1 = is_lower and is_bottom and is_needle and is_lower_greater_than_upper

    strategy2 = is_bottom and candle_length > 0 and lower_shadow_length / candle_length > 2 and is_lower_greater_than_upper

    return strategy1 or strategy2

# 是否是普通下影线策略
def is_normal_lower_strategy(data):
    low = float(data['low'])
    h1, h2, candle_length, upper_shadow_length, lower_shadow_length = get_candle_info(data)
    # 下引线大于上影线x倍数
    is_lower_greater_than_upper = lower_shadow_length > upper_shadow_length * 5
    return lower_shadow_length/(lower_shadow_length + h2) > multiple and is_lower_greater_than_upper