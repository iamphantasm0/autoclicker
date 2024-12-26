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

# Custom function to log and print messages
def log_and_print(message):
    logging.info(message)
    print(message)

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

# Function to simulate a human-like click (minimal movement)
def simulate_human_click():
    # Simulate mouse click at a fixed position (no extra movement)
    x, y = 500, 500  # Adjust these values to your target position
    pyautogui.moveTo(x, y, duration=random.uniform(0.002, 0.005))  # Very minimal movement to prevent shaking

    # Add a small random delay before clicking to mimic human behavior
    time.sleep(random.uniform(0.01, 0.03))  # Slight delay before clicking

    # Simulate mouse down and up
    pyautogui.mouseDown()
    time.sleep(random.uniform(0.01, 0.03))  # Slight delay between down and up
    pyautogui.mouseUp()

    log_and_print(f"Clicked at ({x}, {y})")

def auto_click():
    global running, total_clicks
    last_break_time = time.time()  # Track the last time a break was taken
    min_time_between_breaks = 15  # Reduce minimum time between breaks in seconds

    try:
        while running:
            # Generate a random interval and duration
            interval = random.uniform(0.01, 0.05)  # Faster random interval between clicks (0.01 to 0.05 seconds)
            duration = random.uniform(2, 5)        # Shorter duration to stay on this interval (in seconds)
            
            log_and_print(f"Using interval: {interval:.2f} seconds for the next {duration:.2f} seconds.")
            
            start_time = time.time()

            # Click repeatedly for the specified duration
            while running and (time.time() - start_time) < duration:
                if (time.time() - last_break_time) > min_time_between_breaks and random.random() < 0.1:  # 10% chance
                    break_duration = random.uniform(1, 3)  # Shorter break duration (1 to 3 seconds)
                    log_and_print(f"Taking a break for {break_duration:.2f} seconds.")
                    time.sleep(break_duration)
                    last_break_time = time.time()  # Update the last break time

                # Perform the human-like click
                simulate_human_click()
                total_clicks += 1
                save_total_clicks(total_clicks)  # Save the updated click count to the file
                time.sleep(interval)
    except KeyboardInterrupt:
        log_and_print("Auto-clicker interrupted.")
    finally:
        log_and_print("Auto-clicker stopped cleanly.")  # Ensures clean exit

def start_clicking():
    global running
    if not running:
        running = True
        threading.Thread(target=auto_click, daemon=True).start()
        log_and_print("Auto-clicker started...")

def stop_clicking():
    global running
    if running:
        running = False
        log_and_print("Stopping auto-clicker...")
        # Move mouse slightly to "unstick" it
        pyautogui.moveRel(10, 10, duration=0.2)
        log_and_print("Mouse moved to unstick.")

def main():
    log_and_print("Advanced Random Interval Auto Clicker with Minimal Mouse Movement and Faster Clicks")
    log_and_print("Press 'Ctrl+Alt+S' to start clicking.")
    log_and_print("Press 'Ctrl+Alt+X' to stop clicking.")
    log_and_print("Press 'Ctrl+Alt+Q' to quit the program.")
    log_and_print(f"Total clicks so far: {total_clicks}")

    # Register hotkeys
    keyboard.add_hotkey("ctrl+alt+s", start_clicking)
    keyboard.add_hotkey("ctrl+alt+x", stop_clicking)
    keyboard.add_hotkey("ctrl+alt+q", lambda: (stop_clicking(), exit()))

    log_and_print("Listening for hotkeys...")
    keyboard.wait("ctrl+alt+q")  # Keeps the program running

if __name__ == "__main__":
    main()
