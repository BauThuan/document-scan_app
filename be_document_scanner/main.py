from flask import Flask, request, jsonify
from flask_cors import CORS
import utils

app = Flask(__name__)
CORS(app)

@app.route('/api/v1/public/test')
def index():
    return {'message': 'Hello world'}

@app.route('/api/v1/public/upload-image', methods=['POST'])
def upload_image():
    if 'image_name' not in request.files:
        return jsonify({"error": "No file uploaded"}), 400
    file = request.files['image_name']
    upload_image_path = utils.save_upload_image(file)
    return jsonify({"message": "Upload successful", "image_path": upload_image_path})



if __name__ == '__main__':
    print("Flask app is starting... __name__ =", __name__)
    app.run(debug=True)
