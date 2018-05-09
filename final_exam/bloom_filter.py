# Haoji Liu
import math

def get_num_of_hash_func(m, n):
  return int(float(m) / float(n) * math.log1p(2))

class BloomFilter:
  def __init__(self, m, n):
    self.array_size = m
    self.num_of_hash_func = get_num_of_hash_func(m, n)
    self.array = [0] * m

  def get_positions(self, s):
    return [hash(s+str(val)) % self.array_size for val in range(self.num_of_hash_func)]

  def add(self, s):
    for pos in self.get_positions(s):
      self.array[pos] = 1

  def is_exist(self, s):
    for pos in self.get_positions(s):
      if not self.array[pos]:
        return False
    return True

if __name__ == '__main__':
  print(get_num_of_hash_func(1000, 100))
  bf = BloomFilter(1000, 100)
  print(bf.is_exist('abcd'))
  bf.add('abcd')
  print(bf.is_exist('abcd'))
