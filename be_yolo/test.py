from flask import Flask, request, jsonify
from predictionsVietOcr import YOLO_Pred_VietOCR
import cv2
import numpy as np
import io
from PIL import Image
import base64
import matplotlib.pyplot as plt
import warnings

# Disable warnings
warnings.filterwarnings("ignore", category=UserWarning, module='torch.nn.modules.transformer')

# Create Flask app
app = Flask(__name__)

# Initialize YOLO and VietOCR model
yolo = YOLO_Pred_VietOCR('./Model/weights/best.onnx', 'data.yaml')

# Function to convert OpenCV image to base64
def encode_image_to_base64(img):
    _, buffer = cv2.imencode('.jpg', img)
    return base64.b64encode(buffer).decode('utf-8')

@app.route('/predict', methods=['POST'])
def predict():
    # Get the image file from the POST request
    img_file = request.files.get('image')
    if img_file is None:
        return jsonify({"error": "No image file provided"}), 400
    
    # Read image from the file
    img = np.array(Image.open(img_file))
    
    # Get predictions from the YOLO + VietOCR model
    results, orig_img, img_with_boxes = yolo.predictions(img)
    
    # Prepare results to send back as JSON
    results_data = []
    for item in results:
        results_data.append({
            "label": item["label"],
            "bbox": item["bbox"],
            "confidence": item["confidence"],
            "text": item["text"]
        })

    # Convert the image with bounding boxes to base64 to send in the response
    img_with_boxes_base64 = encode_image_to_base64(img_with_boxes)

    return jsonify({
        "results": results_data,
        "image_with_boxes": img_with_boxes_base64
    })

# Run the Flask app
if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
