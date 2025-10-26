"""
Test script for Plant Disease Prediction System
This script tests the CNN model initialization and basic functionality
"""

import sys
import numpy as np
from PIL import Image
import io

try:
    from plant_disease_model import PlantDiseaseCNN, DISEASE_CLASSES, get_disease_info
    print("✓ Successfully imported plant_disease_model")
except ImportError as e:
    print(f"✗ Failed to import plant_disease_model: {e}")
    sys.exit(1)

def test_model_initialization():
    """Test if the CNN model can be initialized"""
    print("\n=== Testing Model Initialization ===")
    try:
        model = PlantDiseaseCNN(img_height=224, img_width=224, num_classes=38)
        print("✓ Model object created")
        
        model.build_model()
        print("✓ Model architecture built")
        
        model.compile_model()
        print("✓ Model compiled")
        
        return True
    except Exception as e:
        print(f"✗ Model initialization failed: {e}")
        return False

def test_disease_classes():
    """Test disease class definitions"""
    print("\n=== Testing Disease Classes ===")
    try:
        print(f"✓ Number of disease classes: {len(DISEASE_CLASSES)}")
        
        # Check for some expected diseases
        expected = ['Apple___Apple_scab', 'Tomato___Late_blight', 'Potato___Early_blight']
        for disease in expected:
            if disease in DISEASE_CLASSES:
                print(f"✓ Found expected disease: {disease}")
            else:
                print(f"✗ Missing expected disease: {disease}")
        
        return True
    except Exception as e:
        print(f"✗ Disease class test failed: {e}")
        return False

def test_disease_info():
    """Test disease information retrieval"""
    print("\n=== Testing Disease Information ===")
    try:
        # Test a known disease
        info = get_disease_info('Apple___Apple_scab')
        print(f"✓ Retrieved info for Apple Scab")
        print(f"  Description: {info['description'][:50]}...")
        print(f"  Treatment: {info['treatment'][:50]}...")
        
        # Test a healthy plant
        info = get_disease_info('Apple___healthy')
        print(f"✓ Retrieved info for healthy Apple")
        
        # Test an unknown disease (should return generic info)
        info = get_disease_info('Unknown___Disease')
        print(f"✓ Retrieved generic info for unknown disease")
        
        return True
    except Exception as e:
        print(f"✗ Disease info test failed: {e}")
        return False

def test_model_prediction():
    """Test model prediction with a dummy image"""
    print("\n=== Testing Model Prediction ===")
    try:
        model = PlantDiseaseCNN(img_height=224, img_width=224, num_classes=38)
        model.build_model()
        model.compile_model()
        
        # Create a dummy image (random noise)
        dummy_image = np.random.rand(1, 224, 224, 3).astype(np.float32)
        
        predictions = model.model.predict(dummy_image, verbose=0)
        print(f"✓ Model prediction successful")
        print(f"✓ Prediction shape: {predictions.shape}")
        
        # Get top prediction
        top_class = np.argmax(predictions[0])
        confidence = predictions[0][top_class]
        print(f"✓ Top predicted class: {DISEASE_CLASSES[top_class]}")
        print(f"✓ Confidence: {confidence:.4f}")
        
        return True
    except Exception as e:
        print(f"✗ Model prediction test failed: {e}")
        return False

def run_all_tests():
    """Run all tests"""
    print("=" * 60)
    print("Smart Agro Vision - Test Suite")
    print("=" * 60)
    
    tests = [
        test_model_initialization,
        test_disease_classes,
        test_disease_info,
        test_model_prediction
    ]
    
    results = []
    for test in tests:
        try:
            result = test()
            results.append(result)
        except Exception as e:
            print(f"\n✗ Test crashed: {e}")
            results.append(False)
    
    print("\n" + "=" * 60)
    print("Test Summary")
    print("=" * 60)
    passed = sum(results)
    total = len(results)
    print(f"Passed: {passed}/{total}")
    
    if passed == total:
        print("\n🎉 All tests passed!")
        return 0
    else:
        print(f"\n⚠️  {total - passed} test(s) failed")
        return 1

if __name__ == "__main__":
    exit_code = run_all_tests()
    sys.exit(exit_code)
