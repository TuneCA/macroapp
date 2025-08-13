"""
Image Detection Module for Ragnarok X Auto Fishing Bot
Handles screen capture, image recognition, and bite detection
"""

import cv2
import numpy as np
import pyautogui
from PIL import Image, ImageGrab
import time
import os

class ImageDetector:
    def __init__(self):
        self.template_dir = "templates"
        self.create_template_directory()
        
        # Detection parameters
        self.confidence_threshold = 0.8
        self.bite_templates = []
        self.ui_templates = {}
        
        # Screen capture settings
        self.capture_region = None  # (x, y, width, height)
        self.last_screenshot = None
        
    def create_template_directory(self):
        """Create directory for template images"""
        if not os.path.exists(self.template_dir):
            os.makedirs(self.template_dir)
            
    def capture_screen(self, region=None):
        """Capture screenshot of specified region or full screen"""
        try:
            if region:
                x, y, width, height = region
                screenshot = ImageGrab.grab(bbox=(x, y, x + width, y + height))
            else:
                screenshot = ImageGrab.grab()
                
            # Convert to OpenCV format
            screenshot_cv = cv2.cvtColor(np.array(screenshot), cv2.COLOR_RGB2BGR)
            self.last_screenshot = screenshot_cv
            return screenshot_cv
            
        except Exception as e:
            print(f"Screen capture error: {str(e)}")
            return None
            
    def find_template(self, template_path, screenshot=None, confidence=None):
        """Find template in screenshot using template matching"""
        try:
            if screenshot is None:
                screenshot = self.capture_screen()
                
            if screenshot is None:
                return None
                
            # Load template
            if isinstance(template_path, str):
                template = cv2.imread(template_path, cv2.IMREAD_COLOR)
            else:
                template = template_path
                
            if template is None:
                return None
                
            # Set confidence threshold
            if confidence is None:
                confidence = self.confidence_threshold
                
            # Perform template matching
            result = cv2.matchTemplate(screenshot, template, cv2.TM_CCOEFF_NORMED)
            min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(result)
            
            if max_val >= confidence:
                # Get template dimensions
                h, w = template.shape[:2]
                
                # Calculate center point
                center_x = max_loc[0] + w // 2
                center_y = max_loc[1] + h // 2
                
                return {
                    'found': True,
                    'confidence': max_val,
                    'position': (center_x, center_y),
                    'top_left': max_loc,
                    'bottom_right': (max_loc[0] + w, max_loc[1] + h),
                    'size': (w, h)
                }
            else:
                return {'found': False, 'confidence': max_val}
                
        except Exception as e:
            print(f"Template matching error: {str(e)}")
            return None
            
    def detect_color_change(self, region, color_range, threshold=0.1):
        """Detect color changes in a specific region"""
        try:
            screenshot = self.capture_screen(region)
            if screenshot is None:
                return False
                
            # Convert to HSV for better color detection
            hsv = cv2.cvtColor(screenshot, cv2.COLOR_BGR2HSV)
            
            # Create mask for specified color range
            lower_color = np.array(color_range[0])
            upper_color = np.array(color_range[1])
            mask = cv2.inRange(hsv, lower_color, upper_color)
            
            # Calculate percentage of pixels in color range
            pixel_count = np.sum(mask > 0)
            total_pixels = mask.shape[0] * mask.shape[1]
            percentage = pixel_count / total_pixels
            
            return percentage >= threshold
            
        except Exception as e:
            print(f"Color detection error: {str(e)}")
            return False
            
    def detect_motion(self, region, sensitivity=30):
        """Detect motion in a specific region by comparing with previous frame"""
        try:
            current_frame = self.capture_screen(region)
            if current_frame is None:
                return False
                
            if not hasattr(self, 'previous_frame') or self.previous_frame is None:
                self.previous_frame = current_frame
                return False
                
            # Convert to grayscale
            current_gray = cv2.cvtColor(current_frame, cv2.COLOR_BGR2GRAY)
            previous_gray = cv2.cvtColor(self.previous_frame, cv2.COLOR_BGR2GRAY)
            
            # Calculate absolute difference
            diff = cv2.absdiff(current_gray, previous_gray)
            
            # Apply threshold
            _, thresh = cv2.threshold(diff, sensitivity, 255, cv2.THRESH_BINARY)
            
            # Calculate motion percentage
            motion_pixels = np.sum(thresh > 0)
            total_pixels = thresh.shape[0] * thresh.shape[1]
            motion_percentage = motion_pixels / total_pixels
            
            # Update previous frame
            self.previous_frame = current_frame
            
            return motion_percentage > 0.05  # 5% change threshold
            
        except Exception as e:
            print(f"Motion detection error: {str(e)}")
            return False
            
    def detect_fishing_bite(self, fishing_region):
        """Detect fishing bite using multiple detection methods"""
        try:
            # Method 1: Look for bobber movement
            motion_detected = self.detect_motion(fishing_region, sensitivity=20)
            
            # Method 2: Look for color changes (water splash, etc.)
            splash_colors = [
                ([100, 50, 50], [130, 255, 255]),  # Blue range for water
                ([0, 0, 200], [180, 30, 255])      # White range for splash
            ]
            
            color_change = False
            for color_range in splash_colors:
                if self.detect_color_change(fishing_region, color_range, threshold=0.05):
                    color_change = True
                    break
                    
            # Method 3: Template matching for specific bite indicators
            bite_template_found = False
            for template_path in self.get_bite_templates():
                result = self.find_template(template_path, confidence=0.7)
                if result and result['found']:
                    bite_template_found = True
                    break
                    
            # Combine detection methods
            return motion_detected or color_change or bite_template_found
            
        except Exception as e:
            print(f"Bite detection error: {str(e)}")
            return False
            
    def get_bite_templates(self):
        """Get list of bite indicator templates"""
        templates = []
        template_files = [
            "bite_indicator.png",
            "bobber_splash.png",
            "hook_icon.png",
            "exclamation.png"
        ]
        
        for filename in template_files:
            filepath = os.path.join(self.template_dir, filename)
            if os.path.exists(filepath):
                templates.append(filepath)
                
        return templates
        
    def find_ui_element(self, element_name):
        """Find UI element like buttons, icons, etc."""
        template_path = os.path.join(self.template_dir, f"{element_name}.png")
        if os.path.exists(template_path):
            return self.find_template(template_path)
        return None
        
    def save_template(self, region, name):
        """Save a region of screen as template image"""
        try:
            screenshot = self.capture_screen(region)
            if screenshot is not None:
                template_path = os.path.join(self.template_dir, f"{name}.png")
                cv2.imwrite(template_path, screenshot)
                return template_path
            return None
        except Exception as e:
            print(f"Save template error: {str(e)}")
            return None
            
    def calibrate_fishing_area(self, x, y, width=200, height=200):
        """Set the fishing area for focused detection"""
        self.capture_region = (x - width//2, y - height//2, width, height)
        
    def get_fishing_bobber_position(self):
        """Try to locate the fishing bobber automatically"""
        try:
            # Look for common bobber colors/shapes
            screenshot = self.capture_screen()
            if screenshot is None:
                return None
                
            # Convert to HSV
            hsv = cv2.cvtColor(screenshot, cv2.COLOR_BGR2HSV)
            
            # Define bobber color ranges (adjust based on game)
            bobber_colors = [
                ([0, 0, 200], [180, 30, 255]),    # White/bright bobber
                ([10, 100, 100], [25, 255, 255]), # Orange/red bobber
                ([35, 50, 50], [85, 255, 255])    # Green bobber
            ]
            
            for color_range in bobber_colors:
                lower_color = np.array(color_range[0])
                upper_color = np.array(color_range[1])
                mask = cv2.inRange(hsv, lower_color, upper_color)
                
                # Find contours
                contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
                
                for contour in contours:
                    area = cv2.contourArea(contour)
                    if 50 < area < 500:  # Reasonable bobber size
                        # Get center of contour
                        M = cv2.moments(contour)
                        if M["m00"] != 0:
                            cx = int(M["m10"] / M["m00"])
                            cy = int(M["m01"] / M["m00"])
                            return (cx, cy)
                            
            return None
            
        except Exception as e:
            print(f"Bobber detection error: {str(e)}")
            return None
            
    def debug_save_screenshot(self, name="debug"):
        """Save current screenshot for debugging"""
        try:
            screenshot = self.capture_screen()
            if screenshot is not None:
                debug_path = f"debug_{name}_{int(time.time())}.png"
                cv2.imwrite(debug_path, screenshot)
                return debug_path
            return None
        except Exception as e:
            print(f"Debug screenshot error: {str(e)}")
            return None
            
    def create_sample_templates(self):
        """Create sample template files for users to replace"""
        sample_templates = {
            "cast_button.png": "Cast/fishing button template",
            "bite_indicator.png": "Bite indicator template", 
            "bobber_splash.png": "Water splash when fish bites",
            "hook_icon.png": "Hook icon that appears on bite",
            "exclamation.png": "Exclamation mark bite indicator"
        }
        
        for filename, description in sample_templates.items():
            filepath = os.path.join(self.template_dir, filename)
            if not os.path.exists(filepath):
                # Create a placeholder image with text
                img = np.zeros((100, 200, 3), dtype=np.uint8)
                cv2.putText(img, "REPLACE", (20, 40), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 255), 2)
                cv2.putText(img, "WITH GAME", (20, 60), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 1)
                cv2.putText(img, "ELEMENT", (20, 80), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 1)
                cv2.imwrite(filepath, img)
                
        print(f"Template directory created at: {os.path.abspath(self.template_dir)}")
        print("Replace the template images with actual game elements for better detection!")

# Usage example and testing functions
if __name__ == "__main__":
    detector = ImageDetector()
    detector.create_sample_templates()
    
    # Test screen capture
    print("Testing screen capture...")
    screenshot = detector.capture_screen()
    if screenshot is not None:
        print(f"Screenshot captured: {screenshot.shape}")
    
    # Test bobber detection
    print("Testing bobber detection...")
    bobber_pos = detector.get_fishing_bobber_position()
    if bobber_pos:
        print(f"Potential bobber found at: {bobber_pos}")
    else:
        print("No bobber detected")
        
    print("Image detector module loaded successfully!")
