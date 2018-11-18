from bottle import route, run, abort
from bottle import post, get, put, delete, request, response
import json
from uuid import uuid4

from blockchain import Blockchain

node_id = str(uuid4()).replace('-', '')

blockchain = Blockchain()

@post("/nodes/register")
def register_node():
    values = request.json
    nodes = values.get("nodes")

    for node in nodes:
        blockchain.register_node(node)
    
    return ""


@get("/nodes/resolve")
def consensus():
    replaced = blockchain.resolve_conficts()

    if replaced:
        return "Replaced"
    else:
        return "Not replaced"

@post("/transactions/new")
def new_transaction():
    values = request.json
    required = ["sender", "recipient", "amount"]
    if not all(k in values for k in required):
        abort(400, "Wrong parameter")
    
    index = blockchain.new_transaction(
        values["sender"],
        values["recipient"],
        values["amount"]
    )

    res_data = {
        "message": f"トランザクションはブロック{index}に追加されました。"
    }

    return json.dumps(res_data)

@get("/mine")
def mine():
    last_block = blockchain.last_block
    last_proof = last_block["proof"]
    proof = blockchain.proof_of_work(last_proof)

    blockchain.new_transaction(
        sender="0",
        recipient=node_id,
        amount=1
    )

    block = blockchain.new_block(proof)

    res_data = {
        "message": "新しいブロックを採掘しました",
        "index": block["index"],
        "transactions": block["transactions"],
        "proof": block["proof"],
        "previous_hash": block["previous_hash"]
    }

    return json.dumps(res_data)


@get("/chain")
def full_chain():
    response.set_header("content-type", "application/json")
    res_data = {
        "chain": blockchain.chain,
        "length": len(blockchain.chain)
    }

    return json.dumps(res_data)


if __name__ == "__main__":
    import sys
    port = sys.argv[1]
    run(host="localhost", port=port, debug=True, reloader=True)
