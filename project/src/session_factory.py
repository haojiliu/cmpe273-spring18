from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from contextlib import contextmanager

engine = create_engine('sqlite:///app.db')

Base = declarative_base()
Base.metadata.create_all(engine)

Session = sessionmaker(bind=engine)

@contextmanager
def create_session():
  """Provide a transactional scope around a series of operations."""
  session = Session()
  try:
    yield session
    session.commit()
  except:
    session.rollback()
    raise
  finally:
    print('closing session!!')
    session.close()
