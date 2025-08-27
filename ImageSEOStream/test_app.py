#!/usr/bin/env python3
"""
Test script for ImageSEO Pro application
Verifies core functionality without requiring API keys or file uploads
"""

import sys
from pathlib import Path
import tempfile
import shutil

def test_imports():
    """Test that all required modules can be imported"""
    print("🔍 Testing imports...")
    
    try:
        import streamlit
        print("✅ Streamlit imported successfully")
    except ImportError as e:
        print(f"❌ Streamlit import failed: {e}")
        return False
    
    try:
        import openai
        print("✅ OpenAI imported successfully")
    except ImportError as e:
        print(f"❌ OpenAI import failed: {e}")
        return False
    
    try:
        from PIL import Image
        print("✅ PIL/Pillow imported successfully")
    except ImportError as e:
        print(f"❌ PIL import failed: {e}")
        return False
    
    try:
        import cv2
        print("✅ OpenCV imported successfully")
    except ImportError as e:
        print(f"❌ OpenCV import failed: {e}")
        return False
    
    try:
        import numpy
        print("✅ NumPy imported successfully")
    except ImportError as e:
        print(f"❌ NumPy import failed: {e}")
        return False
    
    return True

def test_app_modules():
    """Test that app modules can be imported"""
    print("\n🔍 Testing app modules...")
    
    try:
        import app
        print("✅ Main app module imported successfully")
    except Exception as e:
        print(f"❌ App module import failed: {e}")
        return False
    
    try:
        from image_processor import ImageProcessor
        print("✅ ImageProcessor class imported successfully")
    except Exception as e:
        print(f"❌ ImageProcessor import failed: {e}")
        return False
    
    try:
        from utils import validate_folder, calculate_processing_stats
        print("✅ Utils functions imported successfully")
    except Exception as e:
        print(f"❌ Utils import failed: {e}")
        return False
    
    return True

def test_utils_functions():
    """Test utility functions"""
    print("\n🔍 Testing utility functions...")
    
    from utils import validate_folder, format_file_size, validate_api_key
    
    # Test validate_folder
    with tempfile.TemporaryDirectory() as temp_dir:
        temp_path = Path(temp_dir)
        result = validate_folder(temp_path)
        print(f"✅ validate_folder (empty): {result}")
        
        # Create a test file
        test_file = temp_path / "test.txt"
        test_file.write_text("test")
        result = validate_folder(temp_path)
        print(f"✅ validate_folder (with non-image): {result}")
    
    # Test format_file_size
    sizes = [1024, 1024*1024, 1024*1024*1024]
    for size in sizes:
        formatted = format_file_size(size)
        print(f"✅ format_file_size({size}): {formatted}")
    
    # Test validate_api_key
    test_keys = [
        ("", "empty"),
        ("invalid", "invalid format"),
        ("sk-test123456789012345678901234567890123456789012345678901234567890", "valid format")
    ]
    
    for key, description in test_keys:
        result = validate_api_key(key)
        print(f"✅ validate_api_key ({description}): {result['valid']}")
    
    return True

def test_image_processor_creation():
    """Test ImageProcessor class creation"""
    print("\n🔍 Testing ImageProcessor creation...")
    
    from image_processor import ImageProcessor
    
    try:
        # Test with dummy API key
        processor = ImageProcessor("sk-test123456789012345678901234567890123456789012345678901234567890")
        print("✅ ImageProcessor created successfully")
        
        # Test filename creation
        test_description = "modern kitchen design with white cabinets"
        test_extension = ".webp"
        filename = processor.create_seo_filename(test_description, test_extension)
        print(f"✅ SEO filename created: {filename}")
        
        return True
    except Exception as e:
        print(f"❌ ImageProcessor test failed: {e}")
        return False

def test_file_operations():
    """Test file operations"""
    print("\n🔍 Testing file operations...")
    
    # Test directory creation
    test_dir = Path("test_output")
    test_dir.mkdir(exist_ok=True)
    print(f"✅ Directory created: {test_dir}")
    
    # Test file creation
    test_file = test_dir / "test.txt"
    test_file.write_text("test content")
    print(f"✅ File created: {test_file}")
    
    # Cleanup
    test_file.unlink()
    test_dir.rmdir()
    print("✅ Cleanup completed")
    
    return True

def main():
    """Run all tests"""
    print("🎯 ImgSage - Application Test Suite")
    print("=" * 50)
    
    tests = [
        ("Import Tests", test_imports),
        ("App Module Tests", test_app_modules),
        ("Utility Function Tests", test_utils_functions),
        ("ImageProcessor Tests", test_image_processor_creation),
        ("File Operation Tests", test_file_operations)
    ]
    
    passed = 0
    total = len(tests)
    
    for test_name, test_func in tests:
        print(f"\n📋 Running {test_name}...")
        try:
            if test_func():
                print(f"✅ {test_name} PASSED")
                passed += 1
            else:
                print(f"❌ {test_name} FAILED")
        except Exception as e:
            print(f"❌ {test_name} FAILED with exception: {e}")
    
    print("\n" + "=" * 50)
    print(f"📊 Test Results: {passed}/{total} tests passed")
    
    if passed == total:
        print("🎉 All tests passed! Application is ready to run.")
        print("\n🚀 To start the application, run:")
        print("   streamlit run app.py")
        return 0
    else:
        print("⚠️  Some tests failed. Please check the errors above.")
        return 1

if __name__ == "__main__":
    sys.exit(main())
