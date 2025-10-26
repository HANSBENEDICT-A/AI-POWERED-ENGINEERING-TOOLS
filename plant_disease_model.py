"""
Plant Disease Prediction Model using CNN
This module contains the CNN architecture for plant disease classification
"""

import tensorflow as tf
from tensorflow import keras
from tensorflow.keras import layers, models
from tensorflow.keras.preprocessing.image import ImageDataGenerator
import numpy as np
import os


class PlantDiseaseCNN:
    """CNN Model for Plant Disease Classification"""
    
    def __init__(self, img_height=224, img_width=224, num_classes=38):
        """
        Initialize the CNN model
        
        Args:
            img_height: Height of input images
            img_width: Width of input images
            num_classes: Number of disease classes to predict
        """
        self.img_height = img_height
        self.img_width = img_width
        self.num_classes = num_classes
        self.model = None
        
    def build_model(self):
        """Build the CNN architecture"""
        self.model = models.Sequential([
            # First Convolutional Block
            layers.Conv2D(32, (3, 3), activation='relu', 
                         input_shape=(self.img_height, self.img_width, 3)),
            layers.BatchNormalization(),
            layers.MaxPooling2D((2, 2)),
            
            # Second Convolutional Block
            layers.Conv2D(64, (3, 3), activation='relu'),
            layers.BatchNormalization(),
            layers.MaxPooling2D((2, 2)),
            
            # Third Convolutional Block
            layers.Conv2D(128, (3, 3), activation='relu'),
            layers.BatchNormalization(),
            layers.MaxPooling2D((2, 2)),
            
            # Fourth Convolutional Block
            layers.Conv2D(256, (3, 3), activation='relu'),
            layers.BatchNormalization(),
            layers.MaxPooling2D((2, 2)),
            
            # Fifth Convolutional Block
            layers.Conv2D(512, (3, 3), activation='relu'),
            layers.BatchNormalization(),
            layers.MaxPooling2D((2, 2)),
            
            # Flatten and Dense Layers
            layers.Flatten(),
            layers.Dense(512, activation='relu'),
            layers.Dropout(0.5),
            layers.Dense(256, activation='relu'),
            layers.Dropout(0.3),
            layers.Dense(self.num_classes, activation='softmax')
        ])
        
        return self.model
    
    def compile_model(self, learning_rate=0.001):
        """Compile the model with optimizer and loss function"""
        if self.model is None:
            self.build_model()
            
        self.model.compile(
            optimizer=keras.optimizers.Adam(learning_rate=learning_rate),
            loss='categorical_crossentropy',
            metrics=['accuracy']
        )
        
    def get_model_summary(self):
        """Get model architecture summary"""
        if self.model is None:
            self.build_model()
        return self.model.summary()
    
    def save_model(self, filepath):
        """Save the trained model"""
        if self.model is not None:
            self.model.save(filepath)
            print(f"Model saved to {filepath}")
        else:
            print("No model to save. Build and train the model first.")
    
    def load_model(self, filepath):
        """Load a pre-trained model"""
        if os.path.exists(filepath):
            self.model = keras.models.load_model(filepath)
            print(f"Model loaded from {filepath}")
            return True
        else:
            print(f"Model file not found: {filepath}")
            return False


