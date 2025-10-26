"""
Smart Agro Vision - Plant Disease Prediction Application
Flask web application for predicting plant diseases using CNN
"""

from flask import Flask, render_template, request, jsonify, session
import tensorflow as tf
from tensorflow import keras
import numpy as np
from PIL import Image
import io
import os
import base64
from plant_disease_model import PlantDiseaseCNN, DISEASE_CLASSES, get_disease_info

app = Flask(__name__)
app.secret_key = 'smart_agro_vision_secret_key_2023'

# Global model variable
model = None
img_height = 224
img_width = 224

def load_pretrained_model():
    """Load or create the CNN model"""
    global model
    model_path = 'plant_disease_model.h5'
    
    cnn_model = PlantDiseaseCNN(img_height=img_height, img_width=img_width, 
                                num_classes=len(DISEASE_CLASSES))
    
    # Try to load existing model, otherwise create a new one
    if os.path.exists(model_path):
        if cnn_model.load_model(model_path):
            model = cnn_model.model
            print("Pre-trained model loaded successfully!")
        else:
            # Build a new model if loading fails
            cnn_model.build_model()
            cnn_model.compile_model()
            model = cnn_model.model
            print("New model created (no pre-trained weights)")
    else:
        # Build a new model
        cnn_model.build_model()
        cnn_model.compile_model()
        model = cnn_model.model
        print("New model created (no pre-trained weights)")
    
    return model

def preprocess_image(image_file):
    """
    Preprocess the uploaded image for model prediction
    
    Args:
        image_file: Uploaded image file
        
    Returns:
        Preprocessed image array
    """
    try:
        # Read image
        img = Image.open(image_file)
        
        # Convert to RGB if necessary
        if img.mode != 'RGB':
            img = img.convert('RGB')
        
        # Resize to model input size
        img = img.resize((img_width, img_height))
        
        # Convert to array and normalize
        img_array = np.array(img)
        img_array = img_array / 255.0  # Normalize to [0, 1]
        
        # Add batch dimension
        img_array = np.expand_dims(img_array, axis=0)
        
        return img_array, img
    
    except Exception as e:
        print(f"Error preprocessing image: {e}")
        return None, None

def predict_disease(image_array):
    """
    Predict disease from preprocessed image
    
    Args:
        image_array: Preprocessed image array
        
    Returns:
        Prediction results dictionary
    """
    try:
        # Make prediction
        predictions = model.predict(image_array)
        
        # Get top prediction
        predicted_class_idx = np.argmax(predictions[0])
        confidence = float(predictions[0][predicted_class_idx])
        
        # Get disease name
        disease_name = DISEASE_CLASSES[predicted_class_idx]
        
        # Get top 3 predictions
        top_3_idx = np.argsort(predictions[0])[-3:][::-1]
        top_3_predictions = [
            {
                'disease': DISEASE_CLASSES[idx],
                'confidence': float(predictions[0][idx]) * 100
            }
            for idx in top_3_idx
        ]
        
        # Get disease information
        disease_info = get_disease_info(disease_name)
        
        return {
            'success': True,
            'disease': disease_name,
            'confidence': confidence * 100,
            'description': disease_info['description'],
            'treatment': disease_info['treatment'],
            'top_predictions': top_3_predictions
        }
    
    except Exception as e:
        print(f"Error making prediction: {e}")
        return {
            'success': False,
            'error': str(e)
        }

@app.route('/')
def index():
    """Home page"""
    return render_template('plant_disease.html')

@app.route('/predict', methods=['POST'])
def predict():
    """Handle image upload and prediction"""
    try:
        # Check if image file is present
        if 'image' not in request.files:
            return jsonify({'success': False, 'error': 'No image file provided'})
        
        file = request.files['image']
        
        if file.filename == '':
            return jsonify({'success': False, 'error': 'No image selected'})
        
        # Preprocess image
        img_array, original_img = preprocess_image(file)
        
        if img_array is None:
            return jsonify({'success': False, 'error': 'Error processing image'})
        
        # Make prediction
        result = predict_disease(img_array)
        
        # Convert image to base64 for display
        buffered = io.BytesIO()
        original_img.save(buffered, format="PNG")
        img_str = base64.b64encode(buffered.getvalue()).decode()
        result['image_data'] = img_str
        
        return jsonify(result)
    
    except Exception as e:
        print(f"Error in predict route: {e}")
        return jsonify({'success': False, 'error': str(e)})

@app.route('/about')
def about():
    """About page with project information"""
    return render_template('about.html')

@app.route('/diseases')
def diseases():
    """Disease information page"""
    return render_template('diseases.html', diseases=DISEASE_CLASSES)

if __name__ == '__main__':
    # Load the model
    print("Loading CNN model...")
    load_pretrained_model()
    print("Model ready!")
    
    # Run the Flask app
    app.run(debug=True, host='0.0.0.0', port=5000)
