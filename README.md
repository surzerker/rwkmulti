# rwkmulti (RWK Multibox Client)

rwkmulti is a Python script that allows you to control multiple characters simultaneously in the game Race War Kingdoms. This utility has been specifically approved for use with this game, adhering to its guidelines and restrictions.

## Disclaimer

This software is provided "as is," without warranty of any kind, express or implied. In no event shall the author be liable for any claim, damages, or other liabilities, whether in an action of contract, tort, or otherwise, arising from, out of, or in connection with the software or the use or other dealings in the software. Use this script at your own risk. The author is not responsible for any data loss, hardware damage, or other consequences that may result from the software's use.

## Prerequisites

Before you can use this script, you need to ensure that your system meets the following requirements:

1. **Python 3:** The script is written in Python and requires Python 3 to run. If you don't have Python 3 installed, download and install it from [https://www.python.org/downloads/](https://www.python.org/downloads/).

2. **Selenium and Keyboard Libraries:** The script uses Selenium for browser automation and the Keyboard library to listen to keyboard events. Install them using pip:

   ```
   pip install selenium keyboard
   ```

3. **Firefox Browser:** The script is designed to work with Mozilla Firefox. If you don't have Firefox installed, download it from [https://www.mozilla.org/firefox/new/](https://www.mozilla.org/firefox/new/).

4. **GeckoDriver:** You need the GeckoDriver to interface with Firefox through Selenium. Download the appropriate version for your system from [https://github.com/mozilla/geckodriver/releases](https://github.com/mozilla/geckodriver/releases). After downloading, extract the executable and place it in a directory included in your system's PATH, such as `C:\Windows\system32` on Windows.

## Installation

To set up the RWK Multibox Client, follow these steps:

1. Clone or download the repository to your local machine.

2. Open a terminal or command prompt window and navigate to the directory where you saved the script.

3. Ensure that you have completed all the prerequisite steps, including installing Python 3, Selenium, the Keyboard library, Firefox, and GeckoDriver.

## Usage

To run the script, follow these steps:

1. Open a command prompt or terminal window.

2. Navigate to the directory containing `rwkmulti.py`.

3. Execute the script by running:

   ```
   python rwkmulti.py
   ```

4. The script will launch the specified number of Firefox windows and navigate to the Race War Kingdoms login page.

5. Log into RWK in each Firefox window.

6. Once logged in, you can control all characters simultaneously using your keyboard. Press `CTRL+P` to toggle the pause mode, which allows you to temporarily stop broadcasting keystrokes to the game windows.

7. To exit the script, press `CTRL+C` in the command terminal or close the command terminal.

## Support

If you encounter any issues or require assistance, please feel free to open an issue on the GitHub repository.

Thank you for using rwkmulti!
