# rwkmulti.py (version 0.1.1)
# Author: Surzerker (S2)
# This script allows you to control multiple characters simultaneously in Race War Kingdoms. It has been approved by Glitchless on 11/13/2023 with the stipulation that no additional logic can be included.
# If you encounter issues or need assistance setting up this script, please feel free to reach out.

# DISCLAIMER: This software is provided "as is" and comes without any warranties, express or implied. The author is not liable for any claims, damages, or other liabilities, whether in contract, tort, or otherwise, arising from, out of, or in connection with the software or its use. Use this script at your own risk, and be aware that the author is not responsible for any data loss, hardware damage, or other consequences that may result from using the software.

# Instructions:
# 1. Install Python 3: https://www.python.org/downloads/
# 2. Install the required Python packages:
#    - Run the command `pip install selenium keyboard`
# 3. Download the latest version of Firefox: https://www.mozilla.org/firefox/new/
# 4. Download the appropriate GeckoDriver for your Firefox version: https://github.com/mozilla/geckodriver/releases
# 5. Place the GeckoDriver executable in a directory that is included in your system's PATH (e.g., C:\windows\system32\).

# To run the script, open the directory containing this Python script (rwkmulti.py) in the Command Prompt (CMD) and enter the command: `python rwkmulti.py`.
# After running the script, the specified number of Firefox windows will be launched automatically.
# Log into RWK in each Firefox window by copying and pasting your username(s) and password(s) into RWK from notepad (or using saved passwords in Firefox) and then clicking submit.


# Import necessary libraries
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import keyboard
from selenium.webdriver.common.keys import Keys

# Set the number of game windows you want to control (default: 2)
num_game_windows = 2

# Create a list to store the driver instances
drivers = []

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

# Function to send keys to specified drivers
def send_keys_to_drivers(drivers, input_key):
    for driver in drivers:
        driver.find_element(By.TAG_NAME, 'body').send_keys(input_key)
        # Send the HOME key to counteract Selenium's scrolling to the page
        driver.find_element(By.TAG_NAME, 'body').send_keys(Keys.HOME)

while True:
    input_key = keyboard.read_event().name
    if input_key == 'q':
        break
    send_keys_to_drivers(drivers, input_key)

# Close the drivers when done
for driver in drivers:
    driver.quit()
