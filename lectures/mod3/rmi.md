# Remote method invocations
FPNP3e ch18

[remote procedure call (RPC)](https://en.wikipedia.org/wiki/Remote_procedure_call)
---
- calls a function in another process or on a remote server similar to calling local function
- has benefits of process and data load balancing
- two ways to represents parameters and returned results
  - raw binary data whose meaning had to be known in advance
  - self-documenting textual representation such as
    - XML (eXtended Markup Language)
    - JSON (JavaScript Object Notation)
- has three features
  - lacks of strong semantics for the meaning of each call
    - depends on the particular API called
  - a way of invoking methods not defined by RPC but by the application
  - the function calls look normal and similar in the client and server code without elaboration in order to pass over network
- can be deployed on WSGI webframeworks and message queues


RPC limitations
---
- support limited data types and positional arguments
  - RPC bound to a specific programming language may support passing live objects
- RPC client raises an exception when there is an exception occurred on the server
  - these exceptions have to be handled in separate stack frames
- many RPC mechanisms provide introspection
  - clients need to discover the methods supported by a RPC service before use them
    - the types of method parameters are usually required to be discovered as well
- API addressing scheme must be known before hand such as
  - a tuple of (IP address, port number, and URL) addresses a method
- some RPC mechanisms support authentication, access control and authorization on RPC calls such as
  - HTTP basic authentication
  - [OAuth 2.0](https://oauth.net/)


[XML-RPC](https://en.wikipedia.org/wiki/XML-RPC)
---
- runs atop HTTP
- defined in [XML-RPC Specification](http://xmlrpc.com/spec.md)
- Data types: int; float; unicode; list; dict with unicode keys; with nonstandard extensions, datetime and None
- Libraries: 
  - [xmlrpc — XMLRPC server and client modules](https://docs.python.org/3/library/xmlrpc.html)


🔭 Explore
---
- [xmlrpc — XMLRPC server and client modules](https://docs.python.org/3/library/xmlrpc.html)
  - classes for server
  - classes for client


🖊️ Practice
---
- [An XML-RPC Server](./rmi/xmlrpc_server.py)
  - An XML-RPC service lives at a single URL of a web site
    - can be integrated with a normal web application
- [Asking an XML-RPC Server What Functions It Supports](./rmi/xmlrpc_introspect.py)
  - method signatures and documentation strings are retrieved
  - however, no data types for Python language
- [Making XML-RPC Calls](./rmi/xmlrpc_client.py)
  -  a proxy object is created for making function calls against the server 
  -  These calls look exactly like local method calls
- [Using XML-RPC Multicall](./rmi/xmlrpc_multicall.py)

```bash
# open 4 terminals, in each one, run the commands below accordingly
# pay attention to the server terminal on each run
# 1. run the rpc server
python3 xmlrpc_server.py

# 2. run the rpc client for introspection
python3 xmlrpc_introspect.py

# 3. invoke rpc methods
python3 xmlrpc_client.py

# 4. muticall
python3 xmlrpc_multicall.py
```
- investigate the HTTP requests and responses for XML-RPC with Wireshark
  - find the XML representations for method parameters and returned values


XML-RPC features and limitations
---
- does not impose any restrictions on the argument types
  - *addtogether()* works with either strings or numbers
    - and any number of arguments
- can only return a single result value
  - might be a complex data structure
- supports a smaller set of data types than Python data types
  - only supports a single sequence type: the list
- supports recursive complex data structures
- passes exception in the function on the server back acrossthe network and represents locally on the client by an *xmlrpclib.Fault* instance
- supports *dates* and the value *None*
- passes a dictionary as a function's final argument to mimic keyword arguments
  - the dictionary key type must be string


[JSON-RPC](https://en.wikipedia.org/wiki/JSON-RPC)
---
- serializes data structures to strings in JavaScript syntax
  - JSON strings could be turned back into data in a web browser using *eval()*
    - insecure so a formal JSON parser is preferred
- more compact and simple than XML
- runs atop HTTP
- defined in [JSON-RPC Specification](https://www.jsonrpc.org/specification)
- supported data types: int; float; unicode; list; dict with unicode keys; None
- supports attaching id values to each request for asynchrony
- many third-party libraries such as
  - [JSONRPClib-pelix](https://jsonrpclib-pelix.readthedocs.io/)
  - [jsonrpclib](https://github.com/joshmarshall/jsonrpclib)
  - [json-rpc](https://json-rpc.readthedocs.io/)


🖊️ Practice
---
- [A JSON-RPC Server](./rmi/jsonrpc_server.py)
- [A JSON-RPC Client](./rmi/jsonrpc_client.py)
- investigate the json rpc messages with Wireshark
```python
# open 2 terminals, one runs the jsonrpc server
python3 jsonrpc_server.py

# the other runs the jsonrpc client
python3 jsonrpc_client.py
```


Self-Documenting Data
---
- both XML-RPC and JSON-RPC expect you to use their key-value types
  - *struct* in XML-RPC
  - *object* in JSON-RPC
  - key type is limited to be string
  - RPC-appropriate data structure is a list of key-values
  ```python
  # convert python dictionary to self-descriptive rpc list
  elements = {1: 'H', 2:'He'}
  t = [{'number': key, 'symbol': value} for key, value in elements.items()]
  # convert back
  {obj['number']: obj['symbol']) for obj in t}
  ```


Talking About Objects: Pyro and RPyC
---
- Some complex RPC mechanisms support transmitting objects such as
  - [SOAP (Simple Object Access Protocol)](https://en.wikipedia.org/wiki/SOAP)
  - [Common Object Request Broker Architecture (CORBA)](https://en.wikipedia.org/wiki/Common_Object_Request_Broker_Architecture)
- [Pyro - Python Remote Objects](https://pyro4.readthedocs.io/) supports transmitting pickle-able objects
- [RPyC - Transparent, Symmetric Distributed Computing](https://rpyc.readthedocs.io) transmitting object reference used to call back and invoke its methods
  - security is concerned such as exposing dangerous methods


🖊️ Practice
---
- [An RPyC Client](./rmi/rpyc_client.py)
- [An RPyC Server](./rmi/rpyc_server.py)



Recovering from Network Errors
---
- services that offer idempotent operations can safely be retried
  - wrap unsafe operations in safe transactions
- use try and except to wrap larger pieces of code with a solid semantic meaning and can be reattempted or recovered from
- RPC-specific error such as KeyError and ValueError are more helpful


Further topics
---
- [Web service](https://en.wikipedia.org/wiki/Web_service)
  - [REST (Representational state transfer)](https://en.wikipedia.org/wiki/REST)
- [Top 5 Python REST API Frameworks](https://www.moesif.com/blog/api-product-management/api-analytics/Top-5-Python-REST-API-Frameworks/)
  - [Flask-RESTful ](https://flask-restful.readthedocs.io/)
  - [Designing RESTful APIs with Python and Flask](https://auth0.com/blog/developing-restful-apis-with-python-and-flask/)


🔭 Explore
---
- [Web administration for JAMES](https://james.apache.org/server/manage-webadmin.html)


# References
- [Designing a RESTful API with Python and Flask](http://www.pythondoc.com/flask-restful/first.html)
