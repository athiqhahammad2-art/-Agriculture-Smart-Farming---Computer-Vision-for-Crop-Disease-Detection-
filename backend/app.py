from flask import Flask, request, jsonify
from flask_cors import CORS
import os
from dotenv import load_dotenv
from models.disease_detector import DiseaseDetector
from utils.image_processor import ImageProcessor
from database.db_handler import DatabaseHandler
import logging

load_dotenv()

app = Flask(__name__)
CORS(app)

# Initialize components
detector = DiseaseDetector()
image_processor = ImageProcessor()
db = DatabaseHandler()

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

@app.route('/api/health', methods=['GET'])
def health():
    return jsonify({'status': 'healthy', 'service': 'Crop Disease Detection API'}), 200

@app.route('/api/predict', methods=['POST'])
def predict_disease():
    try:
        if 'image' not in request.files:
            return jsonify({'error': 'No image provided'}), 400
        
        file = request.files['image']
        if file.filename == '':
            return jsonify({'error': 'No selected file'}), 400
        
        # Process image
        image_path = os.path.join('temp', file.filename)
        file.save(image_path)
        processed_image = image_processor.preprocess(image_path)
        
        # Get prediction
        prediction = detector.predict(processed_image)
        disease_name = prediction['disease']
        confidence = prediction['confidence']
        
        # Get recommendations
        recommendations = get_treatment_recommendations(disease_name)
        
        # Store in database
        result = {
            'disease': disease_name,
            'confidence': float(confidence),
            'recommendations': recommendations,
            'timestamp': db.store_prediction(disease_name, confidence)
        }
        
        # Cleanup
        os.remove(image_path)
        
        return jsonify(result), 200
    
    except Exception as e:
        logger.error(f"Prediction error: {str(e)}")
        return jsonify({'error': str(e)}), 500

@app.route('/api/history', methods=['GET'])
def get_history():
    try:
        limit = request.args.get('limit', 10, type=int)
        history = db.get_predictions(limit)
        return jsonify({'history': history}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/statistics', methods=['GET'])
def get_statistics():
    try:
        stats = db.get_statistics()
        return jsonify(stats), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

def get_treatment_recommendations(disease_name):
    """Get treatment recommendations for detected disease"""
    recommendations = {
        'Early Blight': {
            'severity': 'High',
            'treatments': ['Apply fungicide (Chlorothalonil or Mancozeb)', 'Remove infected leaves', 'Improve air circulation'],
            'prevention': ['Crop rotation', 'Avoid overhead irrigation', 'Remove debris']
        },
        'Late Blight': {
            'severity': 'Critical',
            'treatments': ['Apply systemic fungicide (Metalaxyl)', 'Isolate affected plants', 'Reduce humidity'],
            'prevention': ['Use resistant varieties', 'Monitor weather closely', 'Prophylactic spraying']
        },
        'Septoria': {
            'severity': 'Medium',
            'treatments': ['Apply protectant fungicide', 'Prune affected leaves', 'Ensure drainage'],
            'prevention': ['Sanitize tools', 'Avoid leaf wetness', 'Space plants properly']
        },
        'Powdery Mildew': {
            'severity': 'Medium',
            'treatments': ['Apply sulfur-based fungicide', 'Increase air circulation', 'Reduce humidity'],
            'prevention': ['Improve ventilation', 'Reduce nitrogen', 'Clean greenhouse']
        },
        'Healthy': {
            'severity': 'None',
            'treatments': ['Continue regular monitoring', 'Maintain optimal conditions'],
            'prevention': ['Maintain hygiene', 'Regular inspections', 'Proper spacing']
        }
    }
    return recommendations.get(disease_name, {'severity': 'Unknown', 'treatments': [], 'prevention': []})

@app.route('/api/diseases', methods=['GET'])
def get_diseases():
    diseases = [
        {'name': 'Early Blight', 'description': 'Fungal disease affecting leaves and stems'},
        {'name': 'Late Blight', 'description': 'Highly destructive water mold disease'},
        {'name': 'Septoria', 'description': 'Fungal leaf spot disease'},
        {'name': 'Powdery Mildew', 'description': 'White powdery coating on leaves'},
        {'name': 'Healthy', 'description': 'No disease detected'}
    ]
    return jsonify({'diseases': diseases}), 200

if __name__ == '__main__':
    os.makedirs('temp', exist_ok=True)
    app.run(debug=True, host='0.0.0.0', port=5000)