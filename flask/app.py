import os
import base64
import cv2

from flask import Flask, send_from_directory, jsonify, request
from flask_cors import CORS  # Import CORS

from brain_tumor_detection.pipeline.predict_pipeline import PredictPipeline  # Adjust the import based on your model's structure
import medical_instance_segmentation.pipeline.predict_pipeline as medicalInstanceSegmentation

app = Flask(__name__, static_folder="../yolov8_react/build", template_folder="../yolov8_react/build")
CORS(app)  # Enable CORS for all routes

brain_tumor_detection = PredictPipeline()  # Assuming `Predictor` is the class that loads and uses the model
segmentation_predict = medicalInstanceSegmentation.PredictPipeline()  # Assuming `Predictor` is the class that loads and uses the model

# API routes
@app.route('/api/segmentation', methods=['POST'], strict_slashes=False)
def segment():
    if 'image' not in request.files:
        return jsonify({'error': 'No image file provided'}), 400

    try:
        file = request.files['image']
        file_path = os.path.join('flask/uploads', file.filename)
        file.save(file_path)

        result, processed_image  = segmentation_predict.predict(file_path)
        
        # Convert processed image to Base64
        _, buffer = cv2.imencode('.jpg', processed_image)  # Adjust the image format as needed
        image_base64 = base64.b64encode(buffer).decode('utf-8')
        
        return jsonify({'result': result, 'image': image_base64}), 200
    except Exception as e:
        print(f"Error: {str(e)}")
        return jsonify({'error': 'Error during prediction'}), 500
    
@app.route('/api/detection', methods=['POST'], strict_slashes=False)
def detect():
    if 'image' not in request.files:
        return jsonify({'error': 'No image file provided'}), 400
    
    try:
        file = request.files['image']
        file_path = os.path.join('flask/uploads', file.filename)
        file.save(file_path)

        result, processed_image  = brain_tumor_detection.predict(file_path)
        
        # Convert processed image to Base64
        _, buffer = cv2.imencode('.jpg', processed_image)  # Adjust the image format as needed
        image_base64 = base64.b64encode(buffer).decode('utf-8')
        
        return jsonify({'result': result, 'image': image_base64}), 200
    except Exception as e:
        print(f"Error: {str(e)}")
        return jsonify({'error': 'Error during prediction'}), 500

# Serve the React app
@app.route('/', defaults={'path': ''})
@app.route('/<path:path>')
def serve_react(path):
    if path != "" and os.path.exists(app.static_folder + '/' + path):
        return send_from_directory(app.static_folder, path)
    else:
        return send_from_directory(app.static_folder, 'index.html')

@app.route('/api/test_post', methods=['POST'], strict_slashes=False)
def test_post():
    print("Received a POST request on /api/test")  # Log the request
    return jsonify({"message": "POST request received successfully!"}), 200

@app.route('/api/test_get', methods=['GET'])
def status():
    return jsonify({"status": "running"}), 200

if __name__ == "__main__":
    os.makedirs('flask/uploads', exist_ok=True)
    app.run(host='0.0.0.0', port=5000, debug=True)