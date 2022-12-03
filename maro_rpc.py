import requests
import json
wei  = 1000000000000000000;
api_url = "http://rpc-tokyo.ttcnet.io"
get_balance = {"jsonrpc":"2.0","method":"eth_getBalance","params":["t07030ee98e75dbe167b95da7be5ed69d415f170a0","latest"],"id":67}
get_blocknumber = {"jsonrpc":"2.0","method":"eth_blockNumber","params":[],"id":67}
headers =  {"Content-Type":"application/json"}
res_get_balance = requests.post(api_url, data=json.dumps(get_balance), headers=headers)
res_get_blocknumber = requests.post(api_url, data=json.dumps(get_blocknumber), headers=headers)
result_bal = res_get_balance.json()
result_num = res_get_blocknumber.json()
block_num = res_get_blocknumber.json()['result']
bal = res_get_balance.json()['result']
print(result_bal)
print(result_num)
print(block_num)
block_n = int(block_num, base=16)
bal_n = int(bal, base=16)
bal_rel = bal_n/wei
print('%d -- %d' % (block_n,bal_n))
print('real balance is %d ' % bal_rel)