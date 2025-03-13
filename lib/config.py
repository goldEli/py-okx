
import json

with open('config.json', 'r') as f:
    config = json.load(f)

with open('coinConfig.json', 'r') as f:
    coin_config = json.load(f)

def get_coin_config():
    return coin_config

def get_symbol_list():
    symbol_list = []
    for symbol in coin_config:
        symbol_list.append(symbol)
    return symbol_list

# 获取模拟盘配置
def get_demo_config():
    flag = "1" # Production trading: 0, Demo trading: 1

    #API initialization
    api_key = config['api_key_demo']
    secret_key = config['secret_key_demo']
    passphrase = config['passphrase_demo']

    return api_key, secret_key, passphrase, flag

# 获取真实盘配置
def get_real_config():
    flag = "0" # Production trading: 0, Demo trading: 1

    #API initialization
    api_key = config['api_key']
    secret_key = config['secret_key']
    passphrase = config['passphrase']

    return api_key, secret_key, passphrase, flag
    
# 获取okx info
def get_okx_info():

    # return get_real_config()
    return get_demo_config()
    