from flask import Flask, jsonify, request, json, render_template
import tensorflow as tf
from tensorflow.keras.models import load_model
from PIL import Image, ImageOps
import random
import numpy as np
import io

app = Flask(__name__)

# Load the model
model = load_model('./trained_model.h5')

@app.route('/')
def index():
    return render_template('index.html')

# GET endpoint
@app.route('/api/examples', methods=['GET'])
def get_prediction():
    data = {
        'examples': [generate_math_equation() for i in range(5)]
    }
    return jsonify(data)

def generate_math_equation():
    a = random.randint(0, 99)
    b = random.randint(0, 99)
    operator = random.choice(['+', '-', '*'])
    
    if operator == '+':
        c = a + b
    elif operator == '-':
        c = a - b
    else:
        c = a * b
    
    equation = {
        'a' : a,
        'b' : b,
        'operator' : operator
    }
    return equation if (c >= 0 and c <= 99) else generate_math_equation()

# POST endpoint
@app.route('/api/answer', methods=['POST'])
def post_prediction():
    # Get the image file from the request
    image_file = request.files['image']
    input_eq = json.loads(request.form['data'])

    # Read the image file using PIL
    image = Image.open(image_file)
    print(image.mode)

    _, _, _, alpha_channel = image.split()

    resized = alpha_channel.resize((56, 28))

    imx = np.array(resized)

    imx = imx / 255.0

    imx = np.reshape(imx, (1, 28, 56, 1))

    # Convert the image to a numpy array
    input_data = tf.convert_to_tensor(imx)

    # Perform predictions using the loaded model
    prediction = int(np.argmax(model.predict(input_data)))
    print(prediction)

    res = eval(f"{input_eq['a']}{input_eq['operator']}{input_eq['b']}")

    data = {
        'isCorrect' : res == prediction,
        'prediction' : prediction
    }
    
    return jsonify(data)

if __name__ == '__main__':
    app.run(debug=True)
