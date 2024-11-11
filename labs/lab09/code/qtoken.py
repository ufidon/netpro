from flask import Flask, request, jsonify
import math
import base64
from io import BytesIO
from PIL import Image, ImageDraw

app = Flask(__name__)

# Tokens for the two groups
TOKENS = {
    "get_generate_token": "token123",  # Access for get_params and generate_lissajous
    "set_token": "token456"            # Access for set_params
}

# Initial Lissajous parameters
params = {
    'freq': 1.0,
    'phase': 0.0,
    'curve_color': (0, 0, 0),  # Black curve
    'background_color': (255, 255, 255)  # White background
}

# Utility function to verify tokens for each API route
def verify_token(required_token):
    token = request.args.get("token")
    if token == required_token:
        return True
    return False

# API 1: Retrieve Frequency, Phase, Curve Color, and Background Color Parameters
@app.route('/get_params', methods=['GET'])
def get_params():
    if not verify_token(TOKENS["get_generate_token"]):
        return jsonify({"error": "Unauthorized"}), 401
    return jsonify(params), 200

# API 2: Update Frequency, Phase, Curve Color, and Background Color Parameters
@app.route('/set_params', methods=['POST'])
def set_params():
    if not verify_token(TOKENS["set_token"]):
        return jsonify({"error": "Unauthorized"}), 401

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
    if not verify_token(TOKENS["get_generate_token"]):
        return jsonify({"error": "Unauthorized"}), 401

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
