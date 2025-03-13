import okx.Account as Account
from lib.config import get_okx_info

api_key, secret_key, passphrase, flag = get_okx_info()

# 获取账户余额
def get_account_balance():
    account_api = Account.AccountAPI(api_key, secret_key, passphrase, flag)
    result = account_api.get_account_balance()
    print(result)
    # data = result['data']
    # details = data[0]['details']
    
    # # get usdt balance
    # # loop details find ccy is usdt
    # for detail in details:
    #     if detail['ccy'] == 'USDT':
    #         usdt_balance = detail['availBal']
    #         print('usdt_balance', usdt_balance)
    #         return usdt_balance
    
    # return '0'
    # print(data)