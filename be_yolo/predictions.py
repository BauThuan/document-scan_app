import cv2
import numpy as np
import yaml
from yaml.loader import SafeLoader
from PIL import Image
from vietocr.tool.predictor import Predictor # type: ignore
from vietocr.tool.config import Cfg # type: ignore

class YOLO_Pred_VietOCR():
    def __init__(self, yolo_onnx_model, data_yaml_path, device='cpu'):
        # Load YOLO config
        with open(data_yaml_path, mode='r') as f:
            data_yaml = yaml.load(f, Loader=SafeLoader)
        self.labels = data_yaml['names']
        self.nc = data_yaml['nc']

        # Load YOLO ONNX model
        self.yolo = cv2.dnn.readNetFromONNX(yolo_onnx_model)
        self.yolo.setPreferableBackend(cv2.dnn.DNN_BACKEND_OPENCV)
        self.yolo.setPreferableTarget(cv2.dnn.DNN_TARGET_CPU)

        # Load VietOCR
        config = Cfg.load_config_from_name('vgg_transformer')
        config['cnn']['pretrained'] = False
        config['device'] = device
        self.ocr = Predictor(config)

    def generate_colors(self, ID):
        np.random.seed(10)
        colors = np.random.randint(100, 255, size=(self.nc, 3)).tolist()
        return tuple(colors[ID])

    def predictions(self, image):
        orig = image.copy()
        row, col, _ = image.shape
        max_rc = max(row, col)
        input_image = np.zeros((max_rc, max_rc, 3), dtype=np.uint8)
        input_image[0:row, 0:col] = image

        INPUT_WH_YOLO = 640
        blob = cv2.dnn.blobFromImage(input_image, 1 / 255, (INPUT_WH_YOLO, INPUT_WH_YOLO), swapRB=True, crop=False)
        self.yolo.setInput(blob)
        preds = self.yolo.forward()[0]

        x_factor = input_image.shape[1] / INPUT_WH_YOLO
        y_factor = input_image.shape[0] / INPUT_WH_YOLO

        boxes, confidences, class_ids = [], [], []

        for row in preds:
            confidence = row[4]
            if confidence > 0.4:
                class_score = row[5:].max()
                class_id = row[5:].argmax()
                if class_score > 0.25:
                    cx, cy, w, h = row[0:4]
                    x = int((cx - 0.5 * w) * x_factor)
                    y = int((cy - 0.5 * h) * y_factor)
                    width = int(w * x_factor)
                    height = int(h * y_factor)
                    boxes.append([x, y, width, height])
                    confidences.append(float(confidence))
                    class_ids.append(class_id)

        indices = cv2.dnn.NMSBoxes(boxes, confidences, 0.25, 0.45).flatten()
        results = []
        img_with_boxes = orig.copy()

        for i in indices:
            x, y, w, h = boxes[i]
            class_id = class_ids[i]
            class_name = self.labels[class_id]
            crop_img = orig[y:y + h, x:x + w]
            if crop_img.size == 0:
                continue

            pil_img = Image.fromarray(cv2.cvtColor(crop_img, cv2.COLOR_BGR2RGB))
            try:
                ocr_text = self.ocr.predict(pil_img)
            except:
                ocr_text = ""

            results.append({
                'label': class_name,
                'bbox': [x, y, w, h],
                'text': ocr_text,
                'confidence': confidences[i]
            })

            # Vẽ bounding box với confidence
            bb_conf = int(confidences[i] * 100)
            color = self.generate_colors(class_id)
            text = f'{class_name}: {bb_conf}%'
            cv2.rectangle(img_with_boxes, (x, y), (x + w, y + h), color, 2)
            cv2.rectangle(img_with_boxes, (x, y - 25), (x + w, y), color, -1)
            cv2.putText(img_with_boxes, text, (x + 5, y - 7), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 0), 1)

        return results, orig, img_with_boxes

