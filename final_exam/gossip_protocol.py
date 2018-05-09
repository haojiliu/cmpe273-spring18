import random

num_of_nodes = 1000

nodes = [0] * num_of_nodes
nodes[0] = 1

# each round, a node tells # of other nodes
gossip_volume = 2

positions = []

print('spread to all nodes..')

cnt = 0
while sum(nodes) != num_of_nodes:
  print('This is the round -- %s' % cnt)
  for val in nodes:
    # if this node knows, gossip
    if val:
      for i in range(gossip_volume):
        pos = random.randint(0, 999)
        positions.append(pos)
    else:
      pass

  for pos in positions:
    nodes[pos] = 1
  print('after this round, %s nodes know' % sum(nodes))
  cnt = cnt + 1

print('done with spreading to all nodes..')
