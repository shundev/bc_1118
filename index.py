from bottle import (
    run,
    request,
    response,
    post,
    get,
    abort
)

@get("/")
def index():
    return "Hello, bottle!!"


if __name__ == "__main__":
    run(port=2000, debug=True, reloader=True)