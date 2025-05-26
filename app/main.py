from flask import Flask, request, jsonify
from PIL import Image, UnidentifiedImageError
from datetime import datetime
import json
import base64
import torch
import io
import os
from consumerOpenAI import response_openai

app = Flask(__name__)


# Cargar modelo
BASE_DIR = os.path.dirname(__file__)
path_yolov5 = os.path.join(BASE_DIR, 'yolov5')
path_weights = os.path.join(BASE_DIR,'weights', 'best.pt')

model = torch.hub.load(path_yolov5, 'custom', path = path_weights, source='local')
model.conf = 0.60  # Umbral de confianza

@app.route('/predict', methods=['POST'])
def predict():
    try:
        if 'image' not in request.files:
            return jsonify({'error': 'No image provided'}), 400

        file = request.files['image']
        if file.filename == '':
            return jsonify({'error': 'Empty filename'}), 400

        image_bytes = file.read()

        try:
            image = Image.open(io.BytesIO(image_bytes))
        except UnidentifiedImageError:
            return jsonify({'error': 'Invalid image format'}), 400

        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        output_dir = os.path.join(BASE_DIR,'output', f'detect_{timestamp}')
        
        results = model(image)
        results.save(save_dir=output_dir)

        detections = results.pandas().xyxy[0].to_dict(orient="records")
        
        result = response_openai(file_path = os.path.join(output_dir, "image0.jpg"))
        response_body = json.loads(result)
        return jsonify({'secuence': response_body})

    except Exception as err:
        print("Error:", err)
        return jsonify({'error': str(err)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)