"""
Utility Scripts for Ragnarok X Auto Fishing Bot
Coordinate detection, screen calibration, and testing tools
"""

import tkinter as tk
from tkinter import ttk, messagebox
import pyautogui
import cv2
import numpy as np
from PIL import Image, ImageTk
import threading
import time
import os

class CoordinateDetector:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Coordinate Detection Tool")
        self.root.geometry("400x500")
        
        self.coordinates = {}
        self.is_detecting = False
        
        self.setup_gui()
        
    def setup_gui(self):
        """Setup the coordinate detection GUI"""
        # Title
        title_label = ttk.Label(self.root, text="Coordinate Detection Tool", 
                               font=("Arial", 14, "bold"))
        title_label.pack(pady=10)
        
        # Instructions
        instructions = """
Click the buttons below and then click on the
corresponding element in the game window.

Make sure the game window is visible!
        """
        
        ttk.Label(self.root, text=instructions, justify=tk.CENTER).pack(pady=10)
        
        # Detection buttons
        button_frame = ttk.Frame(self.root)
        button_frame.pack(pady=20)
        
        buttons = [
            ("Cast Button", "cast_button"),
            ("Fishing Area", "fishing_area"),
            ("Hook Button", "hook_button"),
            ("Inventory", "inventory"),
            ("Chat Window", "chat_window")
        ]
        
        for i, (text, key) in enumerate(buttons):
            btn = ttk.Button(button_frame, text=f"Detect {text}", 
                           command=lambda k=key: self.start_detection(k),
                           width=20)
            btn.pack(pady=5)
            
        # Results frame
        results_frame = ttk.LabelFrame(self.root, text="Detected Coordinates", padding="10")
        results_frame.pack(fill='both', expand=True, padx=10, pady=10)
        
        self.results_text = tk.Text(results_frame, height=10, width=40)
        scrollbar = ttk.Scrollbar(results_frame, orient="vertical", command=self.results_text.yview)
        self.results_text.configure(yscrollcommand=scrollbar.set)
        
        self.results_text.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
        
        # Control buttons
        control_frame = ttk.Frame(self.root)
        control_frame.pack(pady=10)
        
        ttk.Button(control_frame, text="Save Coordinates", 
                  command=self.save_coordinates).pack(side="left", padx=5)
        ttk.Button(control_frame, text="Load Coordinates", 
                  command=self.load_coordinates).pack(side="left", padx=5)
        ttk.Button(control_frame, text="Clear", 
                  command=self.clear_results).pack(side="left", padx=5)
        
    def start_detection(self, coord_type):
        """Start coordinate detection for specified type"""
        if self.is_detecting:
            return
            
        self.is_detecting = True
        self.update_results(f"Click on {coord_type.replace('_', ' ')} in 3 seconds...")
        
        # Schedule detection
        self.root.after(3000, lambda: self.detect_coordinate(coord_type))
        
    def detect_coordinate(self, coord_type):
        """Detect coordinate at current mouse position"""
        try:
            x, y = pyautogui.position()
            self.coordinates[coord_type] = (x, y)
            
            self.update_results(f"{coord_type}: ({x}, {y})")
            
        except Exception as e:
            self.update_results(f"Error detecting {coord_type}: {str(e)}")
        finally:
            self.is_detecting = False
            
    def update_results(self, text):
        """Update results display"""
        self.results_text.insert(tk.END, text + "\n")
        self.results_text.see(tk.END)
        
    def clear_results(self):
        """Clear results display"""
        self.results_text.delete(1.0, tk.END)
        self.coordinates.clear()
        
    def save_coordinates(self):
        """Save coordinates to file"""
        try:
            if not self.coordinates:
                messagebox.showwarning("Warning", "No coordinates to save!")
                return
                
            with open("detected_coordinates.txt", "w") as f:
                f.write("# Detected Coordinates for Ragnarok X Fishing Bot\n")
                f.write(f"# Generated: {time.strftime('%Y-%m-%d %H:%M:%S')}\n\n")
                
                for coord_type, (x, y) in self.coordinates.items():
                    f.write(f"{coord_type} = {x}, {y}\n")
                    
            messagebox.showinfo("Success", "Coordinates saved to detected_coordinates.txt!")
            
        except Exception as e:
            messagebox.showerror("Error", f"Failed to save coordinates: {str(e)}")
            
    def load_coordinates(self):
        """Load coordinates from file"""
        try:
            if not os.path.exists("detected_coordinates.txt"):
                messagebox.showwarning("Warning", "No coordinates file found!")
                return
                
            self.clear_results()
            
            with open("detected_coordinates.txt", "r") as f:
                for line in f:
                    line = line.strip()
                    if line and not line.startswith("#"):
                        if "=" in line:
                            coord_type, coords = line.split("=", 1)
                            coord_type = coord_type.strip()
                            
                            # Parse coordinates
                            coords = coords.strip().replace(" ", "")
                            x, y = map(int, coords.split(","))
                            
                            self.coordinates[coord_type] = (x, y)
                            self.update_results(f"{coord_type}: ({x}, {y})")
                            
            messagebox.showinfo("Success", "Coordinates loaded successfully!")
            
        except Exception as e:
            messagebox.showerror("Error", f"Failed to load coordinates: {str(e)}")
            
    def run(self):
        """Run the coordinate detector"""
        self.root.mainloop()

