from flask import Flask, request, render_template_string, redirect, url_for, flash
from flask_httpauth import HTTPBasicAuth, HTTPDigestAuth
import math
import base64
from io import BytesIO
from PIL import Image, ImageDraw

app = Flask(__name__)
# Generate a secure random key:
# import secrets; print(secrets.token_urlsafe())
app.secret_key = 'your_secret_key'  # Change this to a secure random key

# Initialize Flask-HTTPAuth instances
basic_auth = HTTPBasicAuth()
digest_auth = HTTPDigestAuth()

# User credentials for Basic and Digest Auth
users = {
    "shape": "shapepass",   # Basic Auth user
    "color": "colorpass"      # Digest Auth user
}

# Initial Lissajous parameters
params = {
    'freq': 1.0,
    'phase': 0.0,
    'curve_color': (0, 0, 0),  # Black curve
    'background_color': (255, 255, 255)  # White background
}

# Template for the home page with toggle and submit buttons, flash message area
HOME_PAGE = """
<!doctype html>
<html lang="en">
<head>
    <title>Lissajous GIF Generator</title>
    <style>
        .button { padding: 10px; font-size: 14px; color: white; cursor: pointer; }
        .gray { background-color: gray; }
        .green { background-color: green; }
        .disabled { pointer-events: none; opacity: 0.5; }
    </style>
</head>
<body>
    <h2>Lissajous GIF</h2>
    <img src="{{ gif_data }}" alt="Lissajous GIF"/>

    <!-- Flash messages area -->
    {% with messages = get_flashed_messages() %}
      {% if messages %}
        <div class="flash-messages">
          {% for message in messages %}
            <p>{{ message }}</p>
          {% endfor %}
        </div>
      {% endif %}
    {% endwith %}

    <h3>Update Frequency and Phase (Basic Auth Required)</h3>
    <form id="basic-form" method="POST" action="{{ url_for('update_basic') }}">
        <label for="freq">Frequency:</label>
        <input type="text" id="freq" name="freq" value="{{ freq }}" disabled><br>
        <label for="phase">Phase:</label>
        <input type="text" id="phase" name="phase" value="{{ phase }}" disabled><br>
        <button type="button" id="toggle-basic" class="button gray" onclick="toggleEdit('basic')">Enable Edit</button>
        <button type="submit" id="submit-basic" class="button gray disabled">Submit</button>
    </form>

    <h3>Update Curve and Background Colors (Digest Auth Required)</h3>
    <form id="digest-form" method="POST" action="{{ url_for('update_digest') }}">
        <label for="curve_color">Curve Color (e.g., 0,0,0 for black):</label>
        <input type="text" id="curve_color" name="curve_color" value="{{ curve_color }}" disabled><br>
        <label for="background_color">Background Color (e.g., 255,255,255 for white):</label>
        <input type="text" id="background_color" name="background_color" value="{{ background_color }}" disabled><br>
        <button type="button" id="toggle-digest" class="button gray" onclick="toggleEdit('digest')">Enable Edit</button>
        <button type="submit" id="submit-digest" class="button gray disabled">Submit</button>
    </form>

    <script>
        // Function to enable/disable editing fields after authentication
        function toggleEdit(authType) {
            let formId = authType === 'basic' ? 'basic-form' : 'digest-form';
            let toggleButton = document.getElementById(`toggle-${authType}`);
            let submitButton = document.getElementById(`submit-${authType}`);
            
            fetch(`/${authType}_login`)
                .then(response => {
                    if (response.ok) {
                        // Enable form fields and change button styles upon authentication success
                        document.querySelectorAll(`#${formId} input`).forEach(input => input.disabled = false);
                        toggleButton.classList.remove('gray');
                        toggleButton.classList.add('green');
                        toggleButton.textContent = "Edit Enabled";
                        submitButton.classList.remove('disabled');
                        submitButton.classList.add('green');
                    } else {
                        alert("Authentication required!");
                    }
                });
        }
    </script>
</body>
</html>
"""

# Generate Lissajous curve

# Basic Auth Verification


# Digest Auth Verification


# Home page
@app.route('/', methods=['GET'])
def home():
    gif_data = 'Lissajous GIF data'.encode('ascii')
    return render_template_string(HOME_PAGE, gif_data=gif_data, **params)

# Route for updating Frequency and Phase (Basic Auth Required)
@app.route('/update_basic', methods=['GET','POST'])
def update_basic():
    if request.method == 'POST':
        return "<p>Update Frequency and Phase !</p>" 
    else:
        return "<p>Route for updating Frequency and Phase (Basic Auth Required)!</p>"  
 
# Route for updating Curve and Background Colors (Digest Auth Required)
@app.route('/update_digest', methods=['GET', 'POST'])
def update_digest():
    if request.method == 'POST':
        return "<p>Update Curve and Background Colors!</p>" 
    else:
        return "<p>Route for updating Curve and Background Colors (Digest Auth Required)!</p>"  
  

# Login route for Basic Auth to trigger the login pop-up
@app.route('/basic_login')
def basic_login():
  return "<p>Login route for Basic Auth to trigger the login pop-up!</p>"

# Login route for Digest Auth to trigger the login pop-up
@app.route('/digest_login')
def digest_login():
  return "<p>Login route for Digest Auth to trigger the login pop-up!</p>"

if __name__ == "__main__":
    app.run(port=5000, debug=True)