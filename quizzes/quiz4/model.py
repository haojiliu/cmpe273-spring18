import os
import sys
from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy import create_engine

Base = declarative_base()

class Wallet(Base):
    __tablename__ = 'wallet'
    # Here we define columns for the table address.
    # Notice that each column is also a normal Python instance attribute.
    id = Column(Integer, primary_key=True)
    address = Column(String(250), nullable=False)
    balance = Column(Integer, nullable=False)
    public_key = Column(String(250), nullable=False)
