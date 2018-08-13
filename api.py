from textwrap import dedent
from uuid import uuid4
from flask import Flask, jsonify, request

import blockchain

# Node instantiation
api = Flask(__name__)
node_uid = str(uuid4()).replace('-', '')

# Blockchain instantiation
blockchain = blockchain.Blockchain()

@api.route('/mine', methods=['GET'])
def mine():
    last_blk = blockchain.last_block
    last_proof = last_blk.proof
    proof = blockchain.proof_of_work(last_proof)

    blockchain.add_transaction(sender='0', receiver=node_uid, amt=1)

    prev_hash = last_blk.hash()
    blk = blockchain.add_block(proof, prev_hash)

    response = {
        'message': 'New block mined!',
        'index': blk['index'],
        'transactions': blk['transactions'],
        'proof': blk['proof'],
        'previous_hash': blk['prev_hash']
    }

    return jsonify(response), 201

@api.route('/transactions/new', methods=['POST'])
def new_transaction():
    body = request.get_json()
    required_params = ['sender', 'receiver', 'amount']

    try:
        if not all(e in body for e in required_params):
            return 
            'Missing parameters - include: sender, receiver, amount', 400
    except TypeError:
        return 'Missing parameters - include: sender, receiver, amount', 400

    index = blockchain.add_transaction(
        body['sender'], 
        body['receiver'], 
        body['amount'])
    response = {'message': f'Transaction will be appended to block {index}'}
    return jsonify(response), 201

@api.route('/chain', methods=['GET'])
def chain():
    chain = []
    for block in blockchain.chain:
        chain.append(block.to_dict())
    response = {
        'chain': chain,
        'length': len(blockchain.chain)
    }
    return jsonify(response), 200

@api.route('/neighbors/register', methods=['POST'])
def register_neighbors():
    body = request.get_json()

    try:
        neighbors = body['neighbors']
        if neighbors is None:
            return 'Missing valid list of neighbors', 400
    except TypeError:
        return 'Missing valid list of neighbors', 400

    for neighbor in neighbors:
        blockchain.add_neighbor(neighbor)

    response = {
        'message': 'New neighbors have been added',
        'total_neighbors': list(blockchain.neighbors)
    }
    return jsonify(response), 201

@api.route('/neighbors/resolve', methods=['GET'])
def reach_consensus():
    is_chain_replaced = blockchain.resolve()
    chain = []
    for block in blockchain.chain:
        chain.append(block.to_dict())

    response = {
        'chain': chain
    }

    if is_chain_replaced:
        response['message'] = 'Chain has been replaced!'
    else:
        response['message'] = 'Chain is authoritative'
    return jsonify(response), 200

if __name__ == '__main__':
    api.run(host='0.0.0.0', port=5000)