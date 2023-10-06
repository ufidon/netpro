# HTTP servers
FPNP3e ch10


Objectives
---
- Learn off-the-shelf solutions for the major server patterns
- Respond to HTTP requests by
  - returning documents or web API


PSL builtin HTTP server
---
- serve files at specified directory
  - used as a file server

```bash
python3 -m http.server -h
```

WSGI ( Web Server Gateway Interface)
---
- Refer to the WSGI standard [PEP 3333](https://peps.python.org/pep-3333/) for further info

Asynchronous Server-Frameworks 
Forward and Reverse Proxies 
Four Architectures 
Running Python Under Apache  
The Rise of Pure-Python HTTP Servers  
The Benefits of Reverse Proxies  
Platforms as a Service 
GET and POST Patterns and the Question of REST 
WSGI Without a Framework