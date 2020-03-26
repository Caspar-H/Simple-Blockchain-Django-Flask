import json
from uuid import uuid4

from django.http import HttpResponse, JsonResponse
from django.shortcuts import render

# Create your views here.
# Generate a globally unique address for this node
from blockchainapp.utils import blockchainclass
from django.views.decorators.csrf import csrf_exempt

node_identifier = str(uuid4()).replace('-', '')

# Instantiate the blockchain
blockchain = blockchainclass.Blockchain()


def test(request):
    return HttpResponse('test')


def mine(request):
    last_block = blockchain.last_block
    last_proof = last_block['proof']
    proof = blockchain.proof_of_work(last_proof)

    # We must receive a reward for finding the proof.
    # The sender is "0" to signify that this node has mined a new coin.
    blockchain.new_transaction(
        sender="0",
        recipient=node_identifier,
        amount=1,
    )

    # forge the new block by adding it to the chain
    previous_hash = blockchain.hash(last_block)
    block = blockchain.new_block(proof, previous_hash)

    response = {
        'message': "New Block Forged",
        'index': block['index'],
        'transactions': block['transactions'],
        'proof': block['proof'],
        'previous_hash': block['previous_hash'],
    }

    return JsonResponse(data=response, status=200)


def full_chain(request):
    response = {
        'chain': blockchain.chain,
        'length': len(blockchain.chain)
    }

    return JsonResponse(response, status=200)


@csrf_exempt
def new_transaction(request):
    print(request.body)
    values = json.loads(request.body)
    print(values)
    # Check that the required fields are in the POST'ed data
    required = ['sender', 'recipient', 'amount']
    print(type(values), type(required))
    if not all(k in values for k in required):
        return 'Missing values', 400

    # Create a new Transaction
    index = blockchain.new_transaction(values['sender'], values['recipient'],
                                       values['amount'])

    response = {'message': f'Transaction will be added to Block {index}'}
    return JsonResponse(response, status=201)

@csrf_exempt
def register_nodes(request):
    values = json.loads(request.body)

    nodes = values.get('nodes')
    if nodes is None:
        return "Error: Please supply a valid list of nodes", 400

    for node in nodes:
        blockchain.register_node(node)

    response = {
        'message': 'New nodes have been added',
        'total_nodes': list(blockchain.nodes),
    }
    return JsonResponse(response, status=201)


def consensus(request):
    replaced = blockchain.resolve_conflicts()

    if replaced:
        response = {
            'message': 'Our chain was replaced',
            'new_chain': blockchain.chain,
        }
    else:
        response = {
            'message': 'Our chain is authoritative',
            'chain': blockchain.chain,
        }

    return JsonResponse(response, status=200)