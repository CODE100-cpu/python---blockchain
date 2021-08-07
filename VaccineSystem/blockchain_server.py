from uuid import uuid4
from flask import Flask, jsonify, request, render_template
from blockchain import Blockchain


#instantiate our Node
app = Flask(__name__)
# app.json_encoder = MyEncoder

#generate a globally unique address for this node
node_identifier = str(uuid4()).replace('-', '')

#instantiate the Blockchain
blockchain = Blockchain()

@app.route('/', methods=['GET'])
def hello_world():
    """
    Welcome to Blockchain message
    :return: HTML
    """
    response = {
        'header': 'Welcome to BlockchainDB'
    }
    return render_template('landing.html', data=response)

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
    blockchain.blocks.insert_one(block)
    block.pop('_id')

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
        'length': len(blockchain.chain),
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
    # app.run()
