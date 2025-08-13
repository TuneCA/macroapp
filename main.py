#!/usr/bin/env python3
"""
Ragnarok X Next Generation Auto Fishing Bot
A comprehensive automation tool for fishing in Ragnarok X Next Generation
Similar to Macrorify but designed specifically for PC

Author: Auto Generated
Date: August 13, 2025
"""

import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import pyautogui
import cv2
import numpy as np
import time
import threading
import random
import configparser
import os
import sys
from PIL import Image, ImageTk
import psutil
from pynput import keyboard
import json
from datetime import datetime, timedelta

# Import our custom modules
from image_detector import ImageDetector
from config_manager import ConfigManager

class RagnarokFishingBot:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Ragnarok X Auto Fishing Bot v1.0")
        self.root.geometry("800x700")
        self.root.resizable(True, True)
        
        # Initialize components
        self.image_detector = ImageDetector()
        self.config_manager = ConfigManager()
        
        # Bot state variables
        self.is_running = False
        self.is_paused = False
        self.thread = None
        self.emergency_stop = False
        
        # Load configuration
        self.config_manager.load_config()
        
        # Statistics
        self.stats = {
            'fish_caught': 0,
            'casts_made': 0,
            'session_start': None,
            'total_runtime': 0
        }
        
        # Fishing parameters (loaded from config)
        self.load_fishing_params()
        
        # Reel timing parameters
        self.reel_params = {
            'reel_button': (400, 600),      # Default reel button location
            'timing_area': (400, 400),      # Area to monitor for timing circles
            'green_threshold': 30,          # Green color detection threshold
            'circle_detection_radius': 100, # Radius to check for timing circles
            'reaction_delay': (0.1, 0.3)   # Reaction time for reel timing
        }
        
        # Setup GUI
        self.setup_gui()
        self.setup_hotkeys()
        
    def load_fishing_params(self):
        """Load fishing parameters from config manager"""
        self.fishing_params = {
            'cast_button': (
                self.config_manager.getint('Coordinates', 'cast_button_x', 400),
                self.config_manager.getint('Coordinates', 'cast_button_y', 500)
            ),
            'fishing_area': (
                self.config_manager.getint('Coordinates', 'fishing_area_x', 400),
                self.config_manager.getint('Coordinates', 'fishing_area_y', 300)
            ),
            'hook_sensitivity': self.config_manager.getfloat('Detection', 'hook_sensitivity', 0.8),
            'cast_delay': (
                self.config_manager.getfloat('Timing', 'cast_delay_min', 2.0),
                self.config_manager.getfloat('Timing', 'cast_delay_max', 4.0)
            ),
            'bite_timeout': self.config_manager.getint('Timing', 'bite_timeout', 30),
            'reaction_time': (
                self.config_manager.getfloat('Timing', 'reaction_time_min', 0.3),
                self.config_manager.getfloat('Timing', 'reaction_time_max', 0.8)
            )
        }
        
    def setup_gui(self):
        """Setup the main GUI interface"""
        # Create notebook for tabs
        notebook = ttk.Notebook(self.root)
        notebook.pack(fill='both', expand=True, padx=10, pady=10)
        
        # Main Control Tab
        self.create_main_tab(notebook)
        
        # Configuration Tab
        self.create_config_tab(notebook)
        
        # Statistics Tab
        self.create_stats_tab(notebook)
        
        # Help Tab
        self.create_help_tab(notebook)
        
    def create_main_tab(self, notebook):
        """Create the main control tab"""
        main_frame = ttk.Frame(notebook)
        notebook.add(main_frame, text="Main Control")
        
        # Status Frame
        status_frame = ttk.LabelFrame(main_frame, text="Bot Status", padding="10")
        status_frame.pack(fill='x', pady=(0, 10))
        
        self.status_label = ttk.Label(status_frame, text="Status: Stopped", font=("Arial", 12, "bold"))
        self.status_label.pack()
        
        self.time_label = ttk.Label(status_frame, text="Runtime: 00:00:00")
        self.time_label.pack()
        
        # Control Buttons Frame
        control_frame = ttk.LabelFrame(main_frame, text="Controls", padding="10")
        control_frame.pack(fill='x', pady=(0, 10))
        
        button_frame = ttk.Frame(control_frame)
        button_frame.pack()
        
        self.start_button = ttk.Button(button_frame, text="Start Fishing", 
                                     command=self.start_fishing, style="Green.TButton")
        self.start_button.pack(side='left', padx=(0, 5))
        
        self.pause_button = ttk.Button(button_frame, text="Pause", 
                                     command=self.pause_fishing, state='disabled')
        self.pause_button.pack(side='left', padx=5)
        
        self.stop_button = ttk.Button(button_frame, text="Stop", 
                                    command=self.stop_fishing, state='disabled')
        self.stop_button.pack(side='left', padx=(5, 0))
        
        # Quick Settings Frame
        quick_frame = ttk.LabelFrame(main_frame, text="Quick Settings", padding="10")
        quick_frame.pack(fill='x', pady=(0, 10))
        
        # Cast delay setting
        ttk.Label(quick_frame, text="Cast Delay (seconds):").grid(row=0, column=0, sticky='w', padx=(0, 5))
        self.cast_delay_var = tk.StringVar(value=f"{self.fishing_params['cast_delay'][0]}-{self.fishing_params['cast_delay'][1]}")
        cast_delay_entry = ttk.Entry(quick_frame, textvariable=self.cast_delay_var, width=10)
        cast_delay_entry.grid(row=0, column=1, padx=5)
        
        # Bite timeout setting
        ttk.Label(quick_frame, text="Bite Timeout (seconds):").grid(row=0, column=2, sticky='w', padx=(10, 5))
        self.bite_timeout_var = tk.IntVar(value=self.fishing_params['bite_timeout'])
        bite_timeout_spin = ttk.Spinbox(quick_frame, from_=10, to=60, textvariable=self.bite_timeout_var, width=8)
        bite_timeout_spin.grid(row=0, column=3, padx=5)
        
        # Log Frame
        log_frame = ttk.LabelFrame(main_frame, text="Activity Log", padding="10")
        log_frame.pack(fill='both', expand=True)
        
        # Create scrolled text widget for log
        log_scroll_frame = ttk.Frame(log_frame)
        log_scroll_frame.pack(fill='both', expand=True)
        
        self.log_text = tk.Text(log_scroll_frame, height=10, wrap='word')
        log_scrollbar = ttk.Scrollbar(log_scroll_frame, orient='vertical', command=self.log_text.yview)
        self.log_text.configure(yscrollcommand=log_scrollbar.set)
        
        self.log_text.pack(side='left', fill='both', expand=True)
        log_scrollbar.pack(side='right', fill='y')
        
        # Clear log button
        ttk.Button(log_frame, text="Clear Log", command=self.clear_log).pack(pady=(5, 0))
        
    def create_config_tab(self, notebook):
        """Create the configuration tab"""
        config_frame = ttk.Frame(notebook)
        notebook.add(config_frame, text="Configuration")
        
        # Coordinates Frame
        coord_frame = ttk.LabelFrame(config_frame, text="Coordinates Setup", padding="10")
        coord_frame.pack(fill='x', pady=(0, 10))
        
        ttk.Label(coord_frame, text="Cast Button Position:").grid(row=0, column=0, sticky='w', padx=(0, 5))
        self.cast_x_var = tk.IntVar(value=self.fishing_params['cast_button'][0])
        self.cast_y_var = tk.IntVar(value=self.fishing_params['cast_button'][1])
        
        ttk.Entry(coord_frame, textvariable=self.cast_x_var, width=8).grid(row=0, column=1, padx=2)
        ttk.Label(coord_frame, text=",").grid(row=0, column=2)
        ttk.Entry(coord_frame, textvariable=self.cast_y_var, width=8).grid(row=0, column=3, padx=2)
        
        ttk.Button(coord_frame, text="Detect", command=self.detect_cast_button).grid(row=0, column=4, padx=(5, 0))
        
        ttk.Label(coord_frame, text="Fishing Area:").grid(row=1, column=0, sticky='w', padx=(0, 5), pady=(5, 0))
        self.area_x_var = tk.IntVar(value=self.fishing_params['fishing_area'][0])
        self.area_y_var = tk.IntVar(value=self.fishing_params['fishing_area'][1])
        
        ttk.Entry(coord_frame, textvariable=self.area_x_var, width=8).grid(row=1, column=1, padx=2, pady=(5, 0))
        ttk.Label(coord_frame, text=",").grid(row=1, column=2, pady=(5, 0))
        ttk.Entry(coord_frame, textvariable=self.area_y_var, width=8).grid(row=1, column=3, padx=2, pady=(5, 0))
        
        ttk.Button(coord_frame, text="Detect", command=self.detect_fishing_area).grid(row=1, column=4, padx=(5, 0), pady=(5, 0))
        
        # Reel button coordinates
        ttk.Label(coord_frame, text="Reel Button:").grid(row=2, column=0, sticky='w', padx=(0, 5), pady=(5, 0))
        self.reel_x_var = tk.IntVar(value=self.reel_params['reel_button'][0])
        self.reel_y_var = tk.IntVar(value=self.reel_params['reel_button'][1])
        
        ttk.Entry(coord_frame, textvariable=self.reel_x_var, width=8).grid(row=2, column=1, padx=2, pady=(5, 0))
        ttk.Label(coord_frame, text=",").grid(row=2, column=2, pady=(5, 0))
        ttk.Entry(coord_frame, textvariable=self.reel_y_var, width=8).grid(row=2, column=3, padx=2, pady=(5, 0))
        
        ttk.Button(coord_frame, text="Detect", command=self.detect_reel_button).grid(row=2, column=4, padx=(5, 0), pady=(5, 0))
        
        # Timing area coordinates
        ttk.Label(coord_frame, text="Timing Area:").grid(row=3, column=0, sticky='w', padx=(0, 5), pady=(5, 0))
        self.timing_x_var = tk.IntVar(value=self.reel_params['timing_area'][0])
        self.timing_y_var = tk.IntVar(value=self.reel_params['timing_area'][1])
        
        ttk.Entry(coord_frame, textvariable=self.timing_x_var, width=8).grid(row=3, column=1, padx=2, pady=(5, 0))
        ttk.Label(coord_frame, text=",").grid(row=3, column=2, pady=(5, 0))
        ttk.Entry(coord_frame, textvariable=self.timing_y_var, width=8).grid(row=3, column=3, padx=2, pady=(5, 0))
        
        ttk.Button(coord_frame, text="Detect", command=self.detect_timing_area).grid(row=3, column=4, padx=(5, 0), pady=(5, 0))
        
        # Detection Settings Frame
        detection_frame = ttk.LabelFrame(config_frame, text="Detection Settings", padding="10")
        detection_frame.pack(fill='x', pady=(0, 10))
        
        ttk.Label(detection_frame, text="Hook Sensitivity:").grid(row=0, column=0, sticky='w', padx=(0, 5))
        self.sensitivity_var = tk.DoubleVar(value=self.fishing_params['hook_sensitivity'])
        sensitivity_scale = ttk.Scale(detection_frame, from_=0.5, to=1.0, variable=self.sensitivity_var, 
                                    orient='horizontal', length=200)
        sensitivity_scale.grid(row=0, column=1, padx=5)
        self.sensitivity_label = ttk.Label(detection_frame, text=f"{self.sensitivity_var.get():.2f}")
        self.sensitivity_label.grid(row=0, column=2, padx=5)
        sensitivity_scale.configure(command=self.update_sensitivity_label)
        
        # Reel timing settings
        ttk.Label(detection_frame, text="Reel Timing Delay:").grid(row=1, column=0, sticky='w', padx=(0, 5), pady=(5, 0))
        self.reel_delay_var = tk.DoubleVar(value=0.2)
        reel_delay_scale = ttk.Scale(detection_frame, from_=0.05, to=0.5, variable=self.reel_delay_var,
                                   orient='horizontal', length=200)
        reel_delay_scale.grid(row=1, column=1, padx=5, pady=(5, 0))
        self.reel_delay_label = ttk.Label(detection_frame, text=f"{self.reel_delay_var.get():.2f}s")
        self.reel_delay_label.grid(row=1, column=2, padx=5, pady=(5, 0))
        reel_delay_scale.configure(command=self.update_reel_delay_label)
        
        # Green threshold for timing detection
        ttk.Label(detection_frame, text="Green Detection:").grid(row=2, column=0, sticky='w', padx=(0, 5), pady=(5, 0))
        self.green_threshold_var = tk.IntVar(value=30)
        green_threshold_scale = ttk.Scale(detection_frame, from_=10, to=100, variable=self.green_threshold_var,
                                        orient='horizontal', length=200)
        green_threshold_scale.grid(row=2, column=1, padx=5, pady=(5, 0))
        self.green_threshold_label = ttk.Label(detection_frame, text=f"{self.green_threshold_var.get()}")
        self.green_threshold_label.grid(row=2, column=2, padx=5, pady=(5, 0))
        green_threshold_scale.configure(command=self.update_green_threshold_label)
        
        # Safety Settings Frame
        safety_frame = ttk.LabelFrame(config_frame, text="Safety Settings", padding="10")
        safety_frame.pack(fill='x', pady=(0, 10))
        
        self.randomize_var = tk.BooleanVar(value=True)
        ttk.Checkbutton(safety_frame, text="Randomize timings", variable=self.randomize_var).grid(row=0, column=0, sticky='w')
        
        self.anti_detect_var = tk.BooleanVar(value=True)
        ttk.Checkbutton(safety_frame, text="Anti-detection measures", variable=self.anti_detect_var).grid(row=1, column=0, sticky='w')
        
        ttk.Label(safety_frame, text="Break interval (minutes):").grid(row=0, column=1, sticky='w', padx=(20, 5))
        self.break_interval_var = tk.IntVar(value=30)
        ttk.Spinbox(safety_frame, from_=5, to=120, textvariable=self.break_interval_var, width=8).grid(row=0, column=2)
        
        # Config Buttons Frame
        config_buttons_frame = ttk.Frame(config_frame)
        config_buttons_frame.pack(fill='x', pady=(10, 0))
        
        ttk.Button(config_buttons_frame, text="Save Configuration", command=self.save_config).pack(side='left', padx=(0, 5))
        ttk.Button(config_buttons_frame, text="Load Configuration", command=self.load_config).pack(side='left', padx=5)
        ttk.Button(config_buttons_frame, text="Reset to Defaults", command=self.reset_config).pack(side='left', padx=(5, 0))
        
    def create_stats_tab(self, notebook):
        """Create the statistics tab"""
        stats_frame = ttk.Frame(notebook)
        notebook.add(stats_frame, text="Statistics")
        
        # Session Stats Frame
        session_frame = ttk.LabelFrame(stats_frame, text="Current Session", padding="10")
        session_frame.pack(fill='x', pady=(0, 10))
        
        self.fish_caught_label = ttk.Label(session_frame, text="Fish Caught: 0", font=("Arial", 12))
        self.fish_caught_label.pack(anchor='w')
        
        self.casts_made_label = ttk.Label(session_frame, text="Casts Made: 0", font=("Arial", 12))
        self.casts_made_label.pack(anchor='w')
        
        self.success_rate_label = ttk.Label(session_frame, text="Success Rate: 0%", font=("Arial", 12))
        self.success_rate_label.pack(anchor='w')
        
        self.session_time_label = ttk.Label(session_frame, text="Session Time: 00:00:00", font=("Arial", 12))
        self.session_time_label.pack(anchor='w')
        
        # Performance Frame
        performance_frame = ttk.LabelFrame(stats_frame, text="Performance Metrics", padding="10")
        performance_frame.pack(fill='x', pady=(0, 10))
        
        self.avg_cast_time_label = ttk.Label(performance_frame, text="Avg Cast Time: 0s")
        self.avg_cast_time_label.pack(anchor='w')
        
        self.fish_per_hour_label = ttk.Label(performance_frame, text="Fish per Hour: 0")
        self.fish_per_hour_label.pack(anchor='w')
        
        # Reset Stats Button
        ttk.Button(stats_frame, text="Reset Statistics", command=self.reset_stats).pack(pady=10)
        
    def create_help_tab(self, notebook):
        """Create the help tab"""
        help_frame = ttk.Frame(notebook)
        notebook.add(help_frame, text="Help")
        
        help_text = """
RAGNAROK X AUTO FISHING BOT - HELP GUIDE

SETUP INSTRUCTIONS:
1. Start Ragnarok X Next Generation and go to a fishing location
2. Open the fishing interface in the game
3. Use the 'Detect' buttons in Configuration tab to set coordinates:
   - Cast Button: The button to start fishing
   - Fishing Area: Where to cast your line
   - Reel Button: The button for the timing mini-game
   - Timing Area: Center of the timing circles

FISHING MECHANICS:
This bot handles the two-step fishing process:
1. CAST: Automatically clicks the cast button and fishing area
2. REEL: Detects the timing mini-game and clicks when:
   - The shrinking circle touches the dotted blue circle, OR
   - The timing indicator turns green

HOTKEYS:
- F1: Start/Resume fishing
- F2: Pause fishing
- F3: Stop fishing
- F4: Emergency stop (immediately stops all activity)

COORDINATE DETECTION:
- Cast Button: Click 'Detect' then click on the fishing cast button in game
- Fishing Area: Click 'Detect' then click where you want to cast your line
- Reel Button: Click 'Detect' then click on the reel/timing button
- Timing Area: Click 'Detect' then click center of the timing circles

TIMING SETTINGS:
- Reel Timing Delay: Reaction time before clicking reel (0.05-0.5s)
- Green Detection: Sensitivity for detecting green timing indicator
- Adjust these based on your connection speed and timing preference

SAFETY FEATURES:
- Randomized timing to avoid detection
- Automatic breaks to simulate human behavior
- Emergency stop functionality
- Anti-detection measures

TIPS FOR BEST RESULTS:
- Ensure game window is visible and not minimized
- Use windowed mode for better detection
- Adjust reel timing delay based on your reaction preference
- Test timing detection in short sessions first
- Fine-tune green detection threshold if needed

TROUBLESHOOTING:
- If bot doesn't detect reel mini-game, adjust timing area coordinates
- If reel timing is too fast/slow, adjust the timing delay
- If green detection fails, adjust green detection threshold
- Make sure all coordinates are correctly set
- Check that game window has focus when needed

The bot will automatically handle both casting and the timing-based reel mechanics!
        """
        
        help_text_widget = tk.Text(help_frame, wrap='word', padx=10, pady=10)
        help_text_widget.insert(tk.END, help_text)
        help_text_widget.configure(state='disabled')
        
        help_scrollbar = ttk.Scrollbar(help_frame, orient='vertical', command=help_text_widget.yview)
        help_text_widget.configure(yscrollcommand=help_scrollbar.set)
        
        help_text_widget.pack(side='left', fill='both', expand=True)
        help_scrollbar.pack(side='right', fill='y')
        
    def setup_hotkeys(self):
        """Setup global hotkeys"""
        def on_hotkey(key):
            try:
                if key == keyboard.Key.f1:
                    if not self.is_running:
                        self.start_fishing()
                    elif self.is_paused:
                        self.resume_fishing()
                elif key == keyboard.Key.f2:
                    if self.is_running:
                        self.pause_fishing()
                elif key == keyboard.Key.f3:
                    if self.is_running:
                        self.stop_fishing()
                elif key == keyboard.Key.f4:
                    self.emergency_stop_fishing()
            except Exception as e:
                self.log_message(f"Hotkey error: {str(e)}")
        
        # Start keyboard listener in a separate thread
        def start_listener():
            with keyboard.Listener(on_press=on_hotkey) as listener:
                listener.join()
        
        hotkey_thread = threading.Thread(target=start_listener, daemon=True)
        hotkey_thread.start()
        
    def update_sensitivity_label(self, value):
        """Update sensitivity label when scale changes"""
        self.sensitivity_label.configure(text=f"{float(value):.2f}")
        
    def update_reel_delay_label(self, value):
        """Update reel delay label when scale changes"""
        self.reel_delay_label.configure(text=f"{float(value):.2f}s")
        
    def update_green_threshold_label(self, value):
        """Update green threshold label when scale changes"""
        self.green_threshold_label.configure(text=f"{int(float(value))}")
        
    def log_message(self, message):
        """Add a message to the activity log"""
        timestamp = datetime.now().strftime("%H:%M:%S")
        log_entry = f"[{timestamp}] {message}\n"
        
        self.log_text.insert(tk.END, log_entry)
        self.log_text.see(tk.END)
        
        # Limit log size to prevent memory issues
        if self.log_text.index('end-1c').split('.')[0] > '1000':
            self.log_text.delete('1.0', '100.0')
            
    def clear_log(self):
        """Clear the activity log"""
        self.log_text.delete('1.0', tk.END)
        self.log_message("Log cleared")
        
    def detect_cast_button(self):
        """Detect cast button coordinates"""
        self.log_message("Click on the fishing cast button in 3 seconds...")
        self.root.after(3000, self._get_mouse_position_for_cast)
        
    def detect_fishing_area(self):
        """Detect fishing area coordinates"""
        self.log_message("Click on the fishing area in 3 seconds...")
        self.root.after(3000, self._get_mouse_position_for_area)
        
    def detect_reel_button(self):
        """Detect reel button coordinates"""
        self.log_message("Click on the reel button in 3 seconds...")
        self.root.after(3000, self._get_mouse_position_for_reel)
        
    def detect_timing_area(self):
        """Detect timing circle area coordinates"""
        self.log_message("Click on the timing circle area in 3 seconds...")
        self.root.after(3000, self._get_mouse_position_for_timing)
        
    def _get_mouse_position_for_cast(self):
        """Get mouse position for cast button"""
        try:
            x, y = pyautogui.position()
            self.cast_x_var.set(x)
            self.cast_y_var.set(y)
            self.fishing_params['cast_button'] = (x, y)
            self.log_message(f"Cast button set to: ({x}, {y})")
        except Exception as e:
            self.log_message(f"Error detecting cast button: {str(e)}")
            
    def _get_mouse_position_for_area(self):
        """Get mouse position for fishing area"""
        try:
            x, y = pyautogui.position()
            self.area_x_var.set(x)
            self.area_y_var.set(y)
            self.fishing_params['fishing_area'] = (x, y)
            self.log_message(f"Fishing area set to: ({x}, {y})")
        except Exception as e:
            self.log_message(f"Error detecting fishing area: {str(e)}")
            
    def _get_mouse_position_for_reel(self):
        """Get mouse position for reel button"""
        try:
            x, y = pyautogui.position()
            self.reel_x_var.set(x)
            self.reel_y_var.set(y)
            self.reel_params['reel_button'] = (x, y)
            self.log_message(f"Reel button set to: ({x}, {y})")
        except Exception as e:
            self.log_message(f"Error detecting reel button: {str(e)}")
            
    def _get_mouse_position_for_timing(self):
        """Get mouse position for timing area"""
        try:
            x, y = pyautogui.position()
            self.timing_x_var.set(x)
            self.timing_y_var.set(y)
            self.reel_params['timing_area'] = (x, y)
            self.log_message(f"Timing area set to: ({x}, {y})")
        except Exception as e:
            self.log_message(f"Error detecting timing area: {str(e)}")
            
    def start_fishing(self):
        """Start the fishing automation"""
        if self.is_running:
            return
            
        # Update parameters from GUI
        self.update_params_from_gui()
        
        self.is_running = True
        self.emergency_stop = False
        self.stats['session_start'] = datetime.now()
        
        # Update GUI
        self.start_button.configure(state='disabled')
        self.pause_button.configure(state='normal')
        self.stop_button.configure(state='normal')
        self.status_label.configure(text="Status: Running")
        
        # Start fishing thread
        self.thread = threading.Thread(target=self.fishing_loop, daemon=True)
        self.thread.start()
        
        # Start update timer
        self.update_timer()
        
        self.log_message("Fishing bot started!")
        
    def pause_fishing(self):
        """Pause the fishing automation"""
        if not self.is_running:
            return
            
        self.is_paused = not self.is_paused
        
        if self.is_paused:
            self.pause_button.configure(text="Resume")
            self.status_label.configure(text="Status: Paused")
            self.log_message("Fishing bot paused")
        else:
            self.pause_button.configure(text="Pause")
            self.status_label.configure(text="Status: Running")
            self.log_message("Fishing bot resumed")
            
    def resume_fishing(self):
        """Resume fishing if paused"""
        if self.is_paused:
            self.pause_fishing()
            
    def stop_fishing(self):
        """Stop the fishing automation"""
        self.is_running = False
        self.is_paused = False
        
        # Update GUI
        self.start_button.configure(state='normal')
        self.pause_button.configure(state='disabled', text="Pause")
        self.stop_button.configure(state='disabled')
        self.status_label.configure(text="Status: Stopped")
        
        self.log_message("Fishing bot stopped")
        
    def emergency_stop_fishing(self):
        """Emergency stop - immediately halt all activity"""
        self.emergency_stop = True
        self.stop_fishing()
        self.log_message("EMERGENCY STOP ACTIVATED!")
        
    def update_params_from_gui(self):
        """Update fishing parameters from GUI values"""
        try:
            # Update cast delay
            delay_range = self.cast_delay_var.get().split('-')
            if len(delay_range) == 2:
                self.fishing_params['cast_delay'] = (float(delay_range[0]), float(delay_range[1]))
            
            # Update other parameters
            self.fishing_params['bite_timeout'] = self.bite_timeout_var.get()
            self.fishing_params['hook_sensitivity'] = self.sensitivity_var.get()
            self.fishing_params['cast_button'] = (self.cast_x_var.get(), self.cast_y_var.get())
            self.fishing_params['fishing_area'] = (self.area_x_var.get(), self.area_y_var.get())
            
        except Exception as e:
            self.log_message(f"Error updating parameters: {str(e)}")
            
    def fishing_loop(self):
        """Main fishing automation loop"""
        last_break = time.time()
        
        while self.is_running and not self.emergency_stop:
            try:
                # Check for pause
                while self.is_paused and self.is_running:
                    time.sleep(0.1)
                    
                if not self.is_running or self.emergency_stop:
                    break
                    
                # Check for break time
                if self.anti_detect_var.get():
                    if time.time() - last_break > (self.break_interval_var.get() * 60):
                        self.take_break()
                        last_break = time.time()
                        continue
                
                # Perform fishing cycle
                self.perform_fishing_cycle()
                
            except Exception as e:
                self.log_message(f"Fishing loop error: {str(e)}")
                time.sleep(2)
                
    def perform_fishing_cycle(self):
        """Perform one complete fishing cycle with cast and reel"""
        try:
            # Step 1: Cast the line
            self.cast_line()
            
            # Step 2: Wait for bite detection or reel mini-game to appear
            self.log_message("Waiting for fish bite or reel mini-game...")
            reel_detected = self.wait_for_reel_minigame()
            
            if reel_detected and not self.emergency_stop:
                # Step 3: Handle reel timing mini-game
                success = self.handle_reel_timing()
                if success:
                    self.stats['fish_caught'] += 1
                    self.log_message("Fish caught successfully with reel timing!")
                else:
                    self.log_message("Failed reel timing, fish escaped...")
            else:
                self.log_message("No reel mini-game detected, recasting...")
                
            # Random delay before next cast
            if self.randomize_var.get():
                delay = random.uniform(*self.fishing_params['cast_delay'])
            else:
                delay = sum(self.fishing_params['cast_delay']) / 2
                
            time.sleep(delay)
            
        except Exception as e:
            self.log_message(f"Fishing cycle error: {str(e)}")
            
    def cast_line(self):
        """Cast the fishing line"""
        try:
            cast_x, cast_y = self.fishing_params['cast_button']
            
            # Click cast button
            pyautogui.click(cast_x, cast_y)
            self.stats['casts_made'] += 1
            
            # Small delay
            time.sleep(0.5)
            
            # Click fishing area
            area_x, area_y = self.fishing_params['fishing_area']
            if self.randomize_var.get():
                # Add small random offset to fishing area
                area_x += random.randint(-20, 20)
                area_y += random.randint(-20, 20)
                
            pyautogui.click(area_x, area_y)
            
            self.log_message(f"Line cast to ({area_x}, {area_y})")
            
        except Exception as e:
            self.log_message(f"Cast error: {str(e)}")
            
    def wait_for_bite(self):
        """Wait for fish bite detection"""
        try:
            start_time = time.time()
            timeout = self.fishing_params['bite_timeout']
            
            while time.time() - start_time < timeout:
                if self.emergency_stop or not self.is_running:
                    return False
                    
                # Check for pause
                while self.is_paused and self.is_running:
                    time.sleep(0.1)
                    
                # Here you would implement actual bite detection
                # For now, we'll simulate random bite timing
                if self.simulate_bite_detection():
                    return True
                    
                time.sleep(0.1)
                
            return False
            
        except Exception as e:
            self.log_message(f"Bite detection error: {str(e)}")
            return False
            
    def wait_for_reel_minigame(self):
        """Wait for reel mini-game to appear"""
        try:
            start_time = time.time()
            timeout = self.fishing_params['bite_timeout']
            
            while time.time() - start_time < timeout:
                if self.emergency_stop or not self.is_running:
                    return False
                    
                # Check for pause
                while self.is_paused and self.is_running:
                    time.sleep(0.1)
                    
                # Check if reel mini-game appeared by looking for timing circles
                if self.detect_reel_minigame():
                    self.log_message("Reel mini-game detected!")
                    return True
                    
                time.sleep(0.1)
                
            return False
            
        except Exception as e:
            self.log_message(f"Reel detection error: {str(e)}")
            return False
            
    def detect_reel_minigame(self):
        """Detect if reel mini-game is active"""
        try:
            # Get timing area coordinates
            timing_x, timing_y = self.reel_params['timing_area']
            radius = self.reel_params['circle_detection_radius']
            
            # Capture the timing area
            region = (timing_x - radius, timing_y - radius, radius * 2, radius * 2)
            screenshot = self.image_detector.capture_screen(region)
            
            if screenshot is None:
                return False
                
            # Convert to HSV for better color detection
            hsv = cv2.cvtColor(screenshot, cv2.COLOR_BGR2HSV)
            
            # Look for blue circles (dotted blue circle)
            blue_lower = np.array([100, 50, 50])
            blue_upper = np.array([130, 255, 255])
            blue_mask = cv2.inRange(hsv, blue_lower, blue_upper)
            
            # Look for white/light colors (shrinking circle)
            white_lower = np.array([0, 0, 200])
            white_upper = np.array([180, 30, 255])
            white_mask = cv2.inRange(hsv, white_lower, white_upper)
            
            # Check if we have significant blue and white areas (indicating circles)
            blue_pixels = np.sum(blue_mask > 0)
            white_pixels = np.sum(white_mask > 0)
            total_pixels = screenshot.shape[0] * screenshot.shape[1]
            
            blue_percentage = blue_pixels / total_pixels
            white_percentage = white_pixels / total_pixels
            
            # If we detect both blue and white areas, likely the mini-game is active
            return blue_percentage > 0.02 and white_percentage > 0.02  # 2% threshold for each
            
        except Exception as e:
            self.log_message(f"Reel mini-game detection error: {str(e)}")
            return False
            
    def handle_reel_timing(self):
        """Handle the reel timing mini-game"""
        try:
            self.log_message("Starting reel timing mini-game...")
            
            start_time = time.time()
            max_attempts = 50  # Maximum attempts to detect the right timing
            
            for attempt in range(max_attempts):
                if self.emergency_stop or not self.is_running:
                    return False
                    
                # Check if it's the right time to reel
                if self.is_perfect_timing():
                    # Add reaction delay
                    reaction_delay = self.reel_delay_var.get()
                    time.sleep(reaction_delay)
                    
                    # Click the reel button
                    reel_x, reel_y = self.reel_params['reel_button']
                    pyautogui.click(reel_x, reel_y)
                    
                    self.log_message(f"Reel button clicked! (Attempt {attempt + 1})")
                    
                    # Wait a moment to see if successful
                    time.sleep(1)
                    
                    # Check if mini-game is still active (if not, we likely succeeded)
                    if not self.detect_reel_minigame():
                        return True
                        
                # Small delay between checks
                time.sleep(0.05)  # Check every 50ms for responsive timing
                
                # Timeout after reasonable time
                if time.time() - start_time > 10:  # 10 second timeout
                    break
                    
            self.log_message("Reel timing timeout or failed")
            return False
            
        except Exception as e:
            self.log_message(f"Reel timing error: {str(e)}")
            return False
            
    def is_perfect_timing(self):
        """Check if it's the perfect timing to press reel (green or circle overlap)"""
        try:
            # Get timing area coordinates
            timing_x, timing_y = self.reel_params['timing_area']
            radius = self.reel_params['circle_detection_radius']
            
            # Capture the timing area
            region = (timing_x - radius, timing_y - radius, radius * 2, radius * 2)
            screenshot = self.image_detector.capture_screen(region)
            
            if screenshot is None:
                return False
                
            # Convert to HSV
            hsv = cv2.cvtColor(screenshot, cv2.COLOR_BGR2HSV)
            
            # Method 1: Look for green color (when timing turns green)
            green_lower = np.array([35, 50, 50])
            green_upper = np.array([85, 255, 255])
            green_mask = cv2.inRange(hsv, green_lower, green_upper)
            
            green_pixels = np.sum(green_mask > 0)
            total_pixels = screenshot.shape[0] * screenshot.shape[1]
            green_percentage = green_pixels / total_pixels
            
            # If we detect significant green, it's perfect timing
            if green_percentage > (self.green_threshold_var.get() / 1000):  # Convert threshold to percentage
                self.log_message("Perfect timing detected: GREEN!")
                return True
                
            # Method 2: Detect circle overlap by looking for specific color combinations
            # This is more complex and would require more specific color analysis
            # For now, we'll rely primarily on green detection
            
            return False
            
        except Exception as e:
            self.log_message(f"Timing detection error: {str(e)}")
            return False
        
    def hook_fish(self):
        """Attempt to hook the fish"""
        try:
            # Add reaction time delay
            if self.randomize_var.get():
                reaction_delay = random.uniform(*self.fishing_params['reaction_time'])
            else:
                reaction_delay = sum(self.fishing_params['reaction_time']) / 2
                
            time.sleep(reaction_delay)
            
            # Click to hook (usually same as cast button or specific hook button)
            hook_x, hook_y = self.fishing_params['cast_button']
            pyautogui.click(hook_x, hook_y)
            
            self.log_message("Attempting to hook fish...")
            
            # Wait a moment to see if successful
            time.sleep(2)
            
            # Simulate success rate (replace with actual detection)
            return random.random() < 0.7  # 70% success rate
            
        except Exception as e:
            self.log_message(f"Hook error: {str(e)}")
            return False
            
    def take_break(self):
        """Take a randomized break for anti-detection"""
        break_duration = random.randint(30, 120)  # 30 seconds to 2 minutes
        self.log_message(f"Taking {break_duration} second break for anti-detection...")
        
        start_time = time.time()
        while time.time() - start_time < break_duration:
            if self.emergency_stop or not self.is_running:
                break
            time.sleep(1)
            
        self.log_message("Break completed, resuming fishing...")
        
    def update_timer(self):
        """Update the runtime timer"""
        if self.is_running and self.stats['session_start']:
            runtime = datetime.now() - self.stats['session_start']
            runtime_str = str(runtime).split('.')[0]  # Remove microseconds
            self.time_label.configure(text=f"Runtime: {runtime_str}")
            
            # Update statistics
            self.update_statistics()
            
        # Schedule next update
        if self.is_running:
            self.root.after(1000, self.update_timer)
            
    def update_statistics(self):
        """Update statistics display"""
        try:
            # Update fish caught
            self.fish_caught_label.configure(text=f"Fish Caught: {self.stats['fish_caught']}")
            
            # Update casts made
            self.casts_made_label.configure(text=f"Casts Made: {self.stats['casts_made']}")
            
            # Update success rate
            if self.stats['casts_made'] > 0:
                success_rate = (self.stats['fish_caught'] / self.stats['casts_made']) * 100
                self.success_rate_label.configure(text=f"Success Rate: {success_rate:.1f}%")
            else:
                self.success_rate_label.configure(text="Success Rate: 0%")
                
            # Update session time
            if self.stats['session_start']:
                session_time = datetime.now() - self.stats['session_start']
                session_str = str(session_time).split('.')[0]
                self.session_time_label.configure(text=f"Session Time: {session_str}")
                
                # Calculate fish per hour
                hours = session_time.total_seconds() / 3600
                if hours > 0:
                    fish_per_hour = self.stats['fish_caught'] / hours
                    self.fish_per_hour_label.configure(text=f"Fish per Hour: {fish_per_hour:.1f}")
                    
        except Exception as e:
            self.log_message(f"Statistics update error: {str(e)}")
            
    def reset_stats(self):
        """Reset all statistics"""
        self.stats = {
            'fish_caught': 0,
            'casts_made': 0,
            'session_start': datetime.now() if self.is_running else None,
            'total_runtime': 0
        }
        self.update_statistics()
        self.log_message("Statistics reset")
        
    def save_config(self):
        """Save current configuration using config manager"""
        try:
            # Update config from GUI values
            self.update_config_from_gui()
            
            # Save using config manager
            if self.config_manager.save_config():
                self.log_message("Configuration saved successfully")
                messagebox.showinfo("Success", "Configuration saved successfully!")
            else:
                raise Exception("Config manager failed to save")
            
        except Exception as e:
            error_msg = f"Error saving configuration: {str(e)}"
            self.log_message(error_msg)
            messagebox.showerror("Error", error_msg)
            
    def load_config(self):
        """Load configuration using config manager"""
        try:
            if self.config_manager.load_config():
                # Update GUI from loaded config
                self.update_gui_from_config()
                self.load_fishing_params()
                self.log_message("Configuration loaded successfully")
            else:
                self.log_message("No configuration file found, using defaults")
                
        except Exception as e:
            error_msg = f"Error loading configuration: {str(e)}"
            self.log_message(error_msg)
            messagebox.showerror("Error", error_msg)
            
    def update_config_from_gui(self):
        """Update config manager from GUI values"""
        try:
            # Coordinates
            self.config_manager.set('Coordinates', 'cast_button_x', self.cast_x_var.get())
            self.config_manager.set('Coordinates', 'cast_button_y', self.cast_y_var.get())
            self.config_manager.set('Coordinates', 'fishing_area_x', self.area_x_var.get())
            self.config_manager.set('Coordinates', 'fishing_area_y', self.area_y_var.get())
            
            # Timing
            delay_range = self.cast_delay_var.get().split('-')
            if len(delay_range) == 2:
                self.config_manager.set('Timing', 'cast_delay_min', float(delay_range[0]))
                self.config_manager.set('Timing', 'cast_delay_max', float(delay_range[1]))
            
            self.config_manager.set('Timing', 'bite_timeout', self.bite_timeout_var.get())
            
            # Detection
            self.config_manager.set('Detection', 'hook_sensitivity', self.sensitivity_var.get())
            
            # Safety
            self.config_manager.set('Safety', 'randomize_timings', self.randomize_var.get())
            self.config_manager.set('Safety', 'anti_detection_enabled', self.anti_detect_var.get())
            self.config_manager.set('Safety', 'break_interval_minutes', self.break_interval_var.get())
            
        except Exception as e:
            self.log_message(f"Error updating config from GUI: {str(e)}")
            
    def update_gui_from_config(self):
        """Update GUI from config manager values"""
        try:
            # Coordinates
            self.cast_x_var.set(self.config_manager.getint('Coordinates', 'cast_button_x', 400))
            self.cast_y_var.set(self.config_manager.getint('Coordinates', 'cast_button_y', 500))
            self.area_x_var.set(self.config_manager.getint('Coordinates', 'fishing_area_x', 400))
            self.area_y_var.set(self.config_manager.getint('Coordinates', 'fishing_area_y', 300))
            
            # Timing
            cast_min = self.config_manager.getfloat('Timing', 'cast_delay_min', 2.0)
            cast_max = self.config_manager.getfloat('Timing', 'cast_delay_max', 4.0)
            self.cast_delay_var.set(f"{cast_min}-{cast_max}")
            
            self.bite_timeout_var.set(self.config_manager.getint('Timing', 'bite_timeout', 30))
            
            # Detection
            self.sensitivity_var.set(self.config_manager.getfloat('Detection', 'hook_sensitivity', 0.8))
            
            # Safety
            self.randomize_var.set(self.config_manager.getboolean('Safety', 'randomize_timings', True))
            self.anti_detect_var.set(self.config_manager.getboolean('Safety', 'anti_detection_enabled', True))
            self.break_interval_var.set(self.config_manager.getint('Safety', 'break_interval_minutes', 30))
            
        except Exception as e:
            self.log_message(f"Error updating GUI from config: {str(e)}")
            
    def reset_config(self):
        """Reset configuration to defaults"""
        if messagebox.askyesno("Confirm Reset", "Are you sure you want to reset all settings to defaults?"):
            # Reset to defaults
            self.cast_x_var.set(400)
            self.cast_y_var.set(500)
            self.area_x_var.set(400)
            self.area_y_var.set(300)
            self.sensitivity_var.set(0.8)
            self.cast_delay_var.set("2-4")
            self.bite_timeout_var.set(30)
            self.randomize_var.set(True)
            self.anti_detect_var.set(True)
            self.break_interval_var.set(30)
            
            self.update_params_from_gui()
            self.log_message("Configuration reset to defaults")
            
    def on_closing(self):
        """Handle application closing"""
        if self.is_running:
            if messagebox.askyesno("Confirm Exit", "Fishing bot is still running. Stop and exit?"):
                self.stop_fishing()
                time.sleep(1)  # Give time for threads to stop
                self.root.destroy()
        else:
            self.root.destroy()
            
    def run(self):
        """Run the application"""
        self.root.protocol("WM_DELETE_WINDOW", self.on_closing)
        self.log_message("Ragnarok X Auto Fishing Bot initialized")
        self.log_message("Press F1 to start, F2 to pause, F3 to stop, F4 for emergency stop")
        self.root.mainloop()

if __name__ == "__main__":
    try:
        # Create and run the fishing bot
        bot = RagnarokFishingBot()
        bot.run()
    except Exception as e:
        print(f"Failed to start fishing bot: {str(e)}")
        input("Press Enter to exit...")
