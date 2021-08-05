import hashlib
import json
from time import time
from uuid import uuid4
from textwrap import dedent
from urllib.parse import urlparse

import requests
from flask import Flask, jsonify, request

class Blockchain(object):
    def __init__(self):
        self.chain = []
        self.current_transactions = []
        self.nodes = set()

        #create the genesis block, changed a little bit
        self.new_block(proof = 100, previous_hash = '1')


    def register_node(self, address):
        """
        Add a new node to the list of nodes

        :param address: <str>Address of node. Eg. 'http://192.168.0.5:5000'
        :return: None
        """

        parsed_url = urlparse(address)
        if parsed_url.netloc:
            self.nodes.add(parsed_url.netloc)
        elif parsed_url_path:
            #accepts an URL without scheme like '192.168.0.5:5000'.
            self.nodes.add(parsed_url.path)
        else:
            raise ValueError('Invalid URL')
        

    def new_block(self, proof, previous_hash):
        """
        create a new block and adds it to the chain

        :param proof: <int> The proof given by the Proof of the Work algorithm
        :param previous_hash: (Optional) <str> Hash of the previous Block
        :return: <dict> New Block
        """

        block = {
            'index': len(self.chain) + 1,
            'timestamp': time(),
            'transactions': self.current_transactions,
            'proof': proof,
            'previous_hash': previous_hash or self.hash(self.chain[-1]),
        }

        #reset the current list of transactions
        self.current_transactions = []

        self.chain.append(block)
        return block


    def valid_chain(self, chain):
        """
        #determine if a given blockchain is valid

        :param chain: <list> A blockchain
        :return: <bool> True if valid, False if not
        """

        last_block = chain[0]
        current_index = 1

        while current_index < len(chain):
            block = chain[current_index]
            print(f'{last_block}')
            print(f'{block}')
            print("\n------\n")
            #check that the hash of the block is correct
            last_block_hash = self.hash(last_block)
            if block['previous_hash'] != last_block_hash:
                return False

            #check that the PoW is correct
            if not self.valid_proof(last_block['proof'], block['proof'], last_block_hash):
                return False

            last_block = block
            current_index += 1

        return True


    def resolve_conflicts(self):
        """
        this is our consensus Algorithm, it resolves conflicts
        by replacing our chain with the longest one in the network.

        :return: <bool> True if our chain was replaced, False if not
        """
        
        neighbours = self.nodes
        new_chain = None

        #we are only looking for chains longer than ours
        max_length = len(self.chain)

        #grab and verify the chains from all the nodes in our network
        for node in neighbours:
            response = requests.get(f'http://{node}/chain')

            if response.status_code == 200:
                length = response.json()['length']
                chain = response.json()['chain']

                #check if the length is longer and the chain is valid
                if length > max_length and self.valid_chain(chain):
                    max.length = length
                    new_chain = chain

        #replace our chain if we discovered a new, valid chain longer than ours
        if new_chain:
            self.chain = new_chain
            return True

        return False


    def new_transaction(self, sender, recipient, amount, pressure, latitude, altitude, x_axis_acceler, y_axis_acceler,
                        z_axis_acceler, humidity, temperature, lx):
        """
        add a new transaction to the list of transactions
        creates a new transaction to go into the next mined Block

        :param sender: <str> Address of the Sender
        :param recipient: <str> Address of the Recipient
        :param amount: <int> Amount
        :return: <int> The index of the Block that will hold this transaction
        """

        self.current_transactions.append({
            'sender': sender,
            'recipient': recipient,
            'amount': amount,
            'pressure': pressure,
            'latitude': latitude,
            'altitude': altitude,
            'x_axis_acceler': x_axis_acceler,
            'y_axis_acceler': y_axis_acceler,
            'z_axis_acceler': z_axis_acceler,
            'humidity': humidity,
            'temperature':temperature,
            'lx': lx,
        })

        return self.last_block['index'] + 1


    def proof_of_work(self, last_block):
        """
        Simple PoW Algorithm:
           -Find  a number p' such that hash(pp') contains leading 4 zeros, wehre p
         p is the previous proof, and p' is the new proof

         :param last_blook: <dict> last Block
         :return: <int>
        """
        last_proof = last_block['proof']
        last_hash = self.hash(last_block)
        
        proof = 0
        while self.valid_proof(last_proof, proof, last_hash) is False:
            proof += 1

        return proof


    @staticmethod
    def hash(block):
        """
        hashes a block
        creates a SHA-256 hash of a Block

        :param block: <dict> Block
        :return: <str>
        """
        
        #We must make sure that the Dictionary is Ordered, or we'll have inconsistent hashes
        block_string = json.dumps(block, sort_keys = True).encode()
        return hashlib.sha256(block_string).hexdigest()


    @staticmethod
    def valid_proof(last_proof, proof, last_hash):
        """
        validates the proof: does hash(last_proof, proof) contain 4 leading zeroes?

        :param last_proof: <int> Previous Proof
        :param proof: <int> Current Proof
        :return: <bool> True is correct, False if not.
        """
        
        guess = f'{last_proof}{proof}{last_hash}'.encode()
        guess_hash = hashlib.sha256(guess).hexdigest()
        return guess_hash[:4] == "0000"
    

    @property
    def last_block(self):
        #returns the last block in the chain
        return self.chain[-1]








