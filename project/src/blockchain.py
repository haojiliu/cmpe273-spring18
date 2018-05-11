#!/usr/bin/env python
# Haoji Liu

import hashlib
import simplejson as json
from time import time
from merkleTree import MerkleTree
from decimal import *
context = getcontext()

from datetime import datetime
import os, logging, sys
from urllib.parse import urlparse
# Third party module
import requests
from flask import Flask, render_template, request, redirect, url_for

import logic as l


class Blockchain:
  def __init__(self):
    self.current_transactions = []
    self.chain = []
    self.nodes = set()
    self.mTree = MerkleTree()
    # Create the genesis block
    self.new_block(proof=100, previous_hash='1')

  def register_node(self, address):
    """
    Add a new node to the list of nodes

    :param address: Address of node. Eg. 'http://192.168.0.5:5000'
    """
    parsed_url = urlparse(address)
    if parsed_url.netloc:
      self.nodes.add(parsed_url.netloc)
    elif parsed_url.path:
      # Accepts an URL without scheme like '192.168.0.5:5000'.
      self.nodes.add(parsed_url.path)
    else:
      raise ValueError('Invalid URL')

  def valid_chain(self, chain):
    """
    Determine if a given blockchain is valid

    :param chain: A blockchain
    :return: True if valid, False if not
    """

    last_block = chain[0]
    current_index = 1

    while current_index < len(chain):
      block = chain[current_index]
      # Check that the hash of the block is correct
      if block['previous_hash'] != self.hash(last_block):
        return False

      # Check that the Proof of Work is correct
      if not self.valid_proof(last_block['proof'], block['proof'], block['previous_hash']):
        return False

      last_block = block
      current_index += 1

    return True

  def resolve_conflicts(self):
    """
    This is our consensus algorithm, it resolves conflicts
    by replacing our chain with the longest one in the network.

    :return: True if our chain was replaced, False if not
    """

    neighbors = self.nodes
    new_chain = None

    # We're only looking for chains longer than ours
    max_length = len(self.chain)

    # Grab and verify the chains from all the nodes in our network
    for node in neighbors:
      url = 'http://%s/chain' % node
      try:
        response = requests.get(url, timeout=1)
      except:
        print('contact node %s failed, continue...' % url)
        continue

      if response.status_code == 200:
        length = response.json()['length']
        chain = response.json()['chain']

        # Check if the length is longer and the chain is valid
        if length > max_length and self.valid_chain(chain):
          max_length = length
          new_chain = chain

    # Replace our chain if we discovered a new, valid chain longer than ours
    if new_chain:
      self.chain = new_chain
      return True

    return False

  def new_block(self, proof, previous_hash=None):
    """
    Create a new Block in the Blockchain

    :param proof: The proof given by the Proof of Work algorithm
    :param previous_hash: Hash of previous Block
    :return: New Block
    """
    #assert len(self.current_transactions) == 1

    block = {
      'index': len(self.chain) + 1,
      'timestamp': time(),
      'transactions': self.current_transactions,
      'proof': proof,
      'previous_hash': previous_hash or self.hash(self.last_block),
    }

    # Reset the current list of transactions
    self.current_transactions = []

    self.chain.append(block)
    block_string = json.dumps(block, sort_keys=True, use_decimal=True)
    self.mTree.add_leaf(block_string, do_hash=True)
    self.mTree.make_tree()
    return block

  def get_block_of_txn(self, txn_id):
    for b in self.chain:
      if b['transactions'] and b['transactions'][0]['id'] == txn_id:
        return b

    return None

  def new_transaction(self, form):
    """
    Creates a new transaction to go into the next mined Block

    :param sender: Address of the Sender
    :param recipient: Address of the Recipient
    :param amount: decimal
    :return: The index of the Block that will hold this transaction
    """
    self.current_transactions.append(form)

    return self.last_block['index'] + 1

  @property
  def last_block(self):
    return self.chain[-1]

  @staticmethod
  def hash(block):
    """
    Creates a SHA-256 hash of a Block

    :param block: Block
    """
    block_string = json.dumps(block, sort_keys=True, use_decimal=True).encode()
    return hashlib.sha256(block_string).hexdigest()

  def proof_of_work(self, last_block):
    """
    Simple Proof of Work Algorithm:

     - Find a number p' such that hash(pp') contains leading 4 zeroes
     - Where p is the previous proof, and p' is the new proof

    :param last_block: <dict> last Block
    :return: <int>
    """

    last_proof = last_block['proof']
    last_hash = self.hash(last_block)

    proof = 0
    while self.valid_proof(last_proof, proof, last_hash) is False:
      proof += 1

    return proof, last_hash

  @staticmethod
  def valid_proof(last_proof, proof, last_hash):
    """
    Validates the Proof

    :param last_proof: <int> Previous Proof
    :param proof: <int> Current Proof
    :param last_hash: <str> The hash of the Previous Block
    :return: <bool> True if correct, False if not.

    """

    guess = f'{last_proof}{proof}{last_hash}'.encode()
    guess_hash = hashlib.sha256(guess).hexdigest()
    return guess_hash[:4] == "0000"
