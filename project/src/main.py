# Haoji Liu
import sys
import uuid
import json
import requests
from urllib.parse import urlparse

from flask import Flask, jsonify, request
import logic as l

import blockchain as bc
from decimal import *

CONST_NEW_COIN_BONUS_SENDER = '0'

# Instantiate the Node
app = Flask(__name__)

# Generate a globally unique address for this node
nid = str(uuid.uuid4()).replace('-', '')

# Instantiate the Blockchain
blockchain = bc.Blockchain()

CONST_ALWAYS_CREATE_BLOCK = True

#
# @app.route('/mine', methods=['GET'])
# def mine():
#   # We run the proof of work algorithm to get the next proof...
#   last_block = blockchain.last_block
#   proof, last_hash = blockchain.proof_of_work(last_block)
#
#   # We must receive a reward for finding the proof.
#   # The sender is "0" to signify that this node has mined a new coin.
#   amt_in_decimal = Decimal('1')
#   blockchain.new_transaction(
#     sender=CONST_NEW_COIN_BONUS_SENDER,
#     recipient=nid,
#     amount=amt_in_decimal,
#   )
#
#   # Forge the new Block by adding it to the chain
#   block = blockchain.new_block(proof, last_hash)
#
#   response = {
#     'message': "New Block Forged",
#     'index': block['index'],
#     'transactions': block['transactions'],
#     'proof': block['proof'],
#     'previous_hash': block['previous_hash'],
#   }
#   return jsonify(response), 200

# # GET /txns/5e0e3bd986d1ab40725cb9cae4c7a071eef71195074a4bcd240b37b862ace3f4
# @app.route('/txns/<txn_hash>', methods=['GET'])
# def txn_get(txn_hash):
#   txn_strings = l.get_txns([txn_hash,])
#   if txn_strings:
#     return txn_strings[0]
#   else:
#     return 'no transaction found'

@app.route('/txns/verify/<txn_id>', methods=['GET'])
def txn_verify(txn_id):
  """Returns True if this transaction is valid"""
  if len(l.get_txns(txn_id)) != 1:
    res = False
  
  b = blockchain.get_block_of_txn(txn_id)
  if b != None: 
    proof = blockchain.mTree.get_proof(b['index']-1)
    root = blockchain.mTree.get_merkle_root()
    if blockchain.mTree.validate_proof(proof, root, blockchain.hash(b)):
      res = True
  res = False
  return str(res)

@app.route('/txns', methods=['POST'])
def txn_create():
  form_dict = request.form.to_dict()
  form_dict['id'] = str(uuid.uuid4())
  # Check that the required fields are in the POST'ed data
  required = ['from_legal_entity', 'to_legal_entity', 'product_sku', 'quantity']
  if not all(k in form_dict for k in required):
    return 'Missing values', 400

  if CONST_ALWAYS_CREATE_BLOCK:
    # We run the proof of work algorithm to get the next proof...
    last_block = blockchain.last_block
    proof, last_hash = blockchain.proof_of_work(last_block)

    # add to the current block
    index = blockchain.new_transaction(form_dict)
    assert index

    # Forge the new Block by adding it to the chain
    block = blockchain.new_block(proof, last_hash)

    # # lastly, add to the database
    res = l.create_transaction(form_dict)
  else:
    # TODO: not mine a new block, add to the existing list of txns
    pass

  return res, 201

@app.route('/chain', methods=['GET'])
def full_chain():
  response = {
    'chain': blockchain.chain,
    'length': len(blockchain.chain),
  }
  return jsonify(response), 200


@app.route('/nodes/register', methods=['POST'])
def register_nodes():
  """I assume this endpoint will be hit periodically
  to reflect the latest reality
  """
  values = request.json
  nodes = values.get('nodes')

  if nodes is None:
    return "Error: Please supply a valid list of nodes", 400

  for node in nodes:
    blockchain.register_node(node)

  response = {
    'message': 'New nodes have been added',
    'total_nodes': list(blockchain.nodes),
  }
  return jsonify(response), 201

@app.route('/nodes/resolve', methods=['GET'])
def consensus():
  """I assume this is hit periodically/everytime
  we add a new transaction/block to reflect the reality
  """
  replaced = blockchain.resolve_conflicts()

  if replaced:
    response = {
        'message': 'Our chain was replaced',
        'new_chain': blockchain.chain
    }
  else:
    response = {
        'message': 'Our chain is authoritative',
        'chain': blockchain.chain
    }

  return jsonify(response), 200

if __name__ == '__main__':
  if len(sys.argv) == 2:
    p = sys.argv[1]
  else:
    p = 5000
  app.run(host='0.0.0.0', port=int(p), debug=True)
