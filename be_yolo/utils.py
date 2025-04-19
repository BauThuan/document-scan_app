import os
import settings
import cv2
import base64
from collections import defaultdict

def save_upload_image(file_obj):
    filename = file_obj.filename
    filepath = os.path.join(settings.MEDIA_DIR, filename)
    file_obj.save(filepath)
    return filepath

def image_to_base64(image):
    _, buffer = cv2.imencode('.jpg', image)
    return base64.b64encode(buffer).decode("utf-8")

def group_results_by_label(results):
    grouped = defaultdict(list)

    for item in results:
        label = item['label']
        grouped[label].append({
            'bbox': item['bbox'],
            'text': item['text'],
            'confidence': item['confidence']
        })

    return dict(grouped)

def simplify_results(results):
    grouped = defaultdict(list)

    for item in results:
        label = item['label']
        text = item['text'].strip()
        if text:
            grouped[label].append(text)

    simplified = {k: ', '.join(v) for k, v in grouped.items()}
    return simplified