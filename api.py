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
    last_proof = last_blk['proof']
    proof = blockchain.proof_of_work(last_proof)

    blockchain.add_transaction(sender='0', receiver=node_uid, amt=1)

    prev_hash = blockchain.hash(last_blk)
    blk = blockchain.add_block(proof, prev_hash)

    response = {
        'message': 'New block forged!',
        'index': blk['index'],
        'transactions': blk['transactions'],
        'proof': blk['proof'],
        'previous_hash': blk['prev_hash']
    }

    return jsonify(response), 201

@api.route('/transact', methods=['POST'])
def new_transaction():
    body = request.get_json()
    required_params = ['sender', 'receiver', 'amount']

    try:
        if not all(e in body for e in required_params):
            return 'Missing parameters - include: sender, receiver, amount', 400
    except TypeError:
        return 'Missing parameters - include: sender, receiver, amount', 400

    index = blockchain.add_transaction(body['sender'], body['receiver'], body['amount'])
    response = {'message': f'Transaction will be appended to block {index}'}
    return jsonify(response), 201

@api.route('/chain', methods=['GET'])
def chain():
    response = {
        'chain': blockchain.chain,
        'length': len(blockchain.chain)
    }
    return jsonify(response), 200

if __name__ == '__main__':
    api.run(host='0.0.0.0', port=5000)