# Play
.\yolo_venv\Scripts\activate
jupyter notebook

# Train
pip freeze > requirements_app.txt

python -m venv docapp 
.\docapp\Scripts\activate
# Training model
!python train.py --data data.yaml --weights runs/train/exp3/weights/best.pt --epochs 150 --batch-size 16
# Export model to onnx
!python export.py --weights runs/train/exp3/weights/best.pt --include onnx --simplify --opset 12