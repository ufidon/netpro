import requests
import base64
from time import time
from PIL import Image
from io import BytesIO

"""
① Access with cURL
1. Get Parameters
curl "http://127.0.0.1:5000/get_params?token=token123"
2. Set Parameters
curl -X POST "http://127.0.0.1:5000/set_params?token=token456" \
     -H "Content-Type: application/json" \
     -d '{"freq": 2.0, "phase": 0.5, "curve_color": [0, 255, 0], "background_color": [255, 255, 255]}'
3. Generate Lissajous Curve
curl "http://127.0.0.1:5000/generate_lissajous?token=token123"
② Access with Requests
"""

### 1. **Get Parameters**
url = "http://127.0.0.1:5000/get_params"
token = "token123"

response = requests.get(url, params={"token": token})

if response.status_code == 200:
    print("Parameters:", response.json())
else:
    print("Failed to retrieve parameters:", response.status_code)


### 2. **Set Parameters**
url = "http://127.0.0.1:5000/set_params"
token = "token456"
data = {
    "freq": 2.7,
    "phase": 1.3,
    "curve_color": [0, 200, 0],  # Green curve
    "background_color": [10, 1, 10]  # White background
}

response = requests.post(url, json=data, params={"token": token})

if response.status_code == 200:
    print("Parameters updated successfully:", response.json())
else:
    print("Failed to update parameters:", response.status_code, response.json())

### 3. **Generate Lissajous Curve**
url = "http://127.0.0.1:5000/generate_lissajous"
token = "token123"

response = requests.get(url, params={"token": token})

# Extract the Base64 string, decode it, and save the image as a GIF
if response.status_code == 200:
    # Remove the data prefix and decode the Base64 string
    image_data = response.text.split(",")[1]
    gif_data = base64.b64decode(image_data)
    
    # Open the GIF data in memory as an image
    image = Image.open(BytesIO(gif_data))
    
    # Save the entire GIF animation properly
    gifname = str(int(time())) + '.gif'
    image.save(gifname, format="GIF", save_all=True)
    print(f"Animated GIF saved as {gifname}.")
    
    # To view it, open the GIF with the system's default viewer
    import webbrowser
    webbrowser.open(gifname)
else:
    print("Failed to generate image:", response.status_code)