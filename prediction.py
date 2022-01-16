from flask import Flask
import os
from flask import Flask, flash, request, redirect, url_for
from werkzeug.utils import secure_filename
import tensorflow as tf
from tensorflow.keras.applications.mobilenet_v2 import preprocess_input, decode_predictions
from tensorflow.keras.preprocessing import image
import numpy as np

UPLOAD_FOLDER = '/app/uploads'
ALLOWED_EXTENSIONS = set(['txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'])

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.secret_key = "super secret key"

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/predict', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        # check if the post request has the file part
        if 'file' not in request.files:
            flash('No file part')
            return redirect(request.url)
        file = request.files['file']
        # If the user does not select a file, the browser submits an
        # empty file without a filename.
        if file.filename == '':
            flash('No selected file')
            return redirect(request.url)
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)

            imagePath = os.path.join(app.config['UPLOAD_FOLDER'], filename)

            # Save the image to the disk
            file.save(imagePath)

            # Get the predictions
            predictions = predict(imagePath)

            # Remove the image from the disk
            os.remove(imagePath)

            # Return the predictions
            return predictions

    return request.method


def predict(IMG_PATH):
    img = image.load_img(IMG_PATH, target_size=(224, 224))

    img_array = image.img_to_array(img)
    img_batch = np.expand_dims(img_array, axis=0)
    img_preprocessed = tf.keras.applications.mobilenet_v2.preprocess_input(img_batch)

    model = tf.keras.applications.mobilenet_v2.MobileNetV2()
    labels = model.predict(img_preprocessed)

    predictions = decode_predictions(labels)

    predictions = predictions[0][0]

    pred = predictions[1]
    percentage = '%.2f%%' % (predictions[2]*100)

    return pred, percentage

# So that the flask app starts when the python script is started in cli
if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0')