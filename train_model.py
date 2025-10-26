"""
Training Script Template for Plant Disease CNN Model

This script provides a template for training the CNN model on a dataset.
You'll need to download the PlantVillage dataset or prepare your own dataset.

Dataset Structure:
dataset/
├── train/
│   ├── Apple___Apple_scab/
│   │   ├── image1.jpg
│   │   ├── image2.jpg
│   │   └── ...
│   ├── Apple___Black_rot/
│   └── ...
└── validation/
    ├── Apple___Apple_scab/
    └── ...
"""

import os
from tensorflow.keras.preprocessing.image import ImageDataGenerator
from plant_disease_model import PlantDiseaseCNN

# Configuration
DATASET_DIR = 'dataset'  # Path to your dataset
TRAIN_DIR = os.path.join(DATASET_DIR, 'train')
VAL_DIR = os.path.join(DATASET_DIR, 'validation')

IMG_HEIGHT = 224
IMG_WIDTH = 224
BATCH_SIZE = 32
EPOCHS = 20
NUM_CLASSES = 38

def train_model():
    """Train the plant disease CNN model"""
    
    # Check if dataset exists
    if not os.path.exists(TRAIN_DIR):
        print(f"Error: Training directory not found: {TRAIN_DIR}")
        print("\nPlease download and organize the dataset first.")
        print("Expected structure:")
        print("  dataset/")
        print("    train/")
        print("      Apple___Apple_scab/")
        print("      Apple___Black_rot/")
        print("      ...")
        return
    
    print("=" * 60)
    print("Plant Disease CNN Model Training")
    print("=" * 60)
    
    # Data augmentation for training
    train_datagen = ImageDataGenerator(
        rescale=1./255,
        rotation_range=20,
        width_shift_range=0.2,
        height_shift_range=0.2,
        horizontal_flip=True,
        zoom_range=0.2,
        shear_range=0.2,
        fill_mode='nearest'
    )
    
    # Only rescaling for validation
    val_datagen = ImageDataGenerator(rescale=1./255)
    
    # Load training data
    print("\nLoading training data...")
    train_generator = train_datagen.flow_from_directory(
        TRAIN_DIR,
        target_size=(IMG_HEIGHT, IMG_WIDTH),
        batch_size=BATCH_SIZE,
        class_mode='categorical'
    )
    
    # Load validation data
    print("Loading validation data...")
    validation_generator = val_datagen.flow_from_directory(
        VAL_DIR,
        target_size=(IMG_HEIGHT, IMG_WIDTH),
        batch_size=BATCH_SIZE,
        class_mode='categorical'
    )
    
    print(f"\nFound {train_generator.samples} training images")
    print(f"Found {validation_generator.samples} validation images")
    print(f"Number of classes: {len(train_generator.class_indices)}")
    
    # Create and build model
    print("\nBuilding CNN model...")
    model = PlantDiseaseCNN(
        img_height=IMG_HEIGHT,
        img_width=IMG_WIDTH,
        num_classes=NUM_CLASSES
    )
    model.build_model()
    model.compile_model(learning_rate=0.001)
    
    # Display model summary
    print("\nModel Architecture:")
    model.get_model_summary()
    
    # Calculate steps
    steps_per_epoch = train_generator.samples // BATCH_SIZE
    validation_steps = validation_generator.samples // BATCH_SIZE
    
    print(f"\nTraining Configuration:")
    print(f"  Epochs: {EPOCHS}")
    print(f"  Batch Size: {BATCH_SIZE}")
    print(f"  Steps per Epoch: {steps_per_epoch}")
    print(f"  Validation Steps: {validation_steps}")
    
    # Train the model
    print("\nStarting training...")
    print("=" * 60)
    
    history = model.model.fit(
        train_generator,
        steps_per_epoch=steps_per_epoch,
        epochs=EPOCHS,
        validation_data=validation_generator,
        validation_steps=validation_steps,
        verbose=1
    )
    
    print("\n" + "=" * 60)
    print("Training completed!")
    print("=" * 60)
    
    # Save the trained model
    model_path = 'plant_disease_model.h5'
    model.save_model(model_path)
    print(f"\n✓ Model saved to: {model_path}")
    
    # Print final metrics
    final_train_acc = history.history['accuracy'][-1]
    final_val_acc = history.history['val_accuracy'][-1]
    final_train_loss = history.history['loss'][-1]
    final_val_loss = history.history['val_loss'][-1]
    
    print("\nFinal Training Metrics:")
    print(f"  Training Accuracy: {final_train_acc:.4f}")
    print(f"  Training Loss: {final_train_loss:.4f}")
    print(f"  Validation Accuracy: {final_val_acc:.4f}")
    print(f"  Validation Loss: {final_val_loss:.4f}")
    
    # Save class indices
    import json
    class_indices = train_generator.class_indices
    with open('class_indices.json', 'w') as f:
        json.dump(class_indices, f, indent=2)
    print(f"\n✓ Class indices saved to: class_indices.json")
    
    return history

def plot_training_history(history):
    """Plot training history"""
    try:
        import matplotlib.pyplot as plt
        
        # Plot accuracy
        plt.figure(figsize=(12, 4))
        
        plt.subplot(1, 2, 1)
        plt.plot(history.history['accuracy'], label='Training Accuracy')
        plt.plot(history.history['val_accuracy'], label='Validation Accuracy')
        plt.title('Model Accuracy')
        plt.xlabel('Epoch')
        plt.ylabel('Accuracy')
        plt.legend()
        plt.grid(True)
        
        # Plot loss
        plt.subplot(1, 2, 2)
        plt.plot(history.history['loss'], label='Training Loss')
        plt.plot(history.history['val_loss'], label='Validation Loss')
        plt.title('Model Loss')
        plt.xlabel('Epoch')
        plt.ylabel('Loss')
        plt.legend()
        plt.grid(True)
        
        plt.tight_layout()
        plt.savefig('training_history.png')
        print("\n✓ Training plots saved to: training_history.png")
        
    except ImportError:
        print("\nNote: Install matplotlib to generate training plots")
        print("  pip install matplotlib")

if __name__ == "__main__":
    print("\n" + "=" * 60)
    print("Plant Disease CNN - Training Script")
    print("=" * 60)
    
    # Instructions
    print("\nBefore running this script:")
    print("1. Download the PlantVillage dataset")
    print("2. Organize it in the 'dataset/' directory")
    print("3. Split into 'train/' and 'validation/' folders")
    print("4. Each subfolder should be named after the disease class")
    print("\nDataset download links:")
    print("  - Kaggle: https://www.kaggle.com/datasets/emmarex/plantdisease")
    print("  - GitHub: https://github.com/spMohanty/PlantVillage-Dataset")
    
    # Check if user wants to continue
    response = input("\nDo you have the dataset ready? (yes/no): ").lower()
    
    if response in ['yes', 'y']:
        print("\nStarting training process...")
        history = train_model()
        
        if history:
            # Plot training history
            plot_training_history(history)
            
            print("\n" + "=" * 60)
            print("Training Complete! 🎉")
            print("=" * 60)
            print("\nYour trained model is ready to use!")
            print("Run the application: python plant_disease_app.py")
    else:
        print("\nPlease prepare the dataset and run this script again.")
        print("See USAGE_GUIDE.md for more information.")
