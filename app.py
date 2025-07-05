from flask import Flask, request, render_template
import tensorflow as tf
import numpy as np
import pickle
from tensorflow.keras.preprocessing.sequence import pad_sequences

# Initialize Flask app
app = Flask(__name__, template_folder="templates")

# Load model and tokenizer
from keras.initializers import Orthogonal

custom_objects = {"Orthogonal": Orthogonal}

model = tf.keras.models.load_model("lstm_emotion_model.h5", custom_objects=custom_objects)

with open("tokenizer.pkl", "rb") as f:
    tokenizer = pickle.load(f)

with open("label_encoder.pkl", "rb") as f:
    label_encoder = pickle.load(f)

# Route to render the homepage (index.html)
@app.route('/')
def home():
    return render_template('index.html')

# API endpoint to predict emotion and show result on a new page
@app.route('/predict_emotion', methods=['POST'])
def predict_emotion():
    text = request.form.get("text")

    if not text:
        return render_template("index.html", error="Please provide text input")

    # Preprocess input
    sequence = tokenizer.texts_to_sequences([text])
    padded_sequence = pad_sequences(sequence, maxlen=50, padding="post", truncating="post")


    # Predict emotion
    prediction = model.predict(padded_sequence)
    predicted_label = label_encoder.inverse_transform([np.argmax(prediction)])[0]
    print(predicted_label)  # Debugging output


    # Render result.html with the prediction
    return render_template("result.html", text=text, predicted_emotion=predicted_label)

if __name__ == '__main__':
    app.run(debug=True)
