import tkinter as tk
from tkinter import ttk, messagebox
import threading
import queue
import time
import sys
import os

# Add error handling for imports
try:
    from main import Fishing
    print("✅ Successfully imported Fishing class")
except ImportError as e:
    print(f"❌ Cannot import Fishing class: {e}")
    print("Make sure main.py is in the same directory")
    sys.exit(1)

try:
    import pyautogui
    # Disable pyautogui failsafe
    pyautogui.FAILSAFE = False
    print("✅ PyAutoGUI imported successfully")
except ImportError:
    print("❌ PyAutoGUI not found. Install with: pip install pyautogui")
    sys.exit(1)

class FishingGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Fishing Bot - Debug Version")
        self.root.geometry("600x500")
        self.root.resizable(False, False)
        
        # Initialize variables
        self.fishing_thread = None
        self.is_fishing = False
        self.fishing_instance = None
        self.message_queue = queue.Queue()
        
        self.setup_ui()
        self.check_queue()
        
        # Log startup message
        self.log_message("🚀 Debug Fishing Bot initialized!")
        self.log_message("This version will show detailed debugging info")
        
    def setup_ui(self):
        # Main frame
        main_frame = ttk.Frame(self.root, padding="10")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Title
        title_label = ttk.Label(main_frame, text="🎣 Fishing Bot - Debug Mode", 
                               font=("Arial", 14, "bold"))
        title_label.grid(row=0, column=0, columnspan=3, pady=(0, 20))
        
        # Configuration frame
        config_frame = ttk.LabelFrame(main_frame, text="Configuration", padding="10")
        config_frame.grid(row=1, column=0, columnspan=3, sticky=(tk.W, tk.E), pady=(0, 10))
        
        # Max fishing setting
        ttk.Label(config_frame, text="Maximum Fish:").grid(row=0, column=0, sticky=tk.W, pady=5)
        self.max_fish_var = tk.StringVar(value="3")  # Lower number for testing
        max_fish_entry = ttk.Entry(config_frame, textvariable=self.max_fish_var, width=10)
        max_fish_entry.grid(row=0, column=1, sticky=tk.W, padx=(10, 0), pady=5)
        
        # Test buttons
        test_import_btn = ttk.Button(config_frame, text="Test Import", 
                                    command=self.test_import)
        test_import_btn.grid(row=0, column=2, padx=(20, 0), pady=5)
        
        test_detection_btn = ttk.Button(config_frame, text="Test Detection", 
                                       command=self.test_detection)
        test_detection_btn.grid(row=0, column=3, padx=(10, 0), pady=5)
        
        # Control buttons frame
        button_frame = ttk.LabelFrame(main_frame, text="Controls", padding="10")
        button_frame.grid(row=2, column=0, columnspan=3, sticky=(tk.W, tk.E), pady=(0, 10))
        
        control_buttons = ttk.Frame(button_frame)
        control_buttons.pack()
        
        # Start button
        self.start_button = ttk.Button(control_buttons, text="▶️ Start Fishing (Debug)", 
                                      command=self.start_fishing)
        self.start_button.pack(side=tk.LEFT, padx=(0, 10))
        
        # Stop button
        self.stop_button = ttk.Button(control_buttons, text="⏹️ Stop Fishing", 
                                     command=self.stop_fishing, state=tk.DISABLED)
        self.stop_button.pack(side=tk.LEFT)
        
        # Simple test button
        simple_test_btn = ttk.Button(control_buttons, text="🧪 Simple Test", 
                                    command=self.simple_test)
        simple_test_btn.pack(side=tk.LEFT, padx=(10, 0))
        
        # Status frame
        status_frame = ttk.LabelFrame(main_frame, text="Status", padding="10")
        status_frame.grid(row=3, column=0, columnspan=3, sticky=(tk.W, tk.E), pady=(0, 10))
        
        # Status labels
        ttk.Label(status_frame, text="Status:").grid(row=0, column=0, sticky=tk.W)
        self.status_var = tk.StringVar(value="Ready")
        self.status_label = ttk.Label(status_frame, textvariable=self.status_var, 
                                     foreground="blue", font=("Arial", 9, "bold"))
        self.status_label.grid(row=0, column=1, sticky=tk.W, padx=(10, 0))
        
        ttk.Label(status_frame, text="Fish:").grid(row=0, column=2, sticky=tk.W, padx=(20, 0))
        self.fish_count_var = tk.StringVar(value="0")
        self.fish_label = ttk.Label(status_frame, textvariable=self.fish_count_var, 
                                   foreground="green", font=("Arial", 12, "bold"))
        self.fish_label.grid(row=0, column=3, sticky=tk.W, padx=(10, 0))
        
        # Log area
        log_frame = ttk.LabelFrame(main_frame, text="Debug Log", padding="5")
        log_frame.grid(row=4, column=0, columnspan=3, sticky=(tk.W, tk.E, tk.N, tk.S), pady=(10, 0))
        
        # Text widget with scrollbar
        text_frame = ttk.Frame(log_frame)
        text_frame.pack(fill=tk.BOTH, expand=True)
        
        self.log_text = tk.Text(text_frame, height=15, width=80, wrap=tk.WORD, 
                               font=("Consolas", 9))
        scrollbar = ttk.Scrollbar(text_frame, orient=tk.VERTICAL, command=self.log_text.yview)
        self.log_text.configure(yscrollcommand=scrollbar.set)
        
        self.log_text.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        # Configure grid weights
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)
        main_frame.columnconfigure(2, weight=1)
        main_frame.rowconfigure(4, weight=1)
        
    def test_import(self):
        """Test importing and creating Fishing instance"""
        self.log_message("🧪 Testing import and instance creation...")
        try:
            fishing = Fishing(5)
            self.log_message(f"✅ Fishing instance created successfully")
            self.log_message(f"   - max_fishing: {fishing.max_fishing}")
            self.log_message(f"   - position: {fishing.position}")
            self.log_message(f"   - amount: {fishing.amount}")
        except Exception as e:
            self.log_message(f"❌ Import/creation failed: {e}")
            import traceback
            self.log_message(f"   Traceback: {traceback.format_exc()}")
        
    def test_detection(self):
        """Test image detection"""
        self.log_message("🔍 Testing image detection...")
        
        try:
            # Test cast button detection
            self.log_message("   Testing cast.png detection...")
            cast_position = pyautogui.locateCenterOnScreen('image/cast.png', confidence=0.9)
            if cast_position:
                self.log_message(f"   ✅ Cast button found at: {cast_position}")
            else:
                self.log_message("   ❌ Cast button NOT found")
                
            # Test reel button detection
            self.log_message("   Testing reel.png detection...")
            reel_position = pyautogui.locateCenterOnScreen('image/reel.png', confidence=0.47)
            if reel_position:
                self.log_message(f"   ✅ Reel button found at: {reel_position}")
            else:
                self.log_message("   ❌ Reel button NOT found")
                
        except Exception as e:
            self.log_message(f"❌ Detection test failed: {e}")
        
    def simple_test(self):
        """Simple test without threading"""
        self.log_message("🧪 Running simple test (no threading)...")
        try:
            max_fish = int(self.max_fish_var.get())
            self.log_message(f"   Creating Fishing instance with max_fish={max_fish}")
            
            fishing = Fishing(max_fish)
            self.log_message(f"   ✅ Instance created: position={fishing.position}, amount={fishing.amount}")
            
            # Test one throw
            self.log_message("   Testing throw method...")
            fishing.throw()
            self.log_message(f"   After throw: position={fishing.position}")
            
        except Exception as e:
            self.log_message(f"❌ Simple test failed: {e}")
            import traceback
            self.log_message(f"   Traceback: {traceback.format_exc()}")
        
    def log_message(self, message):
        """Add message to log with timestamp"""
        timestamp = time.strftime("%H:%M:%S")
        log_entry = f"[{timestamp}] {message}\n"
        self.log_text.insert(tk.END, log_entry)
        self.log_text.see(tk.END)
        # Force GUI update
        self.root.update_idletasks()
        
    def start_fishing(self):
        """Start the fishing process in a separate thread"""
        self.log_message("🚀 Starting fishing process...")
        
        try:
            max_fish = int(self.max_fish_var.get())
            if max_fish <= 0:
                raise ValueError("Maximum fish must be greater than 0")
        except ValueError as e:
            messagebox.showerror("Error", f"Invalid maximum fish value: {e}")
            return
            
        self.log_message(f"   Target fish: {max_fish}")
        
        # Check if image files exist
        if not os.path.exists('image/cast.png'):
            self.log_message("❌ cast.png not found in image folder!")
            messagebox.showerror("Error", "cast.png not found in image folder!")
            return
            
        if not os.path.exists('image/reel.png'):
            self.log_message("❌ reel.png not found in image folder!")
            messagebox.showerror("Error", "reel.png not found in image folder!")
            return
            
        self.log_message("   ✅ Image files found")
        
        self.is_fishing = True
        self.start_button.config(state=tk.DISABLED)
        self.stop_button.config(state=tk.NORMAL)
        
        self.status_var.set("Starting...")
        self.log_message("   🧵 Creating fishing thread...")
        
        # Start fishing in separate thread
        self.fishing_thread = threading.Thread(target=self.fishing_worker, args=(max_fish,))
        self.fishing_thread.daemon = True
        self.fishing_thread.start()
        
        self.log_message("   ✅ Fishing thread started!")
        
    def stop_fishing(self):
        """Stop the fishing process"""
        self.log_message("⏹️ Stop button pressed")
        self.is_fishing = False
        self.status_var.set("Stopping...")
        
    def fishing_worker(self, max_fish):
        """Worker function that runs the fishing logic"""
        self.message_queue.put(("log", "🧵 Worker thread started"))
        self.message_queue.put(("log", f"   Worker received max_fish: {max_fish}"))
        
        try:
            # Create a custom fishing class that communicates with GUI
            self.message_queue.put(("log", "   Creating FishingWithGUI instance..."))
            fishing = FishingWithGUI(max_fish, self.message_queue, self.is_fishing_active)
            self.message_queue.put(("log", "   ✅ FishingWithGUI instance created"))
            
            self.message_queue.put(("log", "   Calling fishing.fishing()..."))
            fishing.fishing()
            self.message_queue.put(("log", "   ✅ fishing.fishing() completed"))
            
        except Exception as e:
            error_msg = f"Worker error: {str(e)}"
            self.message_queue.put(("error", error_msg))
            self.message_queue.put(("log", f"❌ {error_msg}"))
            import traceback
            self.message_queue.put(("log", f"   Traceback: {traceback.format_exc()}"))
        finally:
            self.message_queue.put(("log", "🧵 Worker thread finishing"))
            self.message_queue.put(("finished", ""))
            
    def is_fishing_active(self):
        """Check if fishing should continue"""
        active = self.is_fishing
        if not active:
            self.message_queue.put(("log", "   is_fishing_active() returned False - stopping"))
        return active
        
    def check_queue(self):
        """Check for messages from fishing thread"""
        try:
            while True:
                msg_type, data = self.message_queue.get_nowait()
                
                if msg_type == "status":
                    self.status_var.set(data)
                elif msg_type == "fish_count":
                    self.fish_count_var.set(str(data))
                elif msg_type == "log":
                    self.log_message(data)
                elif msg_type == "finished":
                    self.fishing_finished()
                elif msg_type == "error":
                    messagebox.showerror("Error", data)
                    self.fishing_finished()
                    
        except queue.Empty:
            pass
        
        # Schedule next check
        self.root.after(100, self.check_queue)
        
    def fishing_finished(self):
        """Handle fishing completion"""
        self.log_message("✅ Fishing session finished!")
        self.is_fishing = False
        self.start_button.config(state=tk.NORMAL)
        self.stop_button.config(state=tk.DISABLED)
        self.status_var.set("Finished")

