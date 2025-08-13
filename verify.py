"""
Quick verification script for Ragnarok X Auto Fishing Bot
Tests basic functionality and requirements
"""

import sys
import os

def test_imports():
    """Test if all required modules can be imported"""
    print("Testing required modules...")
    
    required_modules = [
        ('tkinter', 'GUI library'),
        ('pyautogui', 'Automation library'),
        ('cv2', 'OpenCV for image processing'),
        ('numpy', 'Numerical computing'),
        ('PIL', 'Image processing'),
        ('pynput', 'Input monitoring'),
        ('configparser', 'Configuration management'),
        ('psutil', 'System utilities')
    ]
    
    missing_modules = []
    
    for module_name, description in required_modules:
        try:
            __import__(module_name)
            print(f"✓ {module_name} - {description}")
        except ImportError as e:
            print(f"✗ {module_name} - MISSING ({description})")
            missing_modules.append(module_name)
            
    return missing_modules

def test_files():
    """Test if all required files exist"""
    print("\nTesting required files...")
    
    required_files = [
        ('launcher.py', 'Main launcher'),
        ('main.py', 'Fishing bot application'),
        ('image_detector.py', 'Image detection module'),
        ('config_manager.py', 'Configuration manager'),
        ('utils.py', 'Utility tools'),
        ('README.md', 'Documentation')
    ]
    
    missing_files = []
    
    for filename, description in required_files:
        if os.path.exists(filename):
            print(f"✓ {filename} - {description}")
        else:
            print(f"✗ {filename} - MISSING ({description})")
            missing_files.append(filename)
            
    return missing_files

def test_functionality():
    """Test basic functionality"""
    print("\nTesting basic functionality...")
    
    try:
        # Test PyAutoGUI
        import pyautogui
        screen_size = pyautogui.size()
        print(f"✓ Screen capture working - Screen size: {screen_size}")
        
        # Test OpenCV
        import cv2
        print(f"✓ OpenCV working - Version: {cv2.__version__}")
        
        # Test image processing
        import numpy as np
        test_array = np.zeros((100, 100, 3), dtype=np.uint8)
        print("✓ NumPy arrays working")
        
        # Test configuration
        from config_manager import ConfigManager
        config_mgr = ConfigManager()
        print("✓ Configuration manager working")
        
        # Test image detector
        from image_detector import ImageDetector
        detector = ImageDetector()
        print("✓ Image detector working")
        
        return True
        
    except Exception as e:
        print(f"✗ Functionality test failed: {str(e)}")
        return False

def main():
    """Main verification function"""
    print("Ragnarok X Auto Fishing Bot - Verification Script")
    print("=" * 50)
    
    # Test imports
    missing_modules = test_imports()
    
    # Test files
    missing_files = test_files()
    
    # Test functionality
    functionality_ok = test_functionality()
    
    # Summary
    print("\n" + "=" * 50)
    print("VERIFICATION SUMMARY")
    print("=" * 50)
    
    if missing_modules:
        print(f"❌ MISSING MODULES: {', '.join(missing_modules)}")
        print("   Run 'pip install -r requirements.txt' to install missing packages")
    else:
        print("✅ All required modules are available")
        
    if missing_files:
        print(f"❌ MISSING FILES: {', '.join(missing_files)}")
        print("   Please ensure all bot files are in the correct directory")
    else:
        print("✅ All required files are present")
        
    if functionality_ok and not missing_modules and not missing_files:
        print("✅ ALL TESTS PASSED - Bot is ready to use!")
        print("\nNext steps:")
        print("1. Run 'python launcher.py' to start the bot")
        print("2. Use the coordinate detector to set up positions")
        print("3. Configure your settings")
        print("4. Start fishing!")
    else:
        print("❌ ISSUES FOUND - Please resolve the above problems before using the bot")
        
    print("\nFor help and documentation, see README.md")

if __name__ == "__main__":
    main()
    input("\nPress Enter to exit...")
