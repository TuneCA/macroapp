import pyautogui

print("Move your mouse to find coordinates for your fishing bot.")
print("Press Ctrl+C when done.")
print("-" * 50)

try:
    pyautogui.displayMousePosition()
except KeyboardInterrupt:
    print("\nDone finding coordinates!")