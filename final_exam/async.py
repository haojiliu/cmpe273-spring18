import asyncio, requests

# global vars
url = 'https://google.com'
cnt = 10

def wrapper_func(idx):
  res = requests.get(url)
  print('%s: %s' % (idx, str(res)))
  return idx

print('sync')
# sync
for i in range(cnt):
  wrapper_func(i)

print('async')

# async
async def main():
  loop = asyncio.get_event_loop()
  futures = [
    loop.run_in_executor(None, wrapper_func, i)
    for i in range(cnt)
  ]
  for response in await asyncio.gather(*futures):
    pass

loop = asyncio.get_event_loop()
loop.run_until_complete(main())
