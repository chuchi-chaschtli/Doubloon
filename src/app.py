from uuid import uuid4
from flask import Flask, jsonify, request

import Crypto.Random
from Crypto.PublicKey import RSA
from binascii import hexlify

import blockchain
import constant

# Node instantiation
app = Flask(__name__)
node_address = str(uuid4()).replace('-', '')

# Blockchain instantiation
blockchain = blockchain.Blockchain()

@app.route('/mine', methods=['GET'])
def mine():
    last_blk = blockchain.last_block
    last_proof = last_blk.proof
    proof = blockchain.proof_of_work(last_proof)

    blockchain.add_transaction(
        constant.MINER_KEY, 
        node_address, 
        constant.MINER_REWARD, 
        "")

    prev_hash = last_blk.hash
    blk = blockchain.add_block(proof, prev_hash)

    response = {
        'message': 'New block mined!',
        'index': blk['index'],
        'transactions': blk['transactions'],
        'proof': blk['proof'],
        'previous_hash': blk['prev_hash']
    }

    return jsonify(response), 201

@app.route('/transactions/get', methods=['GET'])
def get_transactions():
    response = {'transactions': blockchain.current_transactions}
    return jsonify(response), 200

@app.route('/transactions/new', methods=['POST'])
def new_transaction():
    body = request.get_json()
    required_params = ['sender', 'receiver', 'amount', 'signature']

    try:
        if not all(e in body for e in required_params):
            return 'Missing parameters', 400
    except TypeError:
        return 'Missing parameters', 400

    result = blockchain.add_transaction(
        body['sender'], 
        body['receiver'], 
        body['amount'],
        body['signature'])
    if result < 0:
        response = {'message': 'Invalid transaction'}
        return jsonify(response), 406
    else:
        response = {'message': 
                    f'Transaction will be appended to block {result}'}
        return jsonify(response), 201

@app.route('/chain', methods=['GET'])
def get_chain():
    chain = []
    for block in blockchain.chain:
        chain.append(block.dict)
    response = {
        'chain': chain,
        'length': len(blockchain.chain)
    }
    return jsonify(response), 200

@app.route('/chain/resolve', methods=['GET'])
def consensus():
    is_chain_replaced = blockchain.resolve()
    chain = []
    for block in blockchain.chain:
        chain.append(block.dict)

    response = {
        'message': '',
        'chain': chain
    }

    if is_chain_replaced:
        response['message'] = 'Chain has been replaced!'
    else:
        response['message'] = 'Chain is authoritative'
    return jsonify(response), 200

@app.route('/peers/get', methods=['GET'])
def get_peers():
    response = {
        'peers': list(blockchain.peers)
    }
    return jsonify(response), 200

@app.route('/peers/register', methods=['POST'])
def register_peers():
    body = request.get_json()
    original_size = len(blockchain.peers)

    try:
        peers = body['peers']
        if peers is None:
            return 'Missing valid list of peers', 400
    except TypeError:
        return 'Missing valid list of peers', 400

    any_malformed = any(not blockchain.add_peer(peer) for peer in peers)

    message = ''
    status_code = 200
    if any_malformed:
        message = 'Some given peers were malformed'
    elif original_size == len(blockchain.peers):
        message = 'No new peers added'
    else:
        message = 'New peers have been added'
        status_code = 201
    response = {
        'message': message,
        'total_peers': list(blockchain.peers)
    }
    return jsonify(response), status_code

@app.route('/wallet/new', methods=['GET'])
def new_wallet():
    rng = Crypto.Random.new().read
    priv_key = RSA.generate(1024, rng)
    publ_key = priv_key.publickey()
    response = {
        'message': 'Notice: Save these keys!!!',
        'private_key': hexlify(priv_key.exportKey(format='DER')).decode(
            'utf8'),
        'public_key': hexlify(publ_key.exportKey(format='DER')).decode(
            'utf8')
    }
    return jsonify(response), 201

if __name__ == '__main__':
    from argparse import ArgumentParser

    parser = ArgumentParser(description='Blockchain command line')
    parser.add_argument(
        '-host', 
        '--host', 
        default='127.0.0.1', 
        help='host to run service')
    parser.add_argument(
        '-p', 
        '--port', 
        default=8081, 
        type=int, 
        help='port to run service')
    args = parser.parse_args()

    app.run(host=args.host, port=args.port)