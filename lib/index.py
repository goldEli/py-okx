

import okx.Account as Account

# 判断当前账户模式
def get_account_mode(api_key, secret_key, passphrase, flag):
    accountAPI = Account.AccountAPI(api_key, secret_key, passphrase, False, flag)
    result = accountAPI.get_account_config()
    print(result)
    if result['code'] == "0":
         acctLv = result["data"][0]["acctLv"]
         if acctLv == "1":
             return "Simple mode"
         elif acctLv == "2":
            return "Single-currency margin mode"
         elif acctLv == "3":
            return "Multi-currency margin mode"
         elif acctLv == "4":
            return "Portfolio margin mode"
    else:
        return "Error"