class ScreenCaptureTool:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Screen Capture Tool")
        self.root.geometry("500x400")
        
        self.setup_gui()
        
    def setup_gui(self):
        """Setup screen capture GUI"""
        title_label = ttk.Label(self.root, text="Screen Capture Tool", 
                               font=("Arial", 14, "bold"))
        title_label.pack(pady=10)
        
        # Capture options
        options_frame = ttk.LabelFrame(self.root, text="Capture Options", padding="10")
        options_frame.pack(fill='x', padx=10, pady=10)
        
        ttk.Button(options_frame, text="Capture Full Screen", 
                  command=self.capture_full_screen, width=20).pack(pady=5)
        ttk.Button(options_frame, text="Capture Game Window", 
                  command=self.capture_game_window, width=20).pack(pady=5)
        ttk.Button(options_frame, text="Capture Custom Region", 
                  command=self.capture_custom_region, width=20).pack(pady=5)
        
        # Template creation
        template_frame = ttk.LabelFrame(self.root, text="Template Creation", padding="10")
        template_frame.pack(fill='x', padx=10, pady=10)
        
        ttk.Label(template_frame, text="Template Name:").pack(anchor='w')
        self.template_name_var = tk.StringVar()
        ttk.Entry(template_frame, textvariable=self.template_name_var, width=30).pack(pady=5)
        
        ttk.Button(template_frame, text="Create Template from Region", 
                  command=self.create_template, width=25).pack(pady=5)
        
        # Log
        log_frame = ttk.LabelFrame(self.root, text="Log", padding="10")
        log_frame.pack(fill='both', expand=True, padx=10, pady=10)
        
        self.log_text = tk.Text(log_frame, height=8)
        log_scrollbar = ttk.Scrollbar(log_frame, orient="vertical", command=self.log_text.yview)
        self.log_text.configure(yscrollcommand=log_scrollbar.set)
        
        self.log_text.pack(side="left", fill="both", expand=True)
        log_scrollbar.pack(side="right", fill="y")
        
    def log(self, message):
        """Add message to log"""
        timestamp = time.strftime("%H:%M:%S")
        self.log_text.insert(tk.END, f"[{timestamp}] {message}\n")
        self.log_text.see(tk.END)
        
    def capture_full_screen(self):
        """Capture full screen"""
        try:
            screenshot = pyautogui.screenshot()
            filename = f"fullscreen_{int(time.time())}.png"
            screenshot.save(filename)
            self.log(f"Full screen captured: {filename}")
        except Exception as e:
            self.log(f"Error capturing full screen: {str(e)}")
            
    def capture_game_window(self):
        """Attempt to capture game window"""
        try:
            # Try to find Ragnarok X window
            windows = pyautogui.getWindowsWithTitle("Ragnarok")
            if not windows:
                windows = pyautogui.getWindowsWithTitle("ROX")
                
            if windows:
                window = windows[0]
                screenshot = pyautogui.screenshot(region=(window.left, window.top, 
                                                        window.width, window.height))
                filename = f"gamewindow_{int(time.time())}.png"
                screenshot.save(filename)
                self.log(f"Game window captured: {filename}")
            else:
                self.log("Game window not found. Try full screen capture instead.")
                
        except Exception as e:
            self.log(f"Error capturing game window: {str(e)}")
            
    def capture_custom_region(self):
        """Capture custom region using mouse selection"""
        self.log("Click and drag to select region in 3 seconds...")
        self.root.after(3000, self._capture_region_helper)
        
    def _capture_region_helper(self):
        """Helper for custom region capture"""
        try:
            self.log("Click top-left corner of region...")
            self.root.after(2000, self._get_first_point)
        except Exception as e:
            self.log(f"Error in region capture: {str(e)}")
            
    def _get_first_point(self):
        """Get first point of region"""
        try:
            self.first_point = pyautogui.position()
            self.log(f"First point: {self.first_point}")
            self.log("Now click bottom-right corner...")
            self.root.after(2000, self._get_second_point)
        except Exception as e:
            self.log(f"Error getting first point: {str(e)}")
            
    def _get_second_point(self):
        """Get second point and capture region"""
        try:
            second_point = pyautogui.position()
            self.log(f"Second point: {second_point}")
            
            # Calculate region
            x1, y1 = self.first_point
            x2, y2 = second_point
            
            left = min(x1, x2)
            top = min(y1, y2)
            width = abs(x2 - x1)
            height = abs(y2 - y1)
            
            # Capture region
            screenshot = pyautogui.screenshot(region=(left, top, width, height))
            filename = f"region_{int(time.time())}.png"
            screenshot.save(filename)
            self.log(f"Region captured: {filename} ({width}x{height})")
            
        except Exception as e:
            self.log(f"Error getting second point: {str(e)}")
            
    def create_template(self):
        """Create template from captured region"""
        try:
            template_name = self.template_name_var.get().strip()
            if not template_name:
                self.log("Please enter a template name")
                return
                
            self.log(f"Creating template '{template_name}' in 3 seconds...")
            self.log("Click top-left corner of template area...")
            self.root.after(3000, lambda: self._create_template_helper(template_name))
            
        except Exception as e:
            self.log(f"Error creating template: {str(e)}")
            
    def _create_template_helper(self, template_name):
        """Helper for template creation"""
        try:
            self.template_first_point = pyautogui.position()
            self.log(f"First point: {self.template_first_point}")
            self.log("Now click bottom-right corner...")
            self.root.after(2000, lambda: self._finish_template(template_name))
        except Exception as e:
            self.log(f"Error in template creation: {str(e)}")
            
    def _finish_template(self, template_name):
        """Finish template creation"""
        try:
            second_point = pyautogui.position()
            self.log(f"Second point: {second_point}")
            
            # Calculate region
            x1, y1 = self.template_first_point
            x2, y2 = second_point
            
            left = min(x1, x2)
            top = min(y1, y2)
            width = abs(x2 - x1)
            height = abs(y2 - y1)
            
            # Capture template
            screenshot = pyautogui.screenshot(region=(left, top, width, height))
            
            # Ensure templates directory exists
            os.makedirs("templates", exist_ok=True)
            
            filename = f"templates/{template_name}.png"
            screenshot.save(filename)
            self.log(f"Template created: {filename}")
            
        except Exception as e:
            self.log(f"Error finishing template: {str(e)}")
            
    def run(self):
        """Run the screen capture tool"""
        self.root.mainloop()

