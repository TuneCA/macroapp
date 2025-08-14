from pyautogui import *
import pyautogui
import time

# Disable ImageNotFoundException - return None instead of raising exception
pyautogui.useImageNotFoundException(False)

class Fishing:
    def __init__(self, max_fishing):
        self.max_fishing = max_fishing
        self.position = 0
        self.amount = 0

    def throw(self):
        throw_position = pyautogui.locateCenterOnScreen('image/cast.png', confidence=.9, region=(1422, 674,200, 200))
        if throw_position != None:
            btnThrow = pyautogui.moveTo(throw_position)
            pyautogui.click(btnThrow)
            print("cast!")
            print("Tunggu...")
            self.position = 1

    def wait_for_reel(self):
        """Continuously monitor for reel button to appear and click immediately"""
        print("Waiting for reel button to appear...")
        max_wait_time = 30  # Maximum wait time in seconds (adjust as needed)
        start_time = time.time()
        
        while time.time() - start_time < max_wait_time:
            # Check for reel button every 0.1 seconds for quick response
            pull_position = pyautogui.locateCenterOnScreen('image/reel.png', confidence=.95, region=(1422, 674,200, 200))
            if pull_position != None:
                btnPull = pyautogui.moveTo(pull_position)
                pyautogui.click(btnPull)
                print("reel!")
                self.amount += 1
                print("Dapat ikan ", self.amount)
                self.position = 0
                return True
            
            # Small delay to prevent excessive CPU usage but still be responsive
            time.sleep(0.1)
        
        # Timeout - reel button didn't appear
        print("Timeout waiting for reel button, resetting to cast")
        self.position = 0
        return False

    def fishing(self):
        while True:
            if self.amount >= self.max_fishing:
                break
            elif self.position == 0:
                self.throw()
            elif self.position == 1:
                self.wait_for_reel()

if __name__ == "__main__":
    print("Mulai memancing")
    
    max_fishing = 10
    
    letsgo = Fishing(max_fishing)
    letsgo.fishing()