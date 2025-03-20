
# 倍数
multiple = 0.008
# multiple = 0.001

bias = 0.998

# 是否是长上引线
def is_long_upper_shadow(data):
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

    # 冲顶上影线
    print((upper_shadow_length / high) > multiple/4, upper_shadow_length / high, multiple/4)
    print(high > high_1d * bias, high, high_1d, high_1d * bias)
    if (upper_shadow_length / high) > multiple/4 and high > high_1d * bias:
        print("冲顶上影线")
        return True
        
        
    if (upper_shadow_length / high) > multiple:
        return True

    return False 

# 开盘价：631.7
# 最高价：633.7
# 最低价：631.6
# 收盘价：632.4

data = {
    'high': 631.7,
    'open': 633.7,
    'close': 631.6,
    'low': 632.4,
    '1d_high': 637.5,
    '1d_low': 602.1
}

print(is_long_upper_shadow(data))