class FishingWithGUI(Fishing):
    """Extended Fishing class that communicates with GUI"""
    
    def __init__(self, max_fishing, message_queue, is_active_callback):
        self.message_queue = message_queue
        self.is_active = is_active_callback
        
        self.message_queue.put(("log", f"   FishingWithGUI.__init__ called with max_fishing={max_fishing}"))
        
        try:
            super().__init__(max_fishing)
            self.message_queue.put(("log", f"   ✅ Parent __init__ successful"))
            self.message_queue.put(("log", f"   Initial state: position={self.position}, amount={self.amount}"))
        except Exception as e:
            self.message_queue.put(("log", f"   ❌ Parent __init__ failed: {e}"))
            raise
        
    def throw(self):
        """Override throw method to send status updates"""
        self.message_queue.put(("log", "   🎣 throw() method called"))
        
        try:
            # Call the original throw method from main.py
            self.message_queue.put(("log", "   Calling super().throw()..."))
            super().throw()
            self.message_queue.put(("log", f"   ✅ super().throw() completed, position now: {self.position}"))
            
        except Exception as e:
            self.message_queue.put(("log", f"   ❌ throw() error: {e}"))
            
    def wait_for_reel(self):
        """Override wait_for_reel method to send status updates"""
        self.message_queue.put(("log", "   ⏳ wait_for_reel() method called"))
        
        try:
            # Call the original wait_for_reel method from main.py
            self.message_queue.put(("log", "   Calling super().wait_for_reel()..."))
            result = super().wait_for_reel()
            self.message_queue.put(("log", f"   ✅ super().wait_for_reel() returned: {result}"))
            self.message_queue.put(("fish_count", self.amount))
            return result
            
        except Exception as e:
            self.message_queue.put(("log", f"   ❌ wait_for_reel() error: {e}"))
            return False
        
    def fishing(self):
        """Override fishing method to check for stop condition"""
        self.message_queue.put(("log", "🎣 fishing() method started"))
        
        iteration = 0
        while self.is_active():
            iteration += 1
            self.message_queue.put(("log", f"   Fishing loop iteration #{iteration}"))
            
            if self.amount >= self.max_fishing:
                self.message_queue.put(("log", f"🎯 Target reached! Caught {self.amount} fish"))
                break
            elif self.position == 0:
                self.message_queue.put(("log", "   Position=0, calling throw()"))
                self.throw()
            elif self.position == 1:
                self.message_queue.put(("log", "   Position=1, calling wait_for_reel()"))
                self.wait_for_reel()
            else:
                self.message_queue.put(("log", f"   Unknown position: {self.position}"))
                
            # Small delay to prevent excessive CPU usage
            time.sleep(0.5)  # Longer delay for debugging
            
        self.message_queue.put(("log", "🎣 fishing() method completed"))

def main():
    try:
        root = tk.Tk()
        app = FishingGUI(root)
        root.mainloop()
    except Exception as e:
        print(f"❌ Application error: {e}")
        import traceback
        traceback.print_exc()
        input("Press Enter to exit...")

if __name__ == "__main__":
    main()