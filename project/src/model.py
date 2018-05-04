import os
import sys
import time
from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship
from sqlalchemy.types import Numeric

from session_factory import Base

CONST_FLAGS_DELETED = 1 << 3
CONST_FLAGS_INACTIVE = 1 << 2
CONST_FLAGS_ACTIVE = 0

class Block:
  def __init__(self, index, current_transactions, proof, previous_hash):
    self.index = index
    self.timestamp = time()
    self.transactions = current_transactions # pass by reference is the key here!!!
    self.proof = proof
    self.previous_hash = previous_hash

# i.e, baby product
class Product(Base):
  __tablename__ = 'wallet'
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
    self.id = form.get('id')
    self.balance = form.get('balance')
    self.coin_symbol = form.get('coin_symbol')

  def to_string(self):
    return str({
      'id': self.id,
      'balance': self.balance,
      'coin_symbol': self.coin_symbol
    })

# ie, person, corporation, llc
class LegalEntity(Base):
  __tablename__ = 'wallet'
  id = Column(String(250), primary_key=True)
  name = Column(String(250), nullable=True)
  desc = Column(String(250), nullable=True)
  email = Column(String(250), nullable=True)
  address = Column(String(250), nullable=True)
  flags = Column(Integer, nullable=True)
  created_at_utc = Column(String(250), nullable=True)
  updated_at_utc = Column(String(250), nullable=True)

  def __init__(self, form):
    self.id = form.get('id')
    self.balance = form.get('balance')
    self.coin_symbol = form.get('coin_symbol')

  def to_string(self):
    return str({
      'id': self.id,
      'balance': self.balance,
      'coin_symbol': self.coin_symbol
    })

class Transaction(Base):
  __tablename__ = 'txn'
  id = Column(String(250), primary_key=True)
  flags = Column(String(250), nullable=False)
  created_at_utc = Column(String(250), nullable=False)
  from_legal_entity = Column(Integer, ForeignKey("LegalEntity.id"), nullable=False)
  to_legal_entity = Column(Integer, ForeignKey("LegalEntity.id"), nullable=False)
  product_sku = Column(String(250), ForeignKey("Product.sku"), nullable=False)
  quantity = Column(Integer, nullable=False)

  def __init__(self, form):
    self.uuid = form.get('uuid')
    self.status = form.get('status')
    self.from_wallet = form.get('from_wallet')
    self.to_wallet = form.get('to_wallet')
    self.amount = form.get('amount')
    self.time_stamp = form.get('time_stamp')

  def to_string(self):
    return str({
      'txn_hash': self.txn_hash,
      'status': self.status,
      'from_wallet': self.from_wallet,
      'to_wallet': self.to_wallet,
      'amount': self.amount,
      'time_stamp': self.time_stamp
    })
