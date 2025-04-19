import os
import settings
import cv2
import base64

def save_upload_image(file_obj):
    filename = file_obj.filename
    filepath = os.path.join(settings.MEDIA_DIR, filename)
    file_obj.save(filepath)
    return filepath

def image_to_base64(image):
    _, buffer = cv2.imencode('.jpg', image)
    return base64.b64encode(buffer).decode("utf-8")