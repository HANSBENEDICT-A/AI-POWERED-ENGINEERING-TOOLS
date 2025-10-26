# Smart Agro Vision - Quick Start Guide

## 🚀 Getting Started

### Step 1: Installation

1. Make sure you have Python 3.8+ installed:
```bash
python3 --version
```

2. Install required dependencies:
```bash
pip install -r requirements.txt
```

Expected packages:
- Flask (web framework)
- TensorFlow (deep learning)
- NumPy (numerical computing)
- Pillow (image processing)

### Step 2: Running the Application

Start the Flask server:
```bash
python plant_disease_app.py
```

You should see output like:
```
Loading CNN model...
New model created (no pre-trained weights)
Model ready!
 * Running on http://127.0.0.1:5000
```

### Step 3: Access the Web Interface

Open your web browser and go to:
```
http://localhost:5000
```

## 📱 Using the Application

### Main Features

1. **Home Page** (`/`)
   - Upload plant leaf images
   - Get instant disease predictions
   - View confidence scores
   - See treatment recommendations

2. **About Page** (`/about`)
   - Learn about the project
   - Understand the CNN architecture
   - View supported plants and diseases
   - Technical details

3. **Disease Info** (`/diseases`)
   - Browse all 38 disease classes
   - Filter by plant type
   - Search specific diseases
   - View statistics

### How to Predict a Disease

1. **Click "Choose Image"**
   - Select a clear photo of a plant leaf
   - Supported formats: JPG, PNG, etc.
   - Best results: well-lit, close-up leaf images

2. **Preview**
   - The image will appear on screen
   - Verify it's the correct image

3. **Click "Predict Disease"**
   - Wait a few seconds for analysis
   - The CNN model will process the image

4. **View Results**
   - Disease name and confidence score
   - Detailed description
   - Treatment recommendations
   - Top 3 predictions

## 📊 Understanding Results

### Confidence Levels
- **Green (80%+)**: High confidence - reliable prediction
- **Yellow (50-80%)**: Medium confidence - likely accurate
- **Red (<50%)**: Low confidence - consider retaking image

### Disease Names Format
`PlantName___DiseaseName`

Example:
- `Tomato___Late_blight` = Late blight on Tomato
- `Apple___healthy` = Healthy Apple plant

## 🖼️ Image Tips

### Best Practices
✅ Use clear, focused images
✅ Ensure good lighting
✅ Capture the entire leaf
✅ Show disease symptoms clearly
✅ Avoid shadows and glare

### Avoid
❌ Blurry or dark images
❌ Multiple leaves overlapping
❌ Extreme close-ups
❌ Images with heavy filters

## 🛠️ Troubleshooting

### Problem: "Module not found" error
**Solution**: Install missing dependencies
```bash
pip install flask tensorflow numpy pillow
```

### Problem: Slow predictions
**Cause**: CNN processing takes time on CPU
**Solution**: Wait 5-10 seconds; consider GPU if available

### Problem: Low confidence scores
**Cause**: Image quality or unusual symptoms
**Solution**: Try different images or angles

### Problem: Port already in use
**Solution**: Change port in `plant_disease_app.py`:
```python
app.run(debug=True, host='0.0.0.0', port=5001)  # Use 5001 instead
```

## 🧪 Testing

Run the test suite to verify installation:
```bash
python test_model.py
```

Expected output:
```
✓ Model object created
✓ Model architecture built
✓ Model compiled
✓ Number of disease classes: 38
🎉 All tests passed!
```

## 🔒 Important Notes

### Model Training
- The current model is initialized with random weights
- For production use, train the model on a labeled dataset
- Common dataset: PlantVillage (available online)

### Training Instructions
If you want to train the model:

1. Download the PlantVillage dataset
2. Organize images by class folders
3. Use this training code:

```python
from plant_disease_model import PlantDiseaseCNN

# Initialize model
model = PlantDiseaseCNN()
model.build_model()
model.compile_model()

# Train (pseudo-code)
# train_generator = ImageDataGenerator(...)
# model.model.fit(train_generator, epochs=20)

# Save trained model
model.save_model('plant_disease_model.h5')
```

### Performance
- **CPU**: 3-10 seconds per prediction
- **GPU**: <1 second per prediction
- **Accuracy**: Depends on training data quality

## 📚 Supported Disease Classes

The model detects 38 conditions across these plants:
- Apple (4 classes)
- Blueberry (1 class)
- Cherry (2 classes)
- Corn/Maize (4 classes)
- Grape (4 classes)
- Orange (1 class)
- Peach (2 classes)
- Pepper (2 classes)
- Potato (3 classes)
- Raspberry (1 class)
- Soybean (1 class)
- Squash (1 class)
- Strawberry (2 classes)
- Tomato (10 classes)

## 🌐 API Usage

You can also use the prediction API programmatically:

```python
import requests

# Prepare image
files = {'image': open('leaf.jpg', 'rb')}

# Send request
response = requests.post('http://localhost:5000/predict', files=files)

# Get results
result = response.json()
print(f"Disease: {result['disease']}")
print(f"Confidence: {result['confidence']:.2f}%")
```

## 🎓 Learning Resources

### Understanding CNNs
- Convolutional Neural Networks process images through layers
- Each layer learns different features (edges, textures, patterns)
- Multiple layers combine to recognize complex patterns

### Model Architecture
- Input: 224x224 RGB image
- 5 Convolutional blocks with increasing filters
- Batch normalization for stable training
- Dropout for preventing overfitting
- Softmax output for classification

## 💡 Tips for Best Results

1. **Image Quality**: Use high-resolution images
2. **Lighting**: Natural daylight works best
3. **Focus**: Ensure symptoms are clearly visible
4. **Angle**: Capture leaves flat against background
5. **Multiple Samples**: Test with several images if unsure

## 🤝 Contributing

To improve the system:
1. Collect more training data
2. Train on diverse datasets
3. Test with real-world images
4. Report issues and suggestions

## 📞 Support

For help or questions:
- Check the About page in the application
- Review this guide
- Open an issue on GitHub
- Consult the README.md file

---

**Happy Disease Detecting! 🌱**
