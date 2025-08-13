"""
Reel Timing Test Tool for Ragnarok X Auto Fishing Bot
Specialized tool for testing and calibrating the timing mini-game detection
"""

import tkinter as tk
from tkinter import ttk
import pyautogui
import cv2
import numpy as np
import time
import threading
from PIL import Image, ImageTk

class ReelTimingTester:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Reel Timing Detection Tester")
        self.root.geometry("600x500")
        
        self.is_monitoring = False
        self.timing_area = (400, 400)  # Default timing area
        self.detection_radius = 100
        self.green_threshold = 30
        
        self.setup_gui()
        
    def setup_gui(self):
        """Setup the testing GUI"""
        # Title
        title_label = ttk.Label(self.root, text="Reel Timing Detection Tester", 
                               font=("Arial", 14, "bold"))
        title_label.pack(pady=10)
        
        # Instructions
        instructions = """
This tool helps you calibrate the reel timing detection.
1. Set the timing area coordinates
2. Start monitoring
3. Trigger the reel mini-game in Ragnarok X
4. Observe the detection results
        """
        ttk.Label(self.root, text=instructions, justify=tk.CENTER).pack(pady=10)
        
        # Coordinates frame
        coord_frame = ttk.LabelFrame(self.root, text="Timing Area Setup", padding="10")
        coord_frame.pack(fill='x', padx=10, pady=10)
        
        ttk.Label(coord_frame, text="Timing Area X:").grid(row=0, column=0, sticky='w')
        self.timing_x_var = tk.IntVar(value=self.timing_area[0])
        ttk.Entry(coord_frame, textvariable=self.timing_x_var, width=10).grid(row=0, column=1, padx=5)
        
        ttk.Label(coord_frame, text="Timing Area Y:").grid(row=0, column=2, sticky='w', padx=(10, 0))
        self.timing_y_var = tk.IntVar(value=self.timing_area[1])
        ttk.Entry(coord_frame, textvariable=self.timing_y_var, width=10).grid(row=0, column=3, padx=5)
        
        ttk.Button(coord_frame, text="Detect Position", 
                  command=self.detect_timing_position).grid(row=0, column=4, padx=10)
        
        # Settings frame
        settings_frame = ttk.LabelFrame(self.root, text="Detection Settings", padding="10")
        settings_frame.pack(fill='x', padx=10, pady=10)
        
        ttk.Label(settings_frame, text="Detection Radius:").grid(row=0, column=0, sticky='w')
        self.radius_var = tk.IntVar(value=self.detection_radius)
        radius_scale = ttk.Scale(settings_frame, from_=50, to=200, variable=self.radius_var, 
                               orient='horizontal', length=200)
        radius_scale.grid(row=0, column=1, padx=5)
        self.radius_label = ttk.Label(settings_frame, text=f"{self.radius_var.get()}")
        self.radius_label.grid(row=0, column=2)
        radius_scale.configure(command=self.update_radius_label)
        
        ttk.Label(settings_frame, text="Green Threshold:").grid(row=1, column=0, sticky='w', pady=(5, 0))
        self.green_threshold_var = tk.IntVar(value=self.green_threshold)
        green_scale = ttk.Scale(settings_frame, from_=10, to=100, variable=self.green_threshold_var,
                              orient='horizontal', length=200)
        green_scale.grid(row=1, column=1, padx=5, pady=(5, 0))
        self.green_label = ttk.Label(settings_frame, text=f"{self.green_threshold_var.get()}")
        self.green_label.grid(row=1, column=2, pady=(5, 0))
        green_scale.configure(command=self.update_green_label)
        
        # Control frame
        control_frame = ttk.Frame(self.root)
        control_frame.pack(pady=20)
        
        self.start_button = ttk.Button(control_frame, text="Start Monitoring", 
                                     command=self.start_monitoring)
        self.start_button.pack(side='left', padx=5)
        
        self.stop_button = ttk.Button(control_frame, text="Stop Monitoring", 
                                    command=self.stop_monitoring, state='disabled')
        self.stop_button.pack(side='left', padx=5)
        
        ttk.Button(control_frame, text="Test Click", 
                  command=self.test_click).pack(side='left', padx=5)
        
        ttk.Button(control_frame, text="Save Screenshot", 
                  command=self.save_screenshot).pack(side='left', padx=5)
        
        # Results frame
        results_frame = ttk.LabelFrame(self.root, text="Detection Results", padding="10")
        results_frame.pack(fill='both', expand=True, padx=10, pady=10)
        
        # Status labels
        status_frame = ttk.Frame(results_frame)
        status_frame.pack(fill='x', pady=(0, 10))
        
        self.status_label = ttk.Label(status_frame, text="Status: Not monitoring", 
                                    font=("Arial", 10, "bold"))
        self.status_label.pack(anchor='w')
        
        self.detection_label = ttk.Label(status_frame, text="Mini-game: Not detected")
        self.detection_label.pack(anchor='w')
        
        self.timing_label = ttk.Label(status_frame, text="Perfect timing: No")
        self.timing_label.pack(anchor='w')
        
        self.color_info_label = ttk.Label(status_frame, text="Colors: Blue: 0%, White: 0%, Green: 0%")
        self.color_info_label.pack(anchor='w')
        
        # Log text
        self.log_text = tk.Text(results_frame, height=8, wrap='word')
        log_scrollbar = ttk.Scrollbar(results_frame, orient='vertical', command=self.log_text.yview)
        self.log_text.configure(yscrollcommand=log_scrollbar.set)
        
        self.log_text.pack(side='left', fill='both', expand=True)
        log_scrollbar.pack(side='right', fill='y')
        
    def update_radius_label(self, value):
        """Update radius label"""
        self.radius_label.configure(text=f"{int(float(value))}")
        self.detection_radius = int(float(value))
        
    def update_green_label(self, value):
        """Update green threshold label"""
        self.green_label.configure(text=f"{int(float(value))}")
        self.green_threshold = int(float(value))
        
    def detect_timing_position(self):
        """Detect timing position by mouse click"""
        self.log("Click on the center of timing circles in 3 seconds...")
        self.root.after(3000, self._get_timing_position)
        
    def _get_timing_position(self):
        """Get mouse position for timing area"""
        try:
            x, y = pyautogui.position()
            self.timing_x_var.set(x)
            self.timing_y_var.set(y)
            self.timing_area = (x, y)
            self.log(f"Timing area set to: ({x}, {y})")
        except Exception as e:
            self.log(f"Error detecting position: {str(e)}")
            
    def start_monitoring(self):
        """Start monitoring the timing area"""
        self.is_monitoring = True
        self.start_button.configure(state='disabled')
        self.stop_button.configure(state='normal')
        self.status_label.configure(text="Status: Monitoring...")
        
        # Start monitoring thread
        monitor_thread = threading.Thread(target=self.monitor_loop, daemon=True)
        monitor_thread.start()
        
        self.log("Started monitoring timing detection")
        
    def stop_monitoring(self):
        """Stop monitoring"""
        self.is_monitoring = False
        self.start_button.configure(state='normal')
        self.stop_button.configure(state='disabled')
        self.status_label.configure(text="Status: Not monitoring")
        
        self.log("Stopped monitoring")
        
    def monitor_loop(self):
        """Main monitoring loop"""
        while self.is_monitoring:
            try:
                # Update timing area from GUI
                self.timing_area = (self.timing_x_var.get(), self.timing_y_var.get())
                
                # Detect mini-game and timing
                minigame_active = self.detect_reel_minigame()
                perfect_timing = self.is_perfect_timing()
                
                # Update GUI in main thread
                self.root.after_idle(self.update_status, minigame_active, perfect_timing)
                
                # Check every 50ms for responsive detection
                time.sleep(0.05)
                
            except Exception as e:
                self.root.after_idle(self.log, f"Monitor error: {str(e)}")
                break
                
    def update_status(self, minigame_active, perfect_timing):
        """Update status labels"""
        self.detection_label.configure(
            text=f"Mini-game: {'DETECTED' if minigame_active else 'Not detected'}"
        )
        
        timing_text = "Perfect timing: "
        if perfect_timing:
            timing_text += "YES - REEL NOW!"
            self.timing_label.configure(text=timing_text, foreground='green')
        else:
            timing_text += "No"
            self.timing_label.configure(text=timing_text, foreground='black')
            
    def detect_reel_minigame(self):
        """Detect if reel mini-game is active"""
        try:
            timing_x, timing_y = self.timing_area
            radius = self.detection_radius
            
            # Capture timing area
            region = (timing_x - radius, timing_y - radius, radius * 2, radius * 2)
            screenshot = pyautogui.screenshot(region=region)
            screenshot_cv = cv2.cvtColor(np.array(screenshot), cv2.COLOR_RGB2BGR)
            
            # Convert to HSV
            hsv = cv2.cvtColor(screenshot_cv, cv2.COLOR_BGR2HSV)
            
            # Detect colors
            blue_lower = np.array([100, 50, 50])
            blue_upper = np.array([130, 255, 255])
            blue_mask = cv2.inRange(hsv, blue_lower, blue_upper)
            
            white_lower = np.array([0, 0, 200])
            white_upper = np.array([180, 30, 255])
            white_mask = cv2.inRange(hsv, white_lower, white_upper)
            
            green_lower = np.array([35, 50, 50])
            green_upper = np.array([85, 255, 255])
            green_mask = cv2.inRange(hsv, green_lower, green_upper)
            
            # Calculate percentages
            total_pixels = screenshot_cv.shape[0] * screenshot_cv.shape[1]
            blue_percentage = (np.sum(blue_mask > 0) / total_pixels) * 100
            white_percentage = (np.sum(white_mask > 0) / total_pixels) * 100
            green_percentage = (np.sum(green_mask > 0) / total_pixels) * 100
            
            # Update color info
            self.root.after_idle(
                lambda: self.color_info_label.configure(
                    text=f"Colors: Blue: {blue_percentage:.1f}%, White: {white_percentage:.1f}%, Green: {green_percentage:.1f}%"
                )
            )
            
            # Mini-game is active if we detect blue and white
            return blue_percentage > 2 and white_percentage > 2
            
        except Exception as e:
            return False
            
    def is_perfect_timing(self):
        """Check for perfect timing"""
        try:
            timing_x, timing_y = self.timing_area
            radius = self.detection_radius
            
            # Capture timing area
            region = (timing_x - radius, timing_y - radius, radius * 2, radius * 2)
            screenshot = pyautogui.screenshot(region=region)
            screenshot_cv = cv2.cvtColor(np.array(screenshot), cv2.COLOR_RGB2BGR)
            
            # Convert to HSV
            hsv = cv2.cvtColor(screenshot_cv, cv2.COLOR_BGR2HSV)
            
            # Look for green
            green_lower = np.array([35, 50, 50])
            green_upper = np.array([85, 255, 255])
            green_mask = cv2.inRange(hsv, green_lower, green_upper)
            
            green_pixels = np.sum(green_mask > 0)
            total_pixels = screenshot_cv.shape[0] * screenshot_cv.shape[1]
            green_percentage = (green_pixels / total_pixels) * 100
            
            # Perfect timing if green percentage exceeds threshold
            return green_percentage > (self.green_threshold / 10)  # Convert to percentage
            
        except Exception as e:
            return False
            
    def test_click(self):
        """Test clicking at timing area"""
        try:
            x, y = self.timing_area
            pyautogui.click(x, y)
            self.log(f"Test click performed at ({x}, {y})")
        except Exception as e:
            self.log(f"Test click error: {str(e)}")
            
    def save_screenshot(self):
        """Save screenshot of timing area"""
        try:
            timing_x, timing_y = self.timing_area
            radius = self.detection_radius
            
            region = (timing_x - radius, timing_y - radius, radius * 2, radius * 2)
            screenshot = pyautogui.screenshot(region=region)
            
            filename = f"timing_area_{int(time.time())}.png"
            screenshot.save(filename)
            self.log(f"Screenshot saved: {filename}")
            
        except Exception as e:
            self.log(f"Screenshot error: {str(e)}")
            
    def log(self, message):
        """Add message to log"""
        timestamp = time.strftime("%H:%M:%S")
        self.log_text.insert(tk.END, f"[{timestamp}] {message}\n")
        self.log_text.see(tk.END)
        
    def run(self):
        """Run the tester"""
        self.root.mainloop()

if __name__ == "__main__":
    tester = ReelTimingTester()
    tester.run()
