import pyautogui
import time
import threading
import keyboard
import random
import logging
import os

# Set up logging to log intervals and durations to a file
logging.basicConfig(filename='clicker_log.txt', level=logging.INFO, format='%(asctime)s - %(message)s')

# Define a flag to control the auto-clicker
running = False
total_clicks_file = 'total_clicks.txt'

# Function to read the total clicks from the file (or initialize to 0 if it doesn't exist)
def read_total_clicks():
    if os.path.exists(total_clicks_file):
        with open(total_clicks_file, 'r') as f:
            return int(f.read().strip())
    else:
        return 0

# Function to save the total clicks to a file
def save_total_clicks(total_clicks):
    with open(total_clicks_file, 'w') as f:
        f.write(str(total_clicks))

# Initialize the total clicks count
total_clicks = read_total_clicks()

def auto_click():
    global running, total_clicks
    while running:
        # Generate a random interval and duration
        interval = random.uniform(0.1, 0.5)  # Random interval between clicks
        duration = random.uniform(5, 10)    # Random duration to stay on this interval (in seconds)
        
        # Log the generated interval and duration to a file
        logging.info(f"Using interval: {interval:.2f} seconds for the next {duration:.2f} seconds.")
        
        # Print the generated interval and duration to the console
        print(f"Using interval: {interval:.2f} seconds for the next {duration:.2f} seconds.")
        
        start_time = time.time()

        # Click repeatedly for the specified duration
        while running and (time.time() - start_time) < duration:
            pyautogui.click()
            total_clicks += 1  # Increment the total click count
            save_total_clicks(total_clicks)  # Save the updated click count to the file
            time.sleep(interval)

def start_clicking():
    global running
    if not running:
        running = True
        threading.Thread(target=auto_click).start()
        print("Auto-clicker started...")

def stop_clicking():
    global running
    running = False
    print("Auto-clicker stopped...")

def main():
    print("Advanced Random Interval Auto Clicker")
    print("Press 'Ctrl+Alt+S' to start clicking.")
    print("Press 'Ctrl+Alt+X' to stop clicking.")
    print("Press 'Ctrl+Alt+Q' to quit the program.")
    print(f"Total clicks so far: {total_clicks}")

    # Register hotkeys
    keyboard.add_hotkey("ctrl+alt+s", start_clicking)
    keyboard.add_hotkey("ctrl+alt+x", stop_clicking)
    keyboard.add_hotkey("ctrl+alt+q", lambda: (stop_clicking(), exit()))

    print("Listening for hotkeys...")
    keyboard.wait("ctrl+alt+q")  # Keeps the program running

if __name__ == "__main__":
    main()