class TestingTool:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Bot Testing Tool")
        self.root.geometry("600x500")
        
        self.setup_gui()
        
    def setup_gui(self):
        """Setup testing GUI"""
        title_label = ttk.Label(self.root, text="Bot Testing Tool", 
                               font=("Arial", 14, "bold"))
        title_label.pack(pady=10)
        
        # Test buttons
        test_frame = ttk.LabelFrame(self.root, text="Tests", padding="10")
        test_frame.pack(fill='x', padx=10, pady=10)
        
        tests = [
            ("Test Click Accuracy", self.test_click_accuracy),
            ("Test Image Detection", self.test_image_detection),
            ("Test Motion Detection", self.test_motion_detection),
            ("Test Color Detection", self.test_color_detection),
            ("Test Timing", self.test_timing),
            ("Test Screen Capture", self.test_screen_capture)
        ]
        
        for text, command in tests:
            ttk.Button(test_frame, text=text, command=command, width=25).pack(pady=2)
            
        # Results
        results_frame = ttk.LabelFrame(self.root, text="Test Results", padding="10")
        results_frame.pack(fill='both', expand=True, padx=10, pady=10)
        
        self.results_text = tk.Text(results_frame, height=15)
        results_scrollbar = ttk.Scrollbar(results_frame, orient="vertical", command=self.results_text.yview)
        self.results_text.configure(yscrollcommand=results_scrollbar.set)
        
        self.results_text.pack(side="left", fill="both", expand=True)
        results_scrollbar.pack(side="right", fill="y")
        
        # Control buttons
        control_frame = ttk.Frame(self.root)
        control_frame.pack(pady=10)
        
        ttk.Button(control_frame, text="Clear Results", 
                  command=self.clear_results).pack(side="left", padx=5)
        ttk.Button(control_frame, text="Save Results", 
                  command=self.save_results).pack(side="left", padx=5)
        
    def log(self, message):
        """Add message to results"""
        timestamp = time.strftime("%H:%M:%S")
        self.results_text.insert(tk.END, f"[{timestamp}] {message}\n")
        self.results_text.see(tk.END)
        self.root.update()
        
    def test_click_accuracy(self):
        """Test click accuracy"""
        self.log("=== Click Accuracy Test ===")
        self.log("Testing click precision...")
        
        try:
            # Test multiple clicks
            for i in range(5):
                x, y = 400 + i * 10, 300 + i * 10
                start_time = time.time()
                pyautogui.click(x, y)
                click_time = time.time() - start_time
                
                # Verify position
                actual_x, actual_y = pyautogui.position()
                self.log(f"Click {i+1}: Target({x},{y}) -> Actual({actual_x},{actual_y}) Time: {click_time:.3f}s")
                
                time.sleep(0.5)
                
            self.log("Click accuracy test completed")
            
        except Exception as e:
            self.log(f"Click test error: {str(e)}")
            
    def test_image_detection(self):
        """Test image detection capabilities"""
        self.log("=== Image Detection Test ===")
        
        try:
            # Take screenshot for testing
            screenshot = pyautogui.screenshot()
            self.log(f"Screenshot captured: {screenshot.size}")
            
            # Convert to OpenCV format
            screenshot_cv = cv2.cvtColor(np.array(screenshot), cv2.COLOR_RGB2BGR)
            
            # Test template matching with a small region
            height, width = screenshot_cv.shape[:2]
            template = screenshot_cv[100:150, 100:150]  # 50x50 template
            
            result = cv2.matchTemplate(screenshot_cv, template, cv2.TM_CCOEFF_NORMED)
            min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(result)
            
            self.log(f"Template matching confidence: {max_val:.3f}")
            self.log(f"Best match location: {max_loc}")
            
            if max_val > 0.8:
                self.log("Image detection working correctly")
            else:
                self.log("Image detection may need adjustment")
                
        except Exception as e:
            self.log(f"Image detection test error: {str(e)}")
            
    def test_motion_detection(self):
        """Test motion detection"""
        self.log("=== Motion Detection Test ===")
        self.log("Move your mouse to test motion detection...")
        
        try:
            # Capture baseline
            region = (400, 300, 200, 200)  # Test region
            screenshot1 = pyautogui.screenshot(region=region)
            
            time.sleep(2)  # Wait for movement
            
            # Capture after movement
            screenshot2 = pyautogui.screenshot(region=region)
            
            # Convert to grayscale
            gray1 = cv2.cvtColor(np.array(screenshot1), cv2.COLOR_RGB2GRAY)
            gray2 = cv2.cvtColor(np.array(screenshot2), cv2.COLOR_RGB2GRAY)
            
            # Calculate difference
            diff = cv2.absdiff(gray1, gray2)
            _, thresh = cv2.threshold(diff, 30, 255, cv2.THRESH_BINARY)
            
            motion_pixels = np.sum(thresh > 0)
            total_pixels = thresh.shape[0] * thresh.shape[1]
            motion_percentage = (motion_pixels / total_pixels) * 100
            
            self.log(f"Motion detected: {motion_percentage:.2f}% of pixels changed")
            
            if motion_percentage > 1:
                self.log("Motion detection working")
            else:
                self.log("No significant motion detected")
                
        except Exception as e:
            self.log(f"Motion detection test error: {str(e)}")
            
    def test_color_detection(self):
        """Test color detection"""
        self.log("=== Color Detection Test ===")
        
        try:
            # Capture screen
            screenshot = pyautogui.screenshot(region=(400, 300, 100, 100))
            screenshot_cv = cv2.cvtColor(np.array(screenshot), cv2.COLOR_RGB2BGR)
            
            # Convert to HSV
            hsv = cv2.cvtColor(screenshot_cv, cv2.COLOR_BGR2HSV)
            
            # Test for common colors
            color_ranges = {
                'Blue': ([100, 50, 50], [130, 255, 255]),
                'Red': ([0, 50, 50], [10, 255, 255]),
                'Green': ([35, 50, 50], [85, 255, 255]),
                'White': ([0, 0, 200], [180, 30, 255])
            }
            
            for color_name, (lower, upper) in color_ranges.items():
                lower_np = np.array(lower)
                upper_np = np.array(upper)
                
                mask = cv2.inRange(hsv, lower_np, upper_np)
                percentage = (np.sum(mask > 0) / mask.size) * 100
                
                self.log(f"{color_name}: {percentage:.2f}% of region")
                
        except Exception as e:
            self.log(f"Color detection test error: {str(e)}")
            
    def test_timing(self):
        """Test timing accuracy"""
        self.log("=== Timing Test ===")
        
        try:
            delays = [0.1, 0.5, 1.0, 2.0]
            
            for delay in delays:
                start_time = time.time()
                time.sleep(delay)
                actual_delay = time.time() - start_time
                error = abs(actual_delay - delay)
                
                self.log(f"Target: {delay}s, Actual: {actual_delay:.3f}s, Error: {error:.3f}s")
                
        except Exception as e:
            self.log(f"Timing test error: {str(e)}")
            
    def test_screen_capture(self):
        """Test screen capture performance"""
        self.log("=== Screen Capture Test ===")
        
        try:
            capture_times = []
            
            for i in range(10):
                start_time = time.time()
                screenshot = pyautogui.screenshot()
                capture_time = time.time() - start_time
                capture_times.append(capture_time)
                
                self.log(f"Capture {i+1}: {capture_time:.3f}s ({screenshot.size})")
                
            avg_time = sum(capture_times) / len(capture_times)
            self.log(f"Average capture time: {avg_time:.3f}s")
            
            if avg_time < 0.1:
                self.log("Screen capture performance: Excellent")
            elif avg_time < 0.2:
                self.log("Screen capture performance: Good")
            else:
                self.log("Screen capture performance: Needs improvement")
                
        except Exception as e:
            self.log(f"Screen capture test error: {str(e)}")
            
    def clear_results(self):
        """Clear test results"""
        self.results_text.delete(1.0, tk.END)
        
    def save_results(self):
        """Save test results"""
        try:
            results = self.results_text.get(1.0, tk.END)
            filename = f"test_results_{int(time.time())}.txt"
            
            with open(filename, 'w') as f:
                f.write(results)
                
            self.log(f"Results saved to {filename}")
            
        except Exception as e:
            self.log(f"Error saving results: {str(e)}")
            
    def run(self):
        """Run the testing tool"""
        self.root.mainloop()

if __name__ == "__main__":
    import sys
    
    if len(sys.argv) > 1:
        tool = sys.argv[1].lower()
    else:
        print("Available tools:")
        print("1. coordinate - Coordinate Detection Tool")
        print("2. capture - Screen Capture Tool") 
        print("3. test - Testing Tool")
        tool = input("Select tool (1-3): ").strip()
        
    if tool in ['1', 'coordinate']:
        detector = CoordinateDetector()
        detector.run()
    elif tool in ['2', 'capture']:
        capture_tool = ScreenCaptureTool()
        capture_tool.run()
    elif tool in ['3', 'test']:
        testing_tool = TestingTool()
        testing_tool.run()
    else:
        print("Invalid selection. Please run with 'coordinate', 'capture', or 'test'")