# Disease class names (PlantVillage dataset standard)
DISEASE_CLASSES = [
    'Apple___Apple_scab',
    'Apple___Black_rot',
    'Apple___Cedar_apple_rust',
    'Apple___healthy',
    'Blueberry___healthy',
    'Cherry_(including_sour)___Powdery_mildew',
    'Cherry_(including_sour)___healthy',
    'Corn_(maize)___Cercospora_leaf_spot Gray_leaf_spot',
    'Corn_(maize)___Common_rust_',
    'Corn_(maize)___Northern_Leaf_Blight',
    'Corn_(maize)___healthy',
    'Grape___Black_rot',
    'Grape___Esca_(Black_Measles)',
    'Grape___Leaf_blight_(Isariopsis_Leaf_Spot)',
    'Grape___healthy',
    'Orange___Haunglongbing_(Citrus_greening)',
    'Peach___Bacterial_spot',
    'Peach___healthy',
    'Pepper,_bell___Bacterial_spot',
    'Pepper,_bell___healthy',
    'Potato___Early_blight',
    'Potato___Late_blight',
    'Potato___healthy',
    'Raspberry___healthy',
    'Soybean___healthy',
    'Squash___Powdery_mildew',
    'Strawberry___Leaf_scorch',
    'Strawberry___healthy',
    'Tomato___Bacterial_spot',
    'Tomato___Early_blight',
    'Tomato___Late_blight',
    'Tomato___Leaf_Mold',
    'Tomato___Septoria_leaf_spot',
    'Tomato___Spider_mites Two-spotted_spider_mite',
    'Tomato___Target_Spot',
    'Tomato___Tomato_Yellow_Leaf_Curl_Virus',
    'Tomato___Tomato_mosaic_virus',
    'Tomato___healthy'
]

# Disease information and treatment recommendations
DISEASE_INFO = {
    'Apple___Apple_scab': {
        'description': 'Apple scab is a fungal disease that affects apple trees, causing dark spots on leaves and fruit.',
        'treatment': 'Apply fungicides, remove infected leaves, and improve air circulation around trees.'
    },
    'Apple___Black_rot': {
        'description': 'Black rot causes dark lesions on leaves, fruit rot, and cankers on branches.',
        'treatment': 'Prune infected branches, remove mummified fruit, and apply appropriate fungicides.'
    },
    'Apple___Cedar_apple_rust': {
        'description': 'This fungal disease causes yellow-orange spots on apple leaves.',
        'treatment': 'Remove nearby cedar trees if possible, apply fungicides during wet seasons.'
    },
    'Apple___healthy': {
        'description': 'Your apple plant appears healthy!',
        'treatment': 'Continue regular care and monitoring.'
    },
    'Tomato___Late_blight': {
        'description': 'Late blight is a devastating disease that can quickly kill tomato plants.',
        'treatment': 'Remove infected plants immediately, apply copper-based fungicides preventatively.'
    },
    'Tomato___Early_blight': {
        'description': 'Early blight causes dark spots with concentric rings on lower leaves.',
        'treatment': 'Remove infected leaves, improve air circulation, and apply fungicides.'
    },
    'Tomato___healthy': {
        'description': 'Your tomato plant appears healthy!',
        'treatment': 'Continue regular care and monitoring.'
    },
    'Potato___Late_blight': {
        'description': 'Late blight causes water-soaked spots on leaves and can destroy potato crops.',
        'treatment': 'Apply fungicides preventatively, remove infected plants, ensure good drainage.'
    },
    'Potato___Early_blight': {
        'description': 'Early blight affects potato leaves with dark brown spots.',
        'treatment': 'Rotate crops, remove infected leaves, and apply fungicides.'
    },
    'Corn_(maize)___Common_rust_': {
        'description': 'Common rust appears as small, circular reddish-brown pustules on corn leaves.',
        'treatment': 'Plant resistant varieties, remove infected plant debris.'
    },
}

# Add generic info for diseases not specifically listed
def get_disease_info(disease_name):
    """Get disease information or return generic info if not found"""
    if disease_name in DISEASE_INFO:
        return DISEASE_INFO[disease_name]
    
    # Generate generic info for unlisted diseases
    if 'healthy' in disease_name.lower():
        return {
            'description': 'Your plant appears healthy!',
            'treatment': 'Continue regular care and monitoring.'
        }
    else:
        return {
            'description': f'{disease_name.replace("___", " - ").replace("_", " ")}',
            'treatment': 'Consult with a local agricultural extension office for specific treatment recommendations.'
        }
