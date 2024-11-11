
# Web API
This lab gives your hands-on experience on web services that covers investigating an public API, creating your own API with Flask, and securing it with [Bearer Token Authentication](https://datatracker.ietf.org/doc/html/rfc6750). Each task is broken down step-by-step, including testing with `cURL` and Python's `Requests` library.

- **Objective**: Learn to access public RESTful APIs, create a simple web service with Flask, and secure it with Bearer Token Authentication.
- **Tools Needed**: Python, Flask, `cURL`, and Python’s `Requests` library.
- **Prerequisites**: Basic knowledge of Python and RESTful APIs.

In your report, 
- 🎏 explain the code you added or modified and actions taken
- 💻 illustrate with screenshots of corresponding outputs



A [RESTful API (Representational State Transfer API)](https://en.wikipedia.org/wiki/REST) is a web service that follows the principles of REST architecture. It allows different software systems to communicate over the internet using HTTP requests, enabling a client (such as a mobile app or web browser) to interact with a server to create, read, update, or delete resources.

## Key Concepts of RESTful APIs

1. **Resources**: 
   - In a RESTful API, resources are the main objects or data that the API interacts with, such as "users," "orders," or "products."
   - Each resource has a unique identifier, often a URL, called an **endpoint**. For example, a resource for a user profile might be accessible at `https://api.example.com/users/123`.

2. **HTTP Methods**:
   - REST APIs use standard HTTP methods to perform actions on resources:
     - **GET**: Retrieve data from the server (e.g., a list of users or details of a specific user).
     - **POST**: Create a new resource on the server (e.g., adding a new user).
     - **PUT** or **PATCH**: Update an existing resource on the server (e.g., modifying user information).
     - **DELETE**: Remove a resource from the server (e.g., deleting a user).

3. **Stateless Communication**:
   - RESTful APIs are stateless, meaning each request from a client to the server must contain all the information the server needs to fulfill that request. The server does not store any client state between requests, making each request independent.

4. **Uniform Interface**:
   - RESTful APIs follow a consistent, standardized approach. For example, the URL structure is often organized by resource type (`/users`, `/products`), and HTTP methods correspond to specific actions, making the API predictable and easy to use.

5. **Data Format**:
   - RESTful APIs often use **JSON** (JavaScript Object Notation) for data exchange, as it is lightweight, easy to read, and compatible across platforms. However, some APIs also support **XML** or other formats.

6. **Stateless Responses**:
   - The server responds with only the necessary data for the request, and it doesn’t retain client information between requests. This statelessness allows the server to handle many requests efficiently.

## Example of a RESTful API in Action

Let's say we have a RESTful API for managing a simple blog with resources like posts and comments. Here’s how different requests might look:

- **GET** request to list all blog posts:
  ```
  GET https://api.example.com/posts
  ```

- **POST** request to create a new blog post:
  ```
  POST https://api.example.com/posts
  Body:
  {
    "title": "My New Post",
    "content": "This is the content of my new post."
  }
  ```

- **GET** request to retrieve a specific post:
  ```
  GET https://api.example.com/posts/123
  ```

- **PUT** request to update a specific post:
  ```
  PUT https://api.example.com/posts/123
  Body:
  {
    "title": "Updated Title",
    "content": "Updated content."
  }
  ```

- **DELETE** request to delete a specific post:
  ```
  DELETE https://api.example.com/posts/123
  ```

## Advantages of RESTful APIs

- **Scalability**: Statelessness and resource-based design make RESTful APIs suitable for scaling across large applications.
- **Interoperability**: RESTful APIs use widely adopted standards (HTTP and JSON), making them compatible with a wide range of clients.
- **Simplicity**: REST’s predictable URL structure and consistent use of HTTP methods simplify implementation and debugging.


---

## Task 1: Investigate a Public RESTful API — [IPinfo API](https://ipinfo.io/developers)

The **IPinfo API** is a RESTful web service that provides detailed information about IP addresses. It’s commonly used for **geolocation**, **network analysis**, and **IP threat detection**. When queried with an IP address, the IPinfo API returns data including:
- **IP Geolocation**: Provides approximate geographic location of an IP, down to the city level.
- **ASN Data**: Identifies the ISP and network owner, making it useful for network-related analysis.
- **Threat Intelligence**: Flags IP addresses associated with VPNs, proxies, and other privacy or security threats.
- **Carrier Information**: Identifies carrier data, making it helpful for mobile network analysis.
  
### Sample Response:
If you request data for `8.8.8.8` (Google’s public DNS), the API might return:

```json
{
  "ip": "8.8.8.8",
  "hostname": "dns.google",
  "city": "Mountain View",
  "region": "California",
  "country": "US",
  "loc": "37.3861,-122.0839",
  "org": "AS15169 Google LLC",
  "timezone": "America/Los_Angeles"
}
```

### Use Cases:
- **Website Localization**: Display content based on user location.
- **Network Security**: Identify suspicious or risky IP addresses.
- **Targeted Marketing**: Offer region-specific promotions or services.


### Step 1.1: Obtain an IPinfo API Key
1. Go to [IPinfo](https://ipinfo.io/) and create a free account.
2. After creating an account, you will receive an API token.

### Step 1.2: Access IPinfo API with cURL
To test the [IPinfo API](https://ipinfo.io/developers), make a `GET` request with your token. The request retrieves location information for an IP address.

```bash
# Replace 'your_api_token' with your actual IPinfo API token
curl -v "https://ipinfo.io/8.8.8.8?token=your_api_token"
```

### Step 1.3: Access IPinfo API with Python Requests
In Python, you can use the `requests` library to make a similar request.

```python
import requests

# Replace with your IPinfo token
token = "your_api_token"
url = f"https://ipinfo.io/8.8.8.8?token={token}"

response = requests.get(url)
if response.status_code == 200:
    print("Response JSON:", response.json())
else:
    print("Failed to retrieve data:", response.status_code)
```

### Step 1.4: [IPinfo Python Client Library](https://github.com/ipinfo/python)
This official library simplifies accessing IPinfo. Install the library first

```bash
pip install ipinfo
```

- Access IPinfo with the Python library `ipinfo`:

  ```python
  import ipinfo, pprint

  # Replace with your IPinfo token
  access_token = '123456789abc'

  handler = ipinfo.getHandler(access_token)
  ip_address = '216.239.36.21'
  details = handler.getDetails(ip_address)

  pprint.pprint(details.all)
  ```

---

## Task 2: Create a Simple Web Service Generating Lissajous curve GIFs

Let's rewrite the program in Lab08 to provide three distinct RESTful APIs:

1. `GET /get_params` - Retrieve the current Lissajous parameters.
2. `POST /set_params` - Update the Lissajous parameters (frequency, phase, curve color, background color).
3. `GET /generate_lissajous` - Generate the Lissajous curve GIF based on the current parameters.

### Step 2.1: Create the [web service](./code/t2.py)
```python
from flask import Flask, request, jsonify
import math
import base64
from io import BytesIO
from PIL import Image, ImageDraw

# Initial Lissajous parameters
params = {
    'freq': 1.0,
    'phase': 0.0,
    'curve_color': (0, 0, 0),  # Black curve
    'background_color': (255, 255, 255)  # White background
}

app = Flask(__name__)

# API 1: Retrieve Frequency, Phase, Curve Color, and Background Color Parameters
@app.route('/get_params', methods=['GET'])
def get_params():
    return jsonify(params), 200

# API 2: Update Frequency, Phase, Curve Color, and Background Color Parameters
@app.route('/set_params', methods=['POST'])
def set_params():
    data = request.json
    try:
        params['freq'] = float(data.get('freq', params['freq']))
        params['phase'] = float(data.get('phase', params['phase']))
        params['curve_color'] = tuple(map(int, data.get('curve_color', params['curve_color'])))
        params['background_color'] = tuple(map(int, data.get('background_color', params['background_color'])))
        return jsonify({"message": "Parameters updated successfully"}), 200
    except (ValueError, TypeError):
        return jsonify({"error": "Invalid input"}), 400

# API 3: Generate Lissajous Curve as a GIF
@app.route('/generate_lissajous', methods=['GET'])
def generate_lissajous():
    size = 100
    cycles = 5
    nframes = 64
    delay = 8
    frames = []
    freq = params['freq']
    phase = params['phase']
    curve_color = params['curve_color']
    background_color = params['background_color']

    for i in range(nframes):
        img = Image.new("RGB", (2 * size + 1, 2 * size + 1), background_color)
        draw = ImageDraw.Draw(img)
        for t in range(int(cycles * 2 * math.pi / 0.001)):
            x = math.sin(t * 0.001)
            y = math.sin(t * 0.001 * freq + phase)
            draw.point((size + int(x * size + 0.5), size + int(y * size + 0.5)), fill=curve_color)
        phase += 0.1
        frames.append(img)

    output = BytesIO()
    frames[0].save(output, format="GIF", save_all=True, append_images=frames[1:], loop=0, duration=delay * 10, disposal=2)
    return "data:image/gif;base64," + base64.b64encode(output.getvalue()).decode("ascii"), 200

if __name__ == "__main__":
    app.run(port=5000, debug=True)
```

### Explanation of Each API

1. **`GET /get_params`**:
   - Returns the current Lissajous parameters in JSON format.
   - **Example Response**:
     ```json
     {
       "freq": 1.0,
       "phase": 0.0,
       "curve_color": [0, 0, 0],
       "background_color": [255, 255, 255]
     }
     ```

2. **`POST /set_params`**:
   - Accepts a JSON payload with any of the parameters: `freq`, `phase`, `curve_color`, and `background_color`.
   - Updates only the parameters provided, leaving others unchanged.
   - **Example Request**:
     ```json
     {
       "freq": 2.0,
       "curve_color": [255, 0, 0]
     }
     ```

3. **`GET /generate_lissajous`**:
   - Generates a GIF of the Lissajous curve based on the current parameters and returns it as a Base64-encoded string.
   - **Example Response**: 
     ```json
     {
       "image": "data:image/gif;base64,<base64_encoded_string>"
     }
     ```

This setup provides three distinct endpoints for managing and generating Lissajous curve visualizations, with parameters easily configurable and a straightforward structure for testing.

### Step 2.2: Test each of the three APIs with `cURL` and Python `requests`:

### API 1: Retrieve Current Lissajous Parameters (`GET /get_params`)

#### Using cURL
```bash
curl -X GET http://127.0.0.1:5000/get_params
```

#### Using Python Requests
```python
import requests

response = requests.get("http://127.0.0.1:5000/get_params")
print("Current Parameters:", response.json())
```

---

### API 2: Update Lissajous Parameters (`POST /set_params`)

#### Using cURL
Replace the values in `data` as needed for updating parameters.

```bash
curl -X POST http://127.0.0.1:5000/set_params \
    -H "Content-Type: application/json" \
    -d '{"freq": 2.0, "phase": 0.5, "curve_color": [0, 255, 0], "background_color": [10, 0, 0]}'

# Check the update
curl -X GET http://127.0.0.1:5000/get_params    
```

#### Using Python Requests
```python
import requests

url = "http://127.0.0.1:5000/set_params"
data = {
    "freq": 1.2,
    "phase": 0.3,
    "curve_color": [0, 255, 255],
    "background_color": [10, 0, 10]
}

response = requests.post(url, json=data)
print("Update Response:", response.json())

# check the update
response = requests.get("http://127.0.0.1:5000/get_params")
print("Current Parameters:", response.json())
```

---

### API 3: Generate Lissajous Curve GIF (`GET /generate_lissajous`)

#### Using cURL
```bash
curl -X GET http://127.0.0.1:5000/generate_lissajous | sed 's/^data:image\/gif;base64,//' | base64 --decode > output1.gif
```

The response will be a Base64-encoded GIF. To view the image, you would need to decode and save it.

#### Using Python Requests
```python
import requests
import base64
from PIL import Image
from io import BytesIO

url = "http://127.0.0.1:5000/generate_lissajous"
response = requests.get(url)

# Extract the Base64 string, decode it, and save the image as a GIF
if response.status_code == 200:
    # Remove the data prefix and decode the Base64 string
    image_data = response.text.split(",")[1]
    gif_data = base64.b64decode(image_data)
    
    # Open the GIF data in memory as an image
    image = Image.open(BytesIO(gif_data))
    
    # Save the entire GIF animation properly
    image.save("lissajous1.gif", format="GIF", save_all=True)
    print("Animated GIF saved as 'lissajous1.gif'.")
    
    # To view it, open the GIF with the system's default viewer
    import webbrowser
    webbrowser.open("lissajous1.gif")
else:
    print("Failed to generate image:", response.status_code)
```

---

## Task 3: Secure the Web Service with Bearer Token Authentication
Secure the APIs using `Flask-HTTPAuth` with two Bearer tokens: 
- one for accessing `get_params` and `generate_lissajous`, 
- the other for `set_params`.

First, install `Flask-HTTPAuth` if you haven't already:
```bash
pip install Flask-HTTPAuth
```

### Step 3.1: Update the [code in Task 2](./code/t2.py) with token-based authentications.
1. **Import HTTPTokenAuth**:
  ```python
  from flask_httpauth import HTTPTokenAuth
  ```

2. **Two HTTPTokenAuth Instances**: `auth_get_generate` for `get_params` and `generate_lissajous`, and `auth_set` for `set_params`.
  ```python
  # Create two separate token authenticators
  auth_get_generate = HTTPTokenAuth(scheme="Bearer")
  auth_set = HTTPTokenAuth(scheme="Bearer")

  # Tokens for the two groups
  TOKENS = {
      "get_generate_token": "token123",  # Access for get_params and generate_lissajous
      "set_token": "token456"            # Access for set_params
  }
  ```

3. **Token Verification Functions**:
   - `verify_get_generate_token`: Checks if the provided token matches the `get_generate_token` for accessing `get_params` and `generate_lissajous`.
   - `verify_set_token`: Checks if the provided token matches the `set_token` for accessing `set_params`.
   ```python
    # Define authentication verification functions
    @auth_get_generate.verify_token
    def verify_get_generate_token(token):
        return token == TOKENS["get_generate_token"]

    @auth_set.verify_token
    def verify_set_token(token):
        return token == TOKENS["set_token"]  
   ```

4. **Protecting the Endpoints**:
   - `@auth_get_generate.login_required` is applied to `get_params` and `generate_lissajous`.
   - `@auth_set.login_required` is applied to `set_params`.
   ```python
    # API 1: Retrieve Frequency, Phase, Curve Color, and Background Color Parameters
    @app.route('/get_params', methods=['GET'])
    @auth_get_generate.login_required
    def get_params():
      # same as Task 2

    # API 2: Update Frequency, Phase, Curve Color, and Background Color Parameters
    @app.route('/set_params', methods=['POST'])
    @auth_set.login_required
    def set_params():
      # same as Task 2
 
    # API 3: Generate Lissajous Curve as a GIF
    @app.route('/generate_lissajous', methods=['GET'])
    @auth_get_generate.login_required
    def generate_lissajous():  
      # same as Task 2  
   ```


### Step 3.2:  Testing the APIs with Bearer Tokens

Test each of the three protected APIs using both `cURL` and `Python Requests` with the appropriate Bearer tokens.

### 1. Testing `/get_params` API

#### Using cURL
```bash
curl -X GET http://127.0.0.1:5000/get_params -H "Authorization: Bearer token123"
# What do you get without token?
curl -X GET http://127.0.0.1:5000/get_params
```

#### Using Python Requests
```python
import requests

url = "http://127.0.0.1:5000/get_params"
headers = {
    "Authorization": "Bearer token123"
}
response = requests.get(url, headers=headers)

if response.status_code == 200:
    print("Parameters:", response.json())
else:
    print("Failed to retrieve parameters:", response.status_code)

# What do you get without token?
response = requests.get(url)
print(response)
```

### 2. Testing `/set_params` API

#### Using cURL
```bash
curl -X POST http://127.0.0.1:5000/set_params \
     -H "Authorization: Bearer token456" \
     -H "Content-Type: application/json" \
     -d '{"freq": 2.0, "phase": 1.5, "curve_color": [0, 200, 0], "background_color": [20, 1, 1]}'

# What do you get without token?
curl -X POST http://127.0.0.1:5000/set_params \
     -H "Content-Type: application/json" \
     -d '{"freq": 2.0, "phase": 1.5, "curve_color": [0, 200, 0], "background_color": [20, 1, 1]}'
```

#### Using Python Requests
```python
import requests

url = "http://127.0.0.1:5000/set_params"
headers = {
    "Authorization": "Bearer token456",
    "Content-Type": "application/json"
}
data = {
    "freq": 2.0,
    "phase": 1.5,
    "curve_color": [0, 200, 0],
    "background_color": [20, 1, 1]
}
response = requests.post(url, headers=headers, json=data)

if response.status_code == 200:
    print("Update successful:", response.json())
else:
    print("Failed to update parameters:", response.status_code)

# What do you get without token?
response = requests.post(url, headers={"Content-Type": "application/json",}, json=data)
print(response)  
```

### 3. Testing `/generate_lissajous` API

#### Using cURL
```bash
curl -X GET http://127.0.0.1:5000/generate_lissajous -H "Authorization: Bearer token123"| sed 's/^data:image\/gif;base64,//' | base64 --decode > output3.gif

# What do you get without token?
curl -X GET http://127.0.0.1:5000/generate_lissajous
```

#### Using Python Requests
```python
import requests
import base64
from PIL import Image
from io import BytesIO

url = "http://127.0.0.1:5000/generate_lissajous"
headers = {
    "Authorization": "Bearer token123"
}
response = requests.get(url, headers=headers)

# Extract the Base64 string, decode it, and save the image as a GIF
if response.status_code == 200:
    # Remove the data prefix and decode the Base64 string
    image_data = response.text.split(",")[1]
    gif_data = base64.b64decode(image_data)
    
    # Open the GIF data in memory as an image
    image = Image.open(BytesIO(gif_data))
    
    # Save the entire GIF animation properly
    image.save("lissajous3.gif", format="GIF", save_all=True)
    print("Animated GIF saved as 'lissajous3.gif'.")
    
    # To view it, open the GIF with the system's default viewer
    import webbrowser
    webbrowser.open("lissajous3.gif")
else:
    print("Failed to generate image:", response.status_code)

# What do you get without token?
response = requests.get(url) 
print(response)    
```

---

# Summary
This lab provides hands-on experience with RESTful APIs, creating web services, and implementing token-based authentication. 