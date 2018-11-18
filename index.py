from bottle import (
    run,
    request,
    response,
    post,
    get,
    abort
)
import json

from blockchain import Blockchain
blockchain = None

nodes = set()

@get("/chain")
def chain():
    res_data = {
        "chain": blockchain.chain,
        "length": len(blockchain.chain)
    }

    response.set_header(
        "content-type", "application/json"
    )
    return json.dumps(res_data)

@post("/nodes/register")
def node_register():
    data = request.json
    _nodes = data["nodes"]
    for node in _nodes:
        nodes.add(node)

    res_data = {
        "nodes": list(nodes)
    }
    response.set_header(
        "content-type",
        "application/json"
    )

    return json.dumps(res_data)


def main():
    global blockchain
    blockchain = Blockchain()
    run(port=2000, debug=True, reloader=True)


if __name__ == "__main__":
    main()
