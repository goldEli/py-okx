
import json

with open('config.json', 'r') as f:
    config = json.load(f)
# 获取okx info
def get_okx_info():

    flag = "1" # Production trading: 0, Demo trading: 1

    #API initialization
    api_key = config['api_key']
    secret_key = config['secret_key']
    passphrase = config['passphrase']

    return api_key, secret_key, passphrase, flag
    