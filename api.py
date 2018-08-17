from textwrap import dedent
from uuid import uuid4
from flask import Flask, jsonify, request

import Crypto.Random
from Crypto.PublicKey import RSA
from binascii import hexlify

import blockchain
import constant

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

    blockchain.add_transaction(
        constant.MINER_KEY, 
        node_uid, 
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

@api.route('/transactions/get', methods=['GET'])
def get_transactions():
    response = {'transactions': blockchain.current_transactions}
    return jsonify(response), 200

@api.route('/transactions/new', methods=['POST'])
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

@api.route('/chain', methods=['GET'])
def get_chain():
    chain = []
    for block in blockchain.chain:
        chain.append(block.dict)
    response = {
        'chain': chain,
        'length': len(blockchain.chain)
    }
    return jsonify(response), 200

@api.route('/peers/get', methods=['GET'])
def get_peers():
    response = {
        'peers': list(blockchain.peers)
    }
    return jsonify(response), 200

@api.route('/peers/register', methods=['POST'])
def register_peers():
    body = request.get_json()
    original_size = len(blockchain.peers)

    try:
        peers = body['peers']
        if peers is None:
            return 'Missing valid list of peers', 400
    except TypeError:
        return 'Missing valid list of peers', 400

    malformed_count = 0
    for peer in peers:
        if not blockchain.add_peer(peer):
            malformed_count += 1

    message = ''
    status_code = 200
    if malformed_count > 0:
        message = 'Some peers were malformed'
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

@api.route('/peers/resolve', methods=['GET'])
def reach_consensus():
    is_chain_replaced = blockchain.resolve()
    chain = []
    for block in blockchain.chain:
        chain.append(block.dict)

    response = {
        'chain': chain
    }

    if is_chain_replaced:
        response['message'] = 'Chain has been replaced!'
    else:
        response['message'] = 'Chain is authoritative'
    return jsonify(response), 200

@api.route('/wallet/new', methods=['GET'])
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
        '-p', 
        '--port', 
        default=8081, 
        type=int, 
        help='port to run service')
    args = parser.parse_args()
    port = args.port

    api.run(host='0.0.0.0', port=port)