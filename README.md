# Smart Agro Vision - Plant Disease Prediction System

An AI-powered plant disease prediction system using Convolutional Neural Networks (CNN) for accurate detection and classification of plant diseases.

## 🌱 Project Overview

Smart Agro Vision is a deep learning-based web application that helps farmers, gardeners, and agricultural professionals identify plant diseases from leaf images. The system uses a CNN architecture to classify 38 different plant disease conditions across 15 plant species.

## ✨ Features

- **Accurate Disease Detection**: Advanced CNN model trained for plant disease classification
- **Fast Results**: Get predictions in seconds
- **38 Disease Classes**: Supports multiple plant species and disease types
- **Confidence Scores**: See prediction confidence levels
- **Treatment Recommendations**: Receive actionable treatment advice
- **User-Friendly Interface**: Simple image upload and intuitive results display
- **Mobile Responsive**: Works on desktop and mobile devices
- **No IoT Required**: Simple standalone web application

## 🔧 Technology Stack

- **Backend**: Flask (Python)
- **Deep Learning**: TensorFlow/Keras
- **Model Architecture**: CNN with 5 convolutional layers
- **Image Processing**: Pillow (PIL)
- **Frontend**: HTML5, CSS3, JavaScript

## 📋 Supported Plants & Diseases

The system can detect diseases in:
- Apple (Scab, Black Rot, Cedar Apple Rust)
- Tomato (Late Blight, Early Blight, Leaf Mold, Septoria, etc.)
- Potato (Early Blight, Late Blight)
- Corn/Maize (Common Rust, Gray Leaf Spot, Northern Leaf Blight)
- Grape (Black Rot, Esca, Leaf Blight)
- Cherry, Pepper, Peach, Strawberry, and more...

## 🚀 Installation & Setup

### Prerequisites
- Python 3.8 or higher
- pip package manager

### Installation Steps

1. Clone the repository:
```bash
git clone https://github.com/HANSBENEDICT-A/AI-POWERED-ENGINEERING-TOOLS.git
cd AI-POWERED-ENGINEERING-TOOLS
```

2. Install required dependencies:
```bash
pip install -r requirements.txt
```

3. Run the application:
```bash
python plant_disease_app.py
```

4. Open your browser and navigate to:
```
http://localhost:5000
```

## 📖 Usage Instructions

1. **Upload Image**: Click "Choose Image" and select a clear photo of a plant leaf
2. **Predict**: Click "Predict Disease" to analyze the image
3. **View Results**: See the predicted disease, confidence score, and treatment recommendations
4. **Browse Info**: Explore the Disease Info page to learn about all supported conditions

## 🧠 CNN Architecture

The model uses a deep CNN architecture:
- **Input**: 224x224x3 RGB images
- **Convolutional Blocks**: 5 layers (32, 64, 128, 256, 512 filters)
- **Activation**: ReLU with Batch Normalization
- **Pooling**: MaxPooling (2x2)
- **Dense Layers**: 512 and 256 neurons with Dropout
- **Output**: 38 classes with Softmax activation
- **Optimizer**: Adam
- **Loss Function**: Categorical Crossentropy

## 📁 Project Structure

```
AI-POWERED-ENGINEERING-TOOLS/
├── plant_disease_app.py       # Main Flask application
├── plant_disease_model.py     # CNN model architecture
├── requirements.txt           # Python dependencies
├── README.md                  # Project documentation
├── templates/
│   ├── plant_disease.html    # Main interface
│   ├── about.html            # About page
│   └── diseases.html         # Disease database page
└── plant_disease_model.h5    # Pre-trained model (if available)
```

## 🎯 Important Notes

- For best results, use clear, well-lit images of plant leaves
- Ensure the leaf occupies most of the image frame
- Avoid blurry or dark images
- The model works best with leaves showing clear symptoms

## 🔮 Future Enhancements

- Expanded disease database
- Support for more plant species
- Historical tracking of plant health
- Mobile application
- Multi-language support
- Integration with agricultural databases

## 📄 License

This project is open source and available for educational and research purposes.

## 🤝 Contributing

Contributions are welcome! Please feel free to submit pull requests or open issues for bugs and feature requests.

## 📧 Contact

For questions or support, please open an issue on GitHub.

---
**Smart Agro Vision** - Empowering Agriculture with AI 🌱
