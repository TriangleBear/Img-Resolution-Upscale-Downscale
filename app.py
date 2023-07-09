from flask import Flask, render_template, request, redirect, url_for,session, jsonify
import pyrebase
from requests.exceptions import HTTPError
import re
from key import firebaseConfig, secret_key
import cv2
import base64
import numpy as np
import edsr_main

firebase = pyrebase.initialize_app(firebaseConfig)
auth = firebase.auth()

app = Flask(__name__)
app.secret_key= secret_key

def check_user_logged_in():
    if 'user_id' in session:
        return True
    else:
        return False

@app.route('/upscale', methods=['POST'])
def upscale_image():
    # Get the base64-encoded image data from the request
    image_data = request.json['image_data']
    
    # Convert the base64-encoded image data to a numpy array
    image_bytes = np.frombuffer(base64.b64decode(image_data), dtype=np.uint8)
    image_object = cv2.imdecode(image_bytes, cv2.IMREAD_COLOR)
    
    # Upscale the image using the EDSR algorithm
    upscaled_image_object = edsr_main.run(image_object)
    
    # Convert the upscaled image to base64-encoded image data
    _, buffer = cv2.imencode('.jpg', upscaled_image_object)
    upscaled_image_bytes = base64.b64encode(buffer).decode('utf-8')
    
    # Return the upscaled image as a response
    response = {'upscaled_image_data': upscaled_image_bytes}
    return jsonify(response)

@app.route('/')
def home():
    user_logged_in = check_user_logged_in()

    return render_template('home_screen.html', user_logged_in=user_logged_in)


@app.route('/go_premium')
def go_premium():
    user_logged_in = check_user_logged_in() 

    return render_template('go_premium.html', user_logged_in=user_logged_in)


@app.route('/login_screen', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        try:
            login = auth.sign_in_with_email_and_password(email, password)
            session['user_id'] = login['idToken']
            return redirect(url_for('home'))
        except:
            error_message= 'Incorrect email or password.'
            return render_template('login_screen.html', error_message=error_message)

    return render_template('login_screen.html')

@app.route('/register_screen', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        username = request.form.get('username')
        first_name = request.form.get('first_name')
        last_name = request.form.get('last_name')
        
        if not username or not first_name or not last_name:
            error_message = 'Please fill in all the required fields.'
            return render_template('register_screen.html', error_message=error_message)

        if len(password) <6:
            error_message = 'Password should be at least 6 characters.'
            return render_template ('register_screen.html', error_message=error_message)
        

        email_pattern = r'^[\w\.-]+@[\w\.-]+\.\w+$'
        
        if not re.match(email_pattern, email):
            error_message = 'Invalid email format.'
            return render_template('register_screen.html', error_message=error_message)

        # Regular expression pattern for password conditions
        password_pattern = r"^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*?&])[A-Za-z\d@$!%*?&]{6,}$"
        
        if not re.match(password_pattern, password):
            error_message = 'Password should contain at least 1 uppercase letter, 1 lowercase letter, 1 special character, and 1 number.'
            return render_template('register_screen.html', error_message=error_message)

        try:
            user = auth.create_user_with_email_and_password(email, password)
            return render_template('login_screen.html')
        except HTTPError as e:
            if e.response is not None and e.response.content:
                error_message = e.response.json()['error']['message']
            else:
                error_message = 'An error occurred during registration.'
            return render_template('register_screen.html', error_message=error_message)

    return render_template('register_screen.html')


@app.route('/reset_password', methods=['POST'])
def reset_password():
    email = request.form.get('email')
    
    try:
        auth.send_password_reset_email(email)
        return render_template('forgot_password.html', reset_success=True)
    except:
        error_message = "Failed to send password reset email. Please try again."
        return render_template('forgot_password.html', error_message=error_message)

@app.route('/forgotpass', methods=['GET', 'POST'])
def forgotpass():
    if request.method == 'POST':
        email = request.form.get('email')
        
        try:
            auth.send_password_reset_email(email)
            return render_template('forgot_password.html', reset_success=True)
        except:
            error_message = "Failed to send password reset email. Please try again."
            return render_template('forgot_password.html', error_message=error_message)
    
    return render_template('forgot_password.html')


@app.route('/logout')
def logout():
    session.pop('user_id', None)
    return redirect(url_for('home'))


if __name__ == '__main__':
    app.run()