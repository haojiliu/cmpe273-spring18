from datetime import date

from model import Wallet, Base
from sqlalchemy import create_engine
engine = create_engine('sqlite:///assignment2.db')
Base.metadata.create_all(engine)

def session_factory():
  from sqlalchemy.orm import sessionmaker
  DBSession = sessionmaker(bind=engine)
  return DBSession()

def create_wallet():
  session = session_factory()
  wallet1 = Wallet("0x12345", 1000, 'asdfasdfafdafafasfd')
  wallet2 = Wallet("0x12345", 1000, 'asdfasdfafdafafasfd')
  session.add(wallet1)
  session.add(wallet2)
  session.commit()
  session.close()

def get_wallets():
  session = session_factory()
  q = session.query(Wallet)
  session.close()
  return q.all()

def delete_wallet():
  pass

if __name__ == "__main__":
  w = get_wallets()
  if len(w) == 0:
      create_wallet()
  w = get_wallets()

  for x in w:
      print('%s was born in %s' % (x.id, x.address))
