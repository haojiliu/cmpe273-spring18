import requests
import json
import time
def pp(res):
  print(res.status_code)
  print(res.text)

host = 'http://127.0.0.1:5000'
registry_host = 'http://127.0.0.1:3000'

print('\nAn empty blockchain when started:')
res = requests.get(host + '/chain')
pp(res)

print('\ncreate a new entity:')
res = requests.post(registry_host + '/entity', data={})
entity1 = res.text
pp(res)

print('\ncreate a another entity:')
res = requests.post(registry_host + '/entity', data={})
entity2 = res.text
pp(res)

print('\nentity info:')
res = requests.get(registry_host + '/entity/'+entity1)
pp(res)

print('\ndelete entity:')
res = requests.delete(registry_host + '/entity/'+entity1)
pp(res)

print('\nentity info:')
res = requests.get(registry_host + '/entity/'+entity1)
pp(res)

print('\ncreate a product:')
res = requests.post(registry_host + '/product', data={})
sku = res.text
pp(res)

print('\nproduct info:')
res = requests.get(registry_host + '/product/'+sku)
pp(res)

print('\ndelete entity:')
res = requests.delete(registry_host + '/product/'+sku)
pp(res)

print('\nentity info:')
res = requests.get(registry_host + '/product/'+sku)
pp(res)

print('\ncreate a txn:')
res = requests.post(host + '/txns', data={'id': 1, 'created_at_utc': time.time(), 'from_legal_entity':entity1, 'to_legal_entity':entity2, 'product_sku':sku})
pp(res)

print('\nWhat the block chain looks like now:')
res = requests.get(host + '/chain')
pp(res)
