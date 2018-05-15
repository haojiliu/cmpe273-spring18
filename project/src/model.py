import os
import sys
import time
import uuid
import random
import string

from sqlalchemy import Column, ForeignKey, Integer, String, Float
from sqlalchemy.orm import relationship
from sqlalchemy.types import Numeric

from session_factory import Base

CONST_FLAGS_DELETED = 1 << 3
CONST_FLAGS_INACTIVE = 1 << 2
CONST_FLAGS_ACTIVE = 0

CONST_SKU_PREFIX_DEFAULT = 'ABC'

# class Block:
#   def __init__(self, index, current_transactions, proof, previous_hash):
#     self.index = index
#     self.timestamp = time()
#     self.transactions = current_transactions # pass by reference is the key here!!!
#     self.proof = proof
#     self.previous_hash = previous_hash

def generate_randome_string(size):
  return ''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(size))

def sku_generator(prefix=None):
  generated_parts = [generate_randome_string(3), generate_randome_string(3)]
  if prefix:
    return '-'.join([prefix, '-'.join(generated_parts)])
  else:
    return '-'.join([CONST_SKU_PREFIX_DEFAULT, '-'.join(generated_parts)])

# i.e, baby product
class Product(Base):
  __tablename__ = 'product'
  sku = Column(String(250), primary_key=True)
  flags = Column(Integer, nullable=True)
  description = Column(String(250), nullable=True)
  weight = Column(String(250), nullable=True)
  size_x = Column(Float, nullable=True)
  size_y = Column(Float, nullable=True)
  size_z = Column(Float, nullable=True)
  manufacturer_id = Column(String(250), nullable=True)
  created_at_utc = Column(String(250), nullable=True)
  updated_at_utc = Column(String(250), nullable=True)

  def __init__(self, form):
    self.sku = sku_generator(prefix='BTC')
    self.flags = form.get('flags', 0)
    self.description = form.get('description', 'sample desc')
    self.weight = form.get('weight', 'sample weight')
    self.size_x = form.get('size_x', 1)
    self.size_y = form.get('size_y', 2)
    self.size_z = form.get('size_z', 3)
    self.manufacturer_id = form.get('manufacturer_id', 'sample manufacturer_id')
    self.created_at_utc = form.get('created_at_utc', 'sample created_at_utc')
    self.updated_at_utc = form.get('updated_at_utc', 'sample updated_at_utc')

  def to_string(self):
    d = dict(self.__dict__)
    del d['_sa_instance_state']
    return str(d)

# ie, person, corporation, llc
class LegalEntity(Base):
  __tablename__ = 'legal_entity'
  id = Column(String(250), primary_key=True)
  name = Column(String(250), nullable=True)
  desc = Column(String(250), nullable=True)
  email = Column(String(250), nullable=True)
  address = Column(String(250), nullable=True)
  flags = Column(Integer, nullable=True)
  created_at_utc = Column(String(250), nullable=True)
  updated_at_utc = Column(String(250), nullable=True)

  def __init__(self, form):
    self.id = str(uuid.uuid4())
    self.name = form.get('name', 'sample name')
    self.desc = form.get('desc', 'sample desc')
    self.email = form.get('email', 'sample email')
    self.address = form.get('address', 'sample addr')
    self.flags = form.get('flags', 0)
    self.created_at_utc = form.get('created_at_utc', 'sample created at utc')
    self.updated_at_utc = form.get('updated_at_utc', 'sample updated at utc')

  def to_string(self):
    d = dict(self.__dict__)
    del d['_sa_instance_state']
    return str(d)

class Transaction(Base):
  __tablename__ = 'txn'
  id = Column(String(250), primary_key=True)
  created_at_utc = Column(String(250), nullable=False)
  from_legal_entity = Column(String, ForeignKey("legal_entity.id"), nullable=False)
  to_legal_entity = Column(String, ForeignKey("legal_entity.id"), nullable=False)
  product_sku = Column(String(250), ForeignKey("product.sku"), nullable=False)
  quantity = Column(Integer, nullable=False)

  def __init__(self, form):
    self.id = form.get('id')
    self.created_at_utc = form.get('created_at_utc')
    self.from_legal_entity = form.get('from_legal_entity', 'sample legal entity 1')
    self.to_legal_entity = form.get('to_legal_entity', 'sample legal entity 2')
    self.product_sku = form.get('product_sku', 'sample sku')
    self.quantity = form.get('quantity', 99)

  def to_string(self):
    d = dict(self.__dict__)
    del d['_sa_instance_state']
    return str(d)
