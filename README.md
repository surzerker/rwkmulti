
# rwkmulti (RWK Multibox Client)

rwkmulti is a Python script that allows you to control multiple characters simultaneously in the game Race War Kingdoms. This utility has been specifically approved for use with this game, adhering to its guidelines and restrictions.

## Disclaimer

This software is provided "as is," without warranty of any kind, express or implied. In no event shall the author be liable for any claim, damages, or other liabilities, whether in an action of contract, tort, or otherwise, arising from, out of, or in connection with the software or the use or other dealings in the software. Use this script at your own risk. The author is not responsible for any data loss, hardware damage, or other consequences that may result from the software's use.

## Important Notes

- **Use the latest version of Firefox:** A bug in older Firefox versions causes pages to scroll when keys are sent. Updating Firefox resolves this issue.
- **Windows 11 Users:** You typically do **not** need to install GeckoDriver separately, as Selenium integrates directly with Firefox.
- **Script File:** The script file is named `rwkmulti_v4.pyw` and launches the GUI without opening a command prompt or terminal.

## Prerequisites

Before running this script, ensure the following are installed:

1. **Python 3:**  
   [Download Python 3](https://www.python.org/downloads/).

2. **Required Python Libraries:**  
   Install these with pip3:
   ```sh
   pip3 install selenium keyboard
   ```

3. **Firefox Browser:**  
   [Download Firefox](https://www.mozilla.org/firefox/new/) and ensure it's updated to the latest version.

4. **GeckoDriver (if necessary):**  
   Only required for older Windows versions. [Download GeckoDriver](https://github.com/mozilla/geckodriver/releases). Place the executable in a PATH directory, such as `C:\Windows\system32`.

## Installation

Simply download the `rwkmulti_v4.pyw` file and place it anywhere convenient on your computer.

## Usage

1. Double-click `rwkmulti_v4.pyw` to launch the GUI.

2. The GUI allows you to:
   - Set the number of game windows.
   - Start, pause, or resume your multibox session.
   - Copy logs for troubleshooting.

3. Log into Race War Kingdoms in each Firefox window opened by the script.

4. Your keystrokes will be broadcast simultaneously to all windows:
   - Click the "Resume/Pause" button to toggle pause mode.
   - Close the application by closing the GUI window.

## Configuration

### Customizing Ignored Keys

The script supports selective ignoring of keystrokes for specific characters. Edit line 77 (approximately) in `rwkmulti_v4.pyw`:

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

Update this dictionary to suit your needs.

## Troubleshooting

- **Pages scrolling when keys are sent:** Update Firefox.
- **GeckoDriver not found (Windows 11):** Generally unnecessary; ensure Firefox is updated.
- **Other Issues:** Ensure all prerequisites are installed and review GUI logs.

## License

This project is licensed under the MIT License.

## Support and Contributions

- **Need Help?** Open an issue on GitHub.
- **Want to Contribute?** Submit pull requests with improvements.

Thank you for using rwkmulti!
