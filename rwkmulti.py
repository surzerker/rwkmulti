# rwkmulti.py (version 0.3.2)
# Author: Surzerker (S2)
# This script allows you to control multiple characters simultaneously in Race War Kingdoms. It has been approved by Glitchless on 11/13/2023 with the stipulation that no additional logic can be included.
# If you encounter issues or need assistance setting up this script, please feel free to reach out.

# DISCLAIMER: This software is provided "as is" and comes without any warranties, express or implied. The author is not liable for any claims, damages, or other liabilities, whether in contract, tort, or otherwise, arising from, out of, or in connection with the software or its use. Use this script at your own risk, and be aware that the author is not responsible for any data loss, hardware damage, or other consequences that may result from using the software.

# Instructions:
# 1. Install Python 3: https://www.python.org/downloads/
# 2. Install the required Python packages:
#    - Run the command `pip install selenium keyboard`
#3. Download Firefox: If you don't have Firefox installed, you can download the latest version from [here](https://www.mozilla.org/firefox/new/).
#4 .Download GeckoDriver: To use the script, you'll need the appropriate version of GeckoDriver for your Firefox installation. You can download it from [here](https://github.com/mozilla/geckodriver/releases).
#   - Add GeckoDriver to Your System's PATH: Place the downloaded GeckoDriver executable in a directory that is included in your system's PATH. For example, you can copy it to C:\windows\system32\.   I had to actually download the 32 bit version and put it in my systemwow32 folder

# To run the script, open the directory containing this Python script (rwkmulti.py) in the Command Prompt (CMD) and enter the command: `python rwkmulti.py`.
# After running the script, the specified number of Firefox windows will be launched automatically.
# Log into RWK in each Firefox window by copying and pasting your username(s) and password(s) into RWK from notepad (or using saved passwords in Firefox) and then clicking submit.


from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import keyboard
from selenium.webdriver.common.keys import Keys

print("\n ☺️ RWK Multibox Client started...\n (Wait for all browser windows to open before taking any action.)\n\n Press the CTRL and period keys simultaneously [CTRL+.] to PAUSE/UNPAUSE broadcasting of keys to browser windows.\n To exit this application, close the command terminal or type [CTRL+C].\n")

# Set the number of game windows you want to control (default: 4)
num_game_windows = 4

# Create a list to store the driver instances
drivers = []

# Create a dictionary to keep track of key states for each driver
key_states = {driver: {} for driver in drivers}

# Variable to track whether the application is paused
is_paused = False

# Create the specified number of Firefox browser instances
for i in range(num_game_windows):
    driver = webdriver.Firefox()
    drivers.append(driver)

# Open the URL in each window
url = "https://rwk2.racewarkingdoms.com/"
for driver in drivers:
    driver.get(url)

# Wait for each window to load and get its handle
for driver in drivers:
    wait = WebDriverWait(driver, 10)
    wait.until(EC.presence_of_element_located((By.TAG_NAME, 'body')))
    key_states[driver] = {}  # Initialize key states for each driver

special_keys_map = {
    'up': Keys.ARROW_UP,
    'down': Keys.ARROW_DOWN,
    'left': Keys.ARROW_LEFT,
    'right': Keys.ARROW_RIGHT,
    # Add more mappings as needed
}

def send_keys_to_drivers(drivers, input_key):
    if is_paused:
        return  # Do not send keys if the application is paused
    
    selenium_key = special_keys_map.get(input_key, input_key)  # Map to Selenium key if special, else use as is
    for driver in drivers:
        if input_key not in key_states[driver] or not key_states[driver][input_key]:
            driver.find_element(By.TAG_NAME, 'body').send_keys(selenium_key)
            key_states[driver][input_key] = True

# Main loop
while True:
    event = keyboard.read_event()
    input_key = event.name

    if event.event_type == keyboard.KEY_DOWN and input_key == '.' and keyboard.is_pressed('ctrl'):
        is_paused = not is_paused  # Toggle pause state
        state = "paused" if is_paused else "unpaused"
        print(f"Application is now {state}.")
    elif not is_paused and event.event_type == keyboard.KEY_DOWN:
        send_keys_to_drivers(drivers, input_key)
    elif event.event_type == keyboard.KEY_UP and not is_paused:
        for driver in drivers:
            key_states[driver][input_key] = False

    ##Graceful exit can be bound to a key below.
    #if input_key == 'q':
    #    break

# Close the drivers when done
for driver in drivers:
    driver.quit()
