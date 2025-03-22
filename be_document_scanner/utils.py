import os
import settings
# import cv2

# def save_upload_image(fileObj):
#     filename = fileObj.filename
    
#     name, ext = filename.split('.')
    
#     save_filename = 'upload.'+ext
#     upload_image_path = settings.join_path(settings.SAVE_DIR, save_filename)
#     fileObj.save(upload_image_path)
    
#     return upload_image_path

def save_upload_image(file_obj):
    filename = file_obj.filename
    filepath = os.path.join(settings.MEDIA_DIR, filename)
    file_obj.save(filepath)
    return filepath