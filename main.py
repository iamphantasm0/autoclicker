import pyautogui
import time
import threading
import keyboard
import random

# Define a flag to control the auto-clicker
running = False


def auto_click():
    global running
    while running:
        # Generate a random interval and duration
        interval = random.uniform(0.1, 0.5)  # Random interval between clicks
        duration = random.uniform(5, 10)  # Random duration to stay on this interval (in seconds)

        print(f"Using interval: {interval:.2f} seconds for the next {duration:.2f} seconds.")
        start_time = time.time()

        # Click repeatedly for the specified duration
        while running and (time.time() - start_time) < duration:
            pyautogui.click()
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

    # Register hotkeys
    keyboard.add_hotkey("ctrl+alt+s", start_clicking)
    keyboard.add_hotkey("ctrl+alt+x", stop_clicking)
    keyboard.add_hotkey("ctrl+alt+q", lambda: (stop_clicking(), exit()))

    print("Listening for hotkeys...")
    keyboard.wait("ctrl+alt+q")  # Keeps the program running


if __name__ == "__main__":
    main()
