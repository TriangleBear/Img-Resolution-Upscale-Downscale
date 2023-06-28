from flask import Flask, render_template, request
from PIL import Image

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload():
    # Get the uploaded file from the request
    file = request.files['file']

    # Load the image and display it in the label
    image = Image.open(file)
    image.save('static/image.jpg')

    return render_template('index.html')

@app.route('/downscale', methods=['POST'])
def downscale():
    # Get the current size of the image
    image = Image.open('static/image.jpg')
    width, height = image.size

    # Calculate the new size based on the user's choice
    scale_factor = float(request.form['scale'])
    new_width = int(width * scale_factor)
    new_height = int(height * scale_factor)

    # Downscale the image using bicubic interpolation
    resized_image = image.resize((new_width, new_height), resample=Image.BICUBIC)
    resized_image.save('static/image.jpg')

    return render_template('index.html')

@app.route('/upscale', methods=['POST'])
def upscale():
    # Get the current size of the image
    image = Image.open('static/image.jpg')
    width, height = image.size

    # Calculate the new size based on the user's choice
    scale_factor = float(request.form['scale'])
    new_width = int(width * scale_factor)
    new_height = int(height * scale_factor)

    # Upscale the image using bicubic interpolation
    resized_image = image.resize((new_width, new_height), resample=Image.BICUBIC)
    resized_image.save('static/image.jpg')

    return render_template('index.html')

@app.route('/save', methods=['POST'])
def save():
    # Save the modified image to the selected file with the appropriate file extension
    image = Image.open('static/image.jpg')
    file_extension = 'jpg'  # Default to JPEG if the file extension is not recognized
    image.save('static/image.' + file_extension, file_extension.upper())

    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)
