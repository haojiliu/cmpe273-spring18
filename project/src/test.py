import requests
import json
import time
def pp(res):
  #print('getting status code:')
  print(res.status_code)
  #print('getting result:')
  print(res.text)

host = 'http://127.0.0.1:5000'
host1 = 'http://127.0.0.1:5001'

print('\nA empty blockchain when it just started:')
res = requests.get(host + '/chain')
pp(res)

# print('\nregistry server connection:')
# res = requests.get(host1)
# pp(res)

# # print('register nodes:')
# # res = requests.post(host + '/nodes/register', data = json.dumps({"nodes": [host, host1]}))
# # pp(res)

print('\ncreate a new entity:')
res = requests.post(host1 + '/entity', data={'id': 1})
pp(res)

print('\ncreate a another entity:')
res = requests.post(host1 + '/entity', data={'id': 2})
pp(res)

# print('\nentity info:')
# res = requests.get(host1 + '/entity/1')
# pp(res)

# print('\ndelete entity:')
# res = requests.delete(host1 + '/entity/1')
# pp(res)

# print('\nentity info:')
# res = requests.get(host1 + '/entity/1')
# pp(res)

# print('\ncreate a product:')
# res = requests.post(host1 + '/product', data={'sku': '123-456-789'})
# pp(res)

# print('\nproduct info:')
# res = requests.get(host1 + '/product/123-456-789')
# pp(res)

# print('\ndelete entity:')
# res = requests.delete(host1 + '/product/123-456-789')
# pp(res)

# print('\nentity info:')
# res = requests.get(host1 + '/product/123-456-789')
# pp(res)

print('\ncreate a txn:')
res = requests.post(host + '/txns', data={'id': 1, 'created_at_utc': time.time(), 'from_legal_entity':'1', 'to_legal_entity':'2', 'product_sku':'123'})
pp(res)
