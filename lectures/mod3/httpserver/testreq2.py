from werkzeug.serving import run_simple
from werkzeug.wrappers import Request, Response

def application(environ, start_response):
    request = Request(environ)
    
    # Print request method and path
    print(f"Received {request.method} request for {request.path}")
    
    # Print headers
    print("Headers:")
    for key, value in request.headers.items():
        print(f"  {key}: {value}")
    
    # Print body if present
    if request.data:
        print("Body:")
        print(request.data.decode("utf-8"))
    
    print("-" * 40)
    
    # Send a simple 200 OK response
    response = Response("Request received and logged.", content_type="text/plain")
    return response(environ, start_response)

if __name__ == "__main__":
    run_simple('localhost', 8080, application)
