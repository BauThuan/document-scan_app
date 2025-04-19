from flask import Flask, request, jsonify # type: ignore
from flask_cors import CORS # type: ignore
import utils
import predictions
import cv2

app = Flask(__name__)
CORS(app)

@app.route('/api/v1/public/upload-transform', methods=['POST'])
def upload_and_transform():
    if 'image_name' not in request.files:
        return jsonify({"error": "No file uploaded"}), 400
    
    file = request.files['image_name']

    upload_image_path = utils.save_upload_image(file)

    try:
        image = cv2.imread(upload_image_path)
        image_original = utils.image_to_base64(image)
        if image is None:
            return jsonify({"error": "Invalid image path or cannot read image"}), 400

        img_results, result = predictions.getPredictions(image)

        image_base64 = utils.image_to_base64(img_results)
        
        response_data = {
            "result": result,
            "boxedImage": image_base64,
            "originalImage": image_original,
        }

        response_data["result"] = {k: v for k, v in response_data["result"].items() if k.strip()}

        return jsonify(response_data)

    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    print("Flask app is starting... __name__ =", __name__)
    app.run(debug=True)