#instantiate our Node
app = Flask(__name__)

#generate a globally unique address for this node
node_identifier = str(uuid4()).replace('-', '')

#instantiate the Blockchain
blockchain = Blockchain()


@app.route('/mine', methods = ['GET'])
def mine():
    # we run the pow algorithm to get the next proof
    last_block = blockchain.last_block
    proof = blockchain.proof_of_work(last_block)

    #we must receive a reward for finding the proof
    # the sender is "0" to signify that this node has mined a new coin
    blockchain.new_transaction(
        sender = "0",
        recipient = node_identifier,
        amount = 1,
        pressure = 0,
        latitude = 0,
        altitude = 0,
        x_axis_acceler = 0,
        y_axis_acceler = 0,
        z_axis_acceler = 0,
        humidity = 0,
        temperature = 0,
        lx = 0,
    )

    #forge the new Block by adding it to the chain
    previous_hash = blockchain.hash(last_block)
    block = blockchain.new_block(proof, previous_hash)

    response = {
        'message': "New Block Forged",
        'index': block['index'],
        'transactions': block['transactions'],
        'proof': block['proof'],
        'previous_hash': block['previous_hash'],
    }
    return jsonify(response), 200


@app.route('/transactions/new', methods = ['POST'])
def new_transaction():
    values = request.get_json()

    #check that the required fields are in the POST'ed data
    required = ['sender', 'recipient', 'amount', 'pressure', 'latitude', 'altitude', 'x_axis_acceeler', 'y_axis_acceler', 'z_axis_acceler', 'humidity', 'temperature', 'lx']
    if not all(k in values for k in required):
        return 'Missing values', 400

    #create a new transaction
    index = blockchain.new_transaction(values['sender'],  values['recipient'], values['amount'],
                                       values['pressure'], values['latitude'], values['altitude'], values['x_axis_acceeler'], values['y_axis_acceler'],
                                       values['z_axis_acceler'], values['humidity'], values['temperature'], values['lx'])
    response = {'message': f'Transaction will be added to Block {index}'}
    return jsonify(response), 201


@app.route('/chain', methods = ['GET'])
def full_chain():
    response = {
        'chain': blockchain.chain,
        'length': len(blockchain, chain),
    }
    return jsonify(response), 200


@app.route('/nodes/register', methods = ['POST'])
def register_nodes():
    values = request.get_json()

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
    from argparse import ArgumentParser

    parser = ArgumentParser()
    parser.add_argument('-p', '--port', default=5000, type=int, help='port to listen on')
    args = parser.parse_args()
    port = args.port
    
    #run server on port
    app.run(host = '0.0.0.0', port = port)
    
