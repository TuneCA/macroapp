# Ragnarok X Auto Fishing Bot

A comprehensive automation tool for fishing in Ragnarok X Next Generation, designed specifically for PC with full support for the timing-based reel mini-game mechanics.

## Features

### 🎣 Main Fishing Bot
- **Complete Automation**: Handles both casting and reel timing mini-game
- **Smart Reel Detection**: Automatically detects when timing mini-game appears
- **Perfect Timing**: Clicks reel button when circles align or indicator turns green
- **Customizable Settings**: Adjustable timing, sensitivity, and reaction delays
- **Safety Features**: Anti-detection measures and automatic breaks
- **Statistics Tracking**: Detailed session and overall statistics
- **User-friendly GUI**: Easy-to-use interface with multiple tabs

### 🎯 Timing Mini-Game Support
- **Circle Detection**: Recognizes shrinking and dotted blue circles
- **Green Timing**: Detects when timing indicator turns green
- **Reaction Delay**: Configurable delay to simulate human reaction time
- **Real-time Monitoring**: Live feedback on timing detection
- **Calibration Tools**: Specialized tester for fine-tuning detection

### 🛠️ Utility Tools
- **Coordinate Detector**: Easy setup of all game element positions
- **Screen Capture Tool**: Create templates for image recognition
- **Testing Tool**: Verify bot functionality and performance
- **Reel Timing Tester**: Specialized tool for calibrating timing detection

### ⚙️ Advanced Features
- **Profile Management**: Save and load different configurations
- **Hotkey Support**: Global hotkeys for easy control
- **Motion Detection**: Detect bobber movement and water effects
- **Color Detection**: Identify color changes for bite indicators
- **Template Matching**: Use custom images for UI element detection
- **Randomization**: Human-like behavior patterns
- **Emergency Stop**: Immediate halt functionality

## Installation

### Prerequisites
- Python 3.7 or higher
- Windows 10/11 (tested)
- Ragnarok X Next Generation installed

### Setup Steps

1. **Clone or Download** this repository to your desired location

2. **Install Required Packages**:
   ```bash
   pip install pyautogui opencv-python numpy pillow pynput psutil configparser
   ```

3. **Run the Launcher**:
   ```bash
   python launcher.py
   ```

## Quick Start Guide

### 1. Initial Setup
1. Start Ragnarok X Next Generation
2. Go to any fishing location
3. Open the fishing interface in the game
4. Set the game to windowed mode for better detection

### 2. Configure Coordinates
1. Launch the **Coordinate Detector** from the launcher
2. Set up all required positions:
   - **Cast Button**: Click "Detect" then click the fishing cast button in game
   - **Fishing Area**: Click "Detect" then click where you want to cast
   - **Reel Button**: Click "Detect" then click the reel/timing button
   - **Timing Area**: Click "Detect" then click center of the timing circles
3. Save the coordinates

### 3. Calibrate Reel Timing (Important!)
1. Launch the **Reel Timing Tester** from the launcher
2. Set timing area coordinates (center of timing circles)
3. Start monitoring and trigger a reel mini-game in the game
4. Adjust green detection threshold until it properly detects perfect timing
5. Test the detection accuracy

### 4. Start Fishing
1. Launch the **Main Fishing Bot**
2. Review settings in the Configuration tab
3. Adjust reel timing delay based on your reaction preference
4. Click "Start Fishing" or press F1
5. Monitor the activity log for status updates

## Fishing Mechanics

### Two-Step Process
Ragnarok X uses a timing-based fishing system:

1. **CAST PHASE**: 
   - Bot clicks the cast button
   - Bot clicks on the fishing area to cast the line

2. **REEL PHASE**:
   - Bot waits for the timing mini-game to appear
   - Bot detects when timing is perfect (green indicator or circle overlap)
   - Bot clicks the reel button at the optimal moment

## Configuration Options

### Coordinates
- **Cast Button**: Position of the fishing cast button
- **Fishing Area**: Where to cast the fishing line
- **Detection Region**: Area to monitor for bite indicators

