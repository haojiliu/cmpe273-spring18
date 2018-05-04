import requests

def pp(res):
  #print('getting status code:')
  print(res.status_code)
  #print('getting result:')
  print(res.text)

host = 'http://127.0.0.1:5000'

print('hello world')
res = requests.get(host)
pp(res)

print('create a wallet')

# create a wallet
post_data = {
      "id" : "1233445665353",
      "balance": 5,
      "coin_symbol": "FOO_COIN"
  }
res = requests.post(host+'/wallets', data=post_data)
pp(res)
print('get a wallet')

# get the created wallet
res = requests.get(host + '/wallets/1233445665353')
pp(res)

print('delete a wallet')

# delete the created wallet
res = requests.delete(host + '/wallets/1233445665353')
pp(res)

print('get a wallet')

# get the created wallet
res = requests.get(host + '/wallets/1233445665353')
pp(res)

print('create a txn')

# create a txn
post_data = {
      "txn_hash" : "12314",
      "amount": 5,
      "from_wallet": '12345',
      "to_wallet": '123456',
      'time_stamp': '2016-12-30 12:00:00'
  }
res = requests.post(host+'/txns', data=post_data)
pp(res)
print('get a txn')
# get the created txn
res = requests.get(host + '/txns/1234')
pp(res)
#
# print('delete a txn')
# print('get a txn')
