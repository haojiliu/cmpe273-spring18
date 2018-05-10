import requests
import json
import time
def pp(res):
  print(res.status_code)
  print(res.text)

host = 'http://127.0.0.1:5000'
host1 = 'http://127.0.0.1:5001'
hosts = [host, host1]

registry_host = 'http://127.0.0.1:3000'

print(hosts)

print('\nRegister nodes on node 1:')
res = requests.post(host + '/nodes/register', data={'nodes': hosts})
pp(res)
print('\nRegister nodes on node 2:')
res = requests.post(host1 + '/nodes/register', data={'nodes': hosts})
pp(res)

print('\nNode 1 looks like:')
res = requests.get(host + '/chain')
pp(res)
print('\nNode 2 looks like:')
res = requests.get(host1 + '/chain')
pp(res)

print('\ncreate a new entity:')
res = requests.post(registry_host + '/entity', data={})
entity1 = res.text
pp(res)

print('\ncreate a another entity:')
res = requests.post(registry_host + '/entity', data={})
entity2 = res.text
pp(res)

print('\ncreate a product:')
res = requests.post(registry_host + '/product', data={})
sku = res.text
pp(res)

print('\ncreate a txn on node 1:')
res = requests.post(host + '/txns', data={'id': 1, 'created_at_utc': time.time(), 'from_legal_entity':entity1, 'to_legal_entity':entity2, 'product_sku':sku})
pp(res)

print('\nNode 1 looks like:')
res = requests.get(host + '/chain')
pp(res)
print('\nNode 2 looks like:')
res = requests.get(host1 + '/chain')
pp(res)

print('\nresolve consensus on node 2:')
res = requests.post(host1 + '/nodes/resolve')
pp(res)

print('\nNode 1 looks like:')
res = requests.get(host + '/chain')
pp(res)
print('\nNode 2 looks like:')
res = requests.get(host1 + '/chain')
pp(res)
#
# print('\nregistry node 1:')
# res = requests.get(registry_host)
# pp(res)
#
# print('register nodes:')
# res = requests.post(host + '/nodes/register', data = json.dumps({"nodes": [host, registry_host]}))
# pp(res)