### Timing Settings
- **Cast Delay**: Time between casts (randomizable)
- **Bite Timeout**: Maximum wait time for fish bite
- **Reaction Time**: Delay before hooking fish
- **Hook Duration**: How long to hold hook action

### Detection Settings
- **Hook Sensitivity**: Image matching threshold (0.5-1.0)
- **Motion Sensitivity**: Movement detection threshold
- **Color Detection**: Enable color-based bite detection
- **Template Matching**: Use custom image templates

### Safety Features
- **Randomize Timings**: Add variation to prevent detection
- **Anti-detection**: Enable human-like behavior
- **Break Intervals**: Automatic breaks during long sessions
- **Mouse Variation**: Random movement offsets

## Usage Tips

### For Best Results
- Use windowed mode in the game
- Ensure game window is visible (not minimized)
- Start with short test sessions
- Adjust sensitivity based on detection accuracy
- Create custom templates for better recognition

### Safety Recommendations
- Enable randomization features
- Take regular manual breaks
- Don't run for excessive periods
- Monitor bot activity periodically
- Follow game terms of service

## Hotkeys

- **F1**: Start/Resume fishing
- **F2**: Pause fishing
- **F3**: Stop fishing
- **F4**: Emergency stop (immediate halt)
- **F5**: Save debug screenshot (when available)

## File Structure

```
macroapp/
├── launcher.py           # Main launcher GUI
├── main.py              # Main fishing bot application
├── image_detector.py    # Image recognition and detection
├── config_manager.py    # Configuration management
├── utils.py            # Utility tools (coordinate detection, etc.)
├── config/             # Configuration files and profiles
├── templates/          # Image templates for detection
└── README.md           # This file
```

## Troubleshooting

### Common Issues

**Bot doesn't detect fish bites:**
- Increase hook sensitivity in settings
- Check fishing area coordinates
- Ensure game window is visible
- Create better bite indicator templates

**False positive detections:**
- Decrease hook sensitivity
- Adjust detection region size
- Disable conflicting detection methods

**Bot clicks wrong locations:**
- Re-detect coordinates using the coordinate tool
- Check screen resolution hasn't changed
- Verify game is in windowed mode

**Bot stops unexpectedly:**
- Check activity log for error messages
- Verify all required packages are installed
- Run system check from launcher

### Advanced Troubleshooting

1. **Use Testing Tools**: Run the testing tool to verify functionality
2. **Check Templates**: Ensure template images match current game graphics
3. **Debug Mode**: Enable debug info in interface settings
4. **Log Analysis**: Review activity log for specific error patterns

## Template Creation

### Creating Effective Templates
1. Use the Screen Capture Tool to capture game elements
2. Focus on unique, consistent visual indicators
3. Capture templates at different game states
4. Test templates with the testing tool

### Recommended Templates
- `bite_indicator.png` - Exclamation mark or bite symbol
- `bobber_splash.png` - Water splash effect
- `hook_icon.png` - Hook prompt button
- `cast_button.png` - Fishing cast button

## Safety and Legal Considerations

### Important Notes
- This tool is for educational and personal use
- Check your game's terms of service regarding automation
- Use responsibly and in moderation
- Take regular breaks to avoid detection
- Consider the impact on other players

### Anti-Detection Features
- Randomized timing patterns
- Variable mouse movements
- Simulated human breaks
- Configurable behavior patterns

## Contributing

### Reporting Issues
1. Use the built-in testing tools to gather information
2. Include your configuration settings
3. Provide activity log excerpts
4. Describe expected vs actual behavior

### Feature Requests
- Suggest improvements through issues
- Include specific use cases
- Consider compatibility impact

## Version History

### v1.0 (Current)
- Initial release
- Complete fishing automation
- Multi-detection system
- Profile management
- Utility tools suite
- Safety features

## License

This project is provided as-is for educational purposes. Use at your own risk and in compliance with applicable terms of service.

## Disclaimer

This software is not affiliated with or endorsed by Ragnarok X Next Generation or its developers. Use of automation tools may violate game terms of service. Users are responsible for compliance with all applicable rules and regulations.
#   m a c r o a p p  
 