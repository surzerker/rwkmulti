
# rwkmulti (RWK Multibox Client)

rwkmulti is a Python script that allows you to control multiple characters simultaneously in the game Race War Kingdoms. This utility has been specifically approved for use with this game, adhering to its guidelines and restrictions.

## Disclaimer

This software is provided "as is," without warranty of any kind, express or implied. In no event shall the author be liable for any claim, damages, or other liabilities, whether in an action of contract, tort, or otherwise, arising from, out of, or in connection with the software or the use or other dealings in the software. Use this script at your own risk. The author is not responsible for any data loss, hardware damage, or other consequences that may result from the software's use.

## Important Notes

- **Use the latest version of Firefox:** A bug in older Firefox versions causes pages to scroll when keys are sent. Updating Firefox resolves this issue.
- **Windows 11 Users:** You typically do **not** need to install GeckoDriver separately, as Selenium integrates directly with Firefox.
- **Script File Update:** The script has been changed to a `.pyw` file, which launches the GUI without opening a command prompt or terminal window.

## Prerequisites

Before running this script, ensure the following are installed:

1. **Python 3:**  
   [Download Python 3](https://www.python.org/downloads/).

2. **Required Python Libraries:**  
   Install these with pip:
   ```sh
   pip install selenium keyboard
   ```

3. **Firefox Browser:**  
   [Download Firefox](https://www.mozilla.org/firefox/new/) and ensure it's updated to the latest version.

4. **GeckoDriver (if necessary):**  
   If you're using an OS or setup where GeckoDriver is required (typically older Windows versions), download it from the [official repository](https://github.com/mozilla/geckodriver/releases). Place the executable in a system PATH directory, such as `C:\Windows\system32`.

## Installation

Follow these steps to set up RWK Multibox Client:

1. **Clone the Repository:**
   ```sh
   git clone https://github.com/yourusername/rwkmulti.git
   cd rwkmulti
   ```

2. **Install Dependencies:**
   ```sh
   pip install -r requirements.txt
   ```

3. **Run the Script:**
   ```sh
   pythonw rwkmulti.pyw
   ```

## Usage

1. **Launching and GUI Controls:**  
   Running the script opens a GUI where you can:
   - Set the number of game windows.
   - Start, pause, or resume your multibox session.
   - Copy logs for troubleshooting.

2. **Gameplay Instructions:**  
   After launching, the script opens multiple Firefox windows. Log into Race War Kingdoms in each window. Your keystrokes will broadcast simultaneously to all windows.

   - Use `CTRL+.` to toggle pause mode, stopping key broadcasts temporarily.
   - To close the application, exit from the GUI.

## Configuration

### Customizing Ignored Keys

The script supports selective ignoring of keystrokes for specific characters. Edit line 77 (approximately) in `rwkmulti.pyw`:

```python
self.ignore_keys = {
    "Surzerker": ["c"],
    "Cid": ["c"],
    "Spongebob": ["a"],
    "Buu": ["a"]
    # Add custom character key ignores below, e.g.:
    # "YourCharacterName": ["key1", "key2"]
}
```

Update this dictionary to suit your needs, adding or removing keys as desired.

## Troubleshooting

- **Pages scrolling when keys are sent:**  
  Update Firefox to the latest version.

- **GeckoDriver not found (Windows 11):**  
  Generally, GeckoDriver is not needed. If issues persist, double-check your Firefox installation.

- **General issues:**  
  Confirm all dependencies are installed, review logs within the GUI, and check for conflicts with security software.

## License

This project is licensed under the MIT License. See the `LICENSE` file included in this repository.

## Support and Contributions

- **Need Help?** Open an issue in the GitHub repository.
- **Want to Contribute?** Fork the repository and submit pull requests to contribute improvements.

Thank you for using rwkmulti!
