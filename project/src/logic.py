from datetime import date

from model import LegalEntity, Transaction, Product

from session_factory import create_session

def create_legal_entity(form):
  try:
    with create_session() as s:
      w = LegalEntity(form)
      if _get_legal_entities([w.id], s):
        return 'existed'
      else:
        s.add(w)
        return w.id
  except:
    raise
    return 'failed'

def create_product(form):
  try:
    with create_session() as s:
      p = Product(form)
      if _get_products([p.sku], s):
        return 'existed'
      else:
        s.add(p)
        return p.sku
  except:
    raise
    return 'failed'


def _get_products(skus, session):
  """Return a list of Product object"""
  res = session.query(Product).filter(Product.sku.in_(skus)).all()
  return res

def get_products(skus):
  """Return a list of Product object in strings"""
  with create_session() as s:
    return [w.to_string() for w in _get_products(skus, s)]

def delete_products(skus):
  try:
    with create_session() as s:
      for p in _get_products(skus, s):
        s.delete(p)
  except:
    raise
    return 'delete failed'
  return 'deleted'

def _get_legal_entities(ids, session):
  """Return a list of Entity object"""
  res = session.query(LegalEntity).filter(LegalEntity.id.in_(ids)).all()

  return res

def get_legal_entities(ids):
  """Return a list of Product object in strings"""
  with create_session() as s:
    return [w.to_string() for w in _get_legal_entities(ids, s)]

def delete_legal_entities(ids):
  try:
    with create_session() as s:
      for p in _get_legal_entities(ids, s):
        s.delete(p)
  except:
    raise
    return 'delete failed'
  return 'deleted'

def _get_txns(ids, session):
  """Return a list of Transaction object"""
  res = session.query(Transaction).filter(Transaction.id.in_(ids)).all()
  return res

def get_txns(ids):
  """Return a list of Transaction object in strings"""
  with create_session() as s:
    return [t.to_string() for t in _get_txns(ids, s)]

def create_transaction(form):
  try:
    with create_session() as s:
      t = Transaction(form)

      entities = _get_legal_entities([t.from_legal_entity, t.to_legal_entity], s)
      if len(entities) != 2:
        return 'invalid entity ids'
      products = _get_products([t.product_sku], s)
      if len(products) != 1:
        return 'invalid product sku'

      if _get_txns([t.id], s):
        return 'existed'
      else:
        s.add(t)
        return t.id
  except:
    raise
    return 'failed'
