from bottle import (
    run,
    request,
    response,
    post,
    get,
    abort
)
import json

nodes = set()

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


if __name__ == "__main__":
    run(port=2000, debug=True, reloader=True)