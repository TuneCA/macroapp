"""
Launcher for Ragnarok X Auto Fishing Bot
Provides easy access to all bot components
"""

import tkinter as tk
from tkinter import ttk, messagebox
import subprocess
import sys
import os
import threading

class BotLauncher:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Ragnarok X Auto Fishing Bot Launcher")
        self.root.geometry("500x400")
        self.root.resizable(False, False)
        
        # Set icon and styling
        self.setup_styling()
        self.setup_gui()
        
    def setup_styling(self):
        """Setup custom styling"""
        style = ttk.Style()
        style.theme_use('vista')  # Use vista theme on Windows
        
        # Configure custom styles
        style.configure('Title.TLabel', font=('Arial', 16, 'bold'))
        style.configure('Subtitle.TLabel', font=('Arial', 10))
        style.configure('Launch.TButton', font=('Arial', 11), padding=10)
        
    def setup_gui(self):
        """Setup the launcher GUI"""
        # Title section
        title_frame = ttk.Frame(self.root)
        title_frame.pack(fill='x', pady=20)
        
        title_label = ttk.Label(title_frame, text="Ragnarok X Auto Fishing Bot", 
                               style='Title.TLabel')
        title_label.pack()
        
        subtitle_label = ttk.Label(title_frame, text="Complete Automation Suite for Ragnarok X Next Generation", 
                                  style='Subtitle.TLabel')
        subtitle_label.pack(pady=(5, 0))
        
        # Main applications section
        main_frame = ttk.LabelFrame(self.root, text="Main Applications", padding=20)
        main_frame.pack(fill='x', padx=20, pady=10)
        
        # Main bot button
        bot_frame = ttk.Frame(main_frame)
        bot_frame.pack(fill='x', pady=(0, 10))
        
        ttk.Button(bot_frame, text="🎣 Launch Fishing Bot", 
                  command=self.launch_main_bot, 
                  style='Launch.TButton').pack(side='left')
        
        ttk.Label(bot_frame, text="Main fishing automation tool with GUI", 
                 font=('Arial', 9)).pack(side='left', padx=(10, 0))
        
        # Utilities section
        utils_frame = ttk.LabelFrame(self.root, text="Utility Tools", padding=20)
        utils_frame.pack(fill='x', padx=20, pady=10)
        
        utilities = [
            ("🎯 Coordinate Detector", "Detect game element coordinates", self.launch_coordinate_detector),
            ("📸 Screen Capture Tool", "Capture and create templates", self.launch_screen_capture),
            ("🧪 Testing Tool", "Test bot functionality", self.launch_testing_tool),
            ("🎣 Reel Timing Tester", "Test reel timing detection", self.launch_reel_tester),
        ]
        
        for i, (text, desc, command) in enumerate(utilities):
            util_frame = ttk.Frame(utils_frame)
            util_frame.pack(fill='x', pady=2)
            
            ttk.Button(util_frame, text=text, command=command, width=25).pack(side='left')
            ttk.Label(util_frame, text=desc, font=('Arial', 9)).pack(side='left', padx=(10, 0))
            
        # Information section
        info_frame = ttk.LabelFrame(self.root, text="Information", padding=20)
        info_frame.pack(fill='x', padx=20, pady=10)
        
        info_buttons = [
            ("📖 Read Instructions", self.show_instructions),
            ("⚙️ System Check", self.run_system_check),
            ("📁 Open Config Folder", self.open_config_folder),
        ]
        
        for text, command in info_buttons:
            ttk.Button(info_frame, text=text, command=command, width=20).pack(side='left', padx=5)
            
        # Status bar
        self.status_var = tk.StringVar(value="Ready to launch")
        status_bar = ttk.Label(self.root, textvariable=self.status_var, 
                              relief='sunken', anchor='w')
        status_bar.pack(fill='x', side='bottom')
        
    def launch_main_bot(self):
        """Launch the main fishing bot"""
        try:
            self.status_var.set("Launching main fishing bot...")
            self.root.update()
            
            # Launch in separate process
            subprocess.Popen([sys.executable, "main.py"], 
                           creationflags=subprocess.CREATE_NEW_CONSOLE if os.name == 'nt' else 0)
            
            self.status_var.set("Main fishing bot launched successfully")
            
        except Exception as e:
            messagebox.showerror("Error", f"Failed to launch main bot: {str(e)}")
            self.status_var.set("Failed to launch main bot")
            
    def launch_coordinate_detector(self):
        """Launch coordinate detection tool"""
        try:
            self.status_var.set("Launching coordinate detector...")
            self.root.update()
            
            subprocess.Popen([sys.executable, "utils.py", "coordinate"])
            self.status_var.set("Coordinate detector launched")
            
        except Exception as e:
            messagebox.showerror("Error", f"Failed to launch coordinate detector: {str(e)}")
            self.status_var.set("Failed to launch coordinate detector")
            
    def launch_screen_capture(self):
        """Launch screen capture tool"""
        try:
            self.status_var.set("Launching screen capture tool...")
            self.root.update()
            
            subprocess.Popen([sys.executable, "utils.py", "capture"])
            self.status_var.set("Screen capture tool launched")
            
        except Exception as e:
            messagebox.showerror("Error", f"Failed to launch screen capture tool: {str(e)}")
            self.status_var.set("Failed to launch screen capture tool")
            
    def launch_testing_tool(self):
        """Launch testing tool"""
        try:
            self.status_var.set("Launching testing tool...")
            self.root.update()
            
            subprocess.Popen([sys.executable, "utils.py", "test"])
            self.status_var.set("Testing tool launched")
            
        except Exception as e:
            messagebox.showerror("Error", f"Failed to launch testing tool: {str(e)}")
            self.status_var.set("Failed to launch testing tool")
            
    def launch_reel_tester(self):
        """Launch reel timing tester"""
        try:
            self.status_var.set("Launching reel timing tester...")
            self.root.update()
            
            subprocess.Popen([sys.executable, "reel_tester.py"])
            self.status_var.set("Reel timing tester launched")
            
        except Exception as e:
            messagebox.showerror("Error", f"Failed to launch reel timing tester: {str(e)}")
            self.status_var.set("Failed to launch reel timing tester")
            
    def show_instructions(self):
        """Show instructions window"""
        instructions_window = tk.Toplevel(self.root)
        instructions_window.title("Setup Instructions")
        instructions_window.geometry("600x500")
        
        instructions_text = """
RAGNAROK X AUTO FISHING BOT - SETUP INSTRUCTIONS

INITIAL SETUP:
1. Install and start Ragnarok X Next Generation
2. Go to a fishing location in the game
3. Open the fishing interface
4. Set the game to windowed mode for better detection

FISHING MECHANICS:
Ragnarok X uses a two-step fishing process:
1. CAST: Click the cast button and select fishing area
2. REEL: Timing mini-game where you must click when:
   - The shrinking circle touches the dotted blue circle, OR
   - The timing indicator turns green

COORDINATE SETUP:
1. Launch the Coordinate Detector tool
2. Set up all required coordinates:
   - Cast Button: The fishing cast button
   - Fishing Area: Where to cast your line  
   - Reel Button: The timing mini-game button
   - Timing Area: Center of the timing circles

REEL TIMING CALIBRATION:
1. Launch the Reel Timing Tester tool
2. Set the timing area coordinates
3. Start monitoring during a reel mini-game
4. Adjust green detection threshold as needed
5. Test click timing and reaction delays

CONFIGURATION:
1. Launch the main fishing bot
2. Go to the Configuration tab
3. Adjust timing and detection settings
4. Set reel timing delay based on your preference
5. Test with short sessions first

SAFETY RECOMMENDATIONS:
- Enable randomization and anti-detection features
- Take regular breaks
- Don't run for extended periods
- Monitor the bot during use

HOTKEYS:
- F1: Start/Resume fishing
- F2: Pause fishing
- F3: Stop fishing
- F4: Emergency stop

TROUBLESHOOTING:
- If reel timing fails, use the Reel Timing Tester
- Adjust timing delay if reactions are too fast/slow
- Make sure timing area covers the circles properly
- Check that all coordinates are correctly set
- Verify game window is visible and focused

The bot will automatically handle both casting and reel timing!
        """
        
        text_widget = tk.Text(instructions_window, wrap='word', padx=10, pady=10)
        text_widget.insert(tk.END, instructions_text)
        text_widget.configure(state='disabled')
        
        scrollbar = ttk.Scrollbar(instructions_window, orient='vertical', command=text_widget.yview)
        text_widget.configure(yscrollcommand=scrollbar.set)
        
        text_widget.pack(side='left', fill='both', expand=True)
        scrollbar.pack(side='right', fill='y')
        
    def run_system_check(self):
        """Run system compatibility check"""
        check_window = tk.Toplevel(self.root)
        check_window.title("System Check")
        check_window.geometry("500x400")
        
        # Create text widget for results
        result_text = tk.Text(check_window, wrap='word', padx=10, pady=10)
        result_text.pack(fill='both', expand=True)
        
        def perform_check():
            """Perform the actual system check"""
            result_text.insert(tk.END, "Running system compatibility check...\n\n")
            result_text.update()
            
            # Check Python version
            result_text.insert(tk.END, f"Python Version: {sys.version}\n")
            result_text.update()
            
            # Check required modules
            required_modules = [
                'tkinter', 'pyautogui', 'cv2', 'numpy', 'PIL', 
                'pynput', 'configparser', 'psutil'
            ]
            
            result_text.insert(tk.END, "\nChecking required modules:\n")
            missing_modules = []
            
            for module in required_modules:
                try:
                    __import__(module)
                    result_text.insert(tk.END, f"✓ {module}\n")
                except ImportError:
                    result_text.insert(tk.END, f"✗ {module} - MISSING\n")
                    missing_modules.append(module)
                result_text.update()
                
            # Check screen resolution
            try:
                import pyautogui
                screen_size = pyautogui.size()
                result_text.insert(tk.END, f"\nScreen Resolution: {screen_size.width}x{screen_size.height}\n")
            except:
                result_text.insert(tk.END, "\nScreen Resolution: Could not detect\n")
                
            # Check file permissions
            result_text.insert(tk.END, "\nChecking file permissions:\n")
            test_files = ['main.py', 'utils.py', 'config_manager.py', 'image_detector.py']
            
            for file in test_files:
                if os.path.exists(file):
                    if os.access(file, os.R_OK):
                        result_text.insert(tk.END, f"✓ {file} - Readable\n")
                    else:
                        result_text.insert(tk.END, f"✗ {file} - Not readable\n")
                else:
                    result_text.insert(tk.END, f"✗ {file} - Missing\n")
                result_text.update()
                
            # Summary
            result_text.insert(tk.END, "\n" + "="*50 + "\n")
            if missing_modules:
                result_text.insert(tk.END, f"❌ ISSUES FOUND: Missing modules: {', '.join(missing_modules)}\n")
                result_text.insert(tk.END, "Please install missing modules before using the bot.\n")
            else:
                result_text.insert(tk.END, "✅ SYSTEM CHECK PASSED: All requirements met!\n")
                result_text.insert(tk.END, "Your system is ready to run the fishing bot.\n")
                
        # Run check in thread to avoid freezing GUI
        check_thread = threading.Thread(target=perform_check, daemon=True)
        check_thread.start()
        
    def open_config_folder(self):
        """Open configuration folder"""
        try:
            config_dir = "config"
            if not os.path.exists(config_dir):
                os.makedirs(config_dir)
                
            # Open folder in system file manager
            if os.name == 'nt':  # Windows
                os.startfile(config_dir)
            elif os.name == 'posix':  # macOS and Linux
                subprocess.call(['open', config_dir])
            else:
                messagebox.showinfo("Info", f"Config folder: {os.path.abspath(config_dir)}")
                
        except Exception as e:
            messagebox.showerror("Error", f"Failed to open config folder: {str(e)}")
            
    def run(self):
        """Run the launcher"""
        self.root.mainloop()

if __name__ == "__main__":
    launcher = BotLauncher()
    launcher.run()
