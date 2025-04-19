from flask import Flask, request, jsonify # type: ignore
from flask_cors import CORS # type: ignore
import utils
from predictions import YOLO_Pred_VietOCR
import cv2

app = Flask(__name__)
yolo = YOLO_Pred_VietOCR('./model/best.onnx', 'data.yaml')
CORS(app)

@app.route('/api/v1/public/upload-transform', methods=['POST'])
def upload_and_transform():
    if 'image_name' not in request.files:
        return jsonify({"error": "No file uploaded"}), 400
    
    file = request.files['image_name']

    upload_image_path = utils.save_upload_image(file)

    try:
        image = cv2.imread(upload_image_path)
        if image is None:
            return jsonify({"error": "Invalid image path or cannot read image"}), 400

        results, orig, image_with_boxes = yolo.predictions(image)
        
        image_original = utils.image_to_base64(orig)
        image_base64 = utils.image_to_base64(image_with_boxes)
                
        response_data = {
            "result": utils.simplify_results(results),
            "boxedImage": image_base64,
            "originalImage": image_original,
        }
        return jsonify(response_data)

    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    print("Flask app is starting... __name__ =", __name__)
    app.run(debug=True)
