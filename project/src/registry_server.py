#!/usr/bin/env python
from datetime import datetime
import json
import os, logging, sys

# Third party module
import requests
from flask import Flask, render_template, request, redirect, url_for

import logic as l

# create a Flask app
app = Flask(__name__)

@app.route('/entity', methods=['POST'])
def legal_entity_create():
  # TODO: if exists, update existing object in db
  post_data = request.form
  res = l.create_legal_entity(post_data)
  return res, 201

@app.route('/entity/<idx>', methods=['GET'])
def legal_entity_get(idx):
  entity_strings = l.get_legal_entities([idx,])
  if entity_strings:
    return entity_strings[0]
  else:
    return 'no legal entity found'

@app.route('/entity/<idx>', methods=['DELETE'])
def legal_entity_delete(idx):
  return l.delete_legal_entities([idx,]), 202

@app.route('/product', methods=['POST'])
def product_create():
  # TODO: if exists, update existing object in db
  post_data = request.form
  res = l.create_product(post_data)
  return res, 201

@app.route('/product/<sku>', methods=['GET'])
def product_get(sku):
  product_strings = l.get_products([sku,])
  if product_strings:
    return product_strings[0]
  else:
    return 'no product found'

@app.route('/product/<sku>', methods=['DELETE'])
def product_delete(sku):
  return l.delete_products([sku,]), 202

# Homepage
@app.route('/')
def index():
  return 'registry server'

if __name__ == '__main__':
  app.run(host='0.0.0.0', port=5001, debug=True)
