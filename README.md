# rwkmulti (RWK Multibox Client)

rwkmulti is a Python script that allows you to control multiple characters simultaneously in the game Race War Kingdoms. This utility has been specifically approved for use with this game, adhering to its guidelines and restrictions.

## Disclaimer

This software is provided "as is," without warranty of any kind, express or implied. In no event shall the author be liable for any claim, damages, or other liabilities, whether in an action of contract, tort, or otherwise, arising from, out of, or in connection with the software or the use or other dealings in the software. Use this script at your own risk. The author is not responsible for any data loss, hardware damage, or other consequences that may result from the software's use.

## Important Notes

- **We now use `rwkmulti-latest.pyw` as the main script.**
- **Use the latest version of Firefox:** A bug in older Firefox versions causes pages to scroll when keys are sent. Updating Firefox resolves this.
- **Windows 11 Users:** You typically do **not** need to install GeckoDriver separately, as Selenium integrates directly with Firefox.

## What's New

### Recent Changes & Bugfixes
1. **Fixed occasional key-sending failure:** Resolved a bug that sometimes prevented keystrokes from being sent to all windows.
2. **Key queue improvement:** Previously, if too many keys were pressed rapidly, the script would lag or hang. It now keeps only the last two pressed keys in the queue, preventing the buildup that caused the slowdown.
3. **Load default Firefox profile:**  
   - By default, the script can now load your main Firefox profile instead of creating a temporary profile. This lets you use saved credentials, cookies, and other profile-specific data. Special thanks to Cagedangel for this feature suggestion!
4. **New naming convention:** The script is now named `rwkmulti-latest.pyw` to accomodate the new auto-update feature.
5. **Auto-update support:**  
   - At startup, the script checks if a newer version is available and offers to download it if you’re out-of-date.
   - Prevents overwriting of user-specific config files during the update process.
6. **Config button & config file (`rwkmulti_settings.cfg`):**  
   - A new button in the GUI opens a config panel or edits the text file.
   - Stores the user’s preferred server URL, default Firefox profile setting, and key ignore settings so they persist between updates.
7. **Additional error handling:** If any required Python library is not installed, the script shows a popup explaining how to install the missing dependencies (e.g., Selenium, Keyboard, Requests).

## Prerequisites

1. **Python 3**  
   [Download Python 3](https://www.python.org/downloads/).

2. **Required Python Libraries**  
   Install these with pip (or pip3, depending on your setup):
   ```sh
   pip install selenium keyboard requests
   ```
   - **`selenium`**: Automates Firefox
   - **`keyboard`**: Detects and broadcasts keystrokes
   - **`requests`**: Required for auto-update checks

3. **Firefox Browser**  
   [Download Firefox](https://www.mozilla.org/firefox/new/) and ensure it's updated to the latest version.

4. **GeckoDriver (if necessary)**  
   Only required for older Windows versions. [Download GeckoDriver](https://github.com/mozilla/geckodriver/releases). Place the executable in a directory on your system PATH (e.g., `C:\Windows\system32`).

## Installation

1. Download `rwkmulti-latest.pyw` and place it anywhere convenient on your computer.
2. Double-click `rwkmulti-latest.pyw` to launch the GUI.

## Usage

1. **Launch the script**  
   - Double-click `rwkmulti-latest.pyw`.  
   - If an update is available, you’ll be prompted to download it.

2. **Configuring Windows**  
   - Enter the number of Firefox windows to open.
   - The script can automatically load your primary Firefox profile, using existing credentials and cookies (if configured).

3. **Control Panel Buttons**  
   - **Start**: Opens the specified number of Firefox windows.
   - **Resume/Pause**: Toggles broadcasting keystrokes.
   - **Config**: Opens a config panel (or automatically edits the `rwkmulti_settings.cfg` file).

4. **Gameplay**  
   - Log into Race War Kingdoms in each opened Firefox window.
   - Your keystrokes will be broadcast simultaneously to all windows.  
   - Close by exiting the GUI or stopping the program.

## Configuration

### Customizing Ignored Keys per Character

Your ignore settings are stored in the `rwkmulti_settings.cfg` file (or you can access them through the Config button in the GUI). This file includes lines that specify which keys should be ignored for each character, for example:

```
[IgnoreKeys]
Surzerker = c
Cid = c
Spongebob = a
Buu = a
```

Adjust these lines as needed to suit your preferences.

### Server URL & Profile Settings

The `rwkmulti_settings.cfg` file also lets you set:
- **Server URL**: The Race War Kingdoms server or environment you want to launch.
- **Default Firefox Profile**: By specifying this, the script won’t create a new temporary profile.

These settings persist even if you update the script using the auto-updater.

## Troubleshooting

- **Keystroke scrolling in Firefox**: Update Firefox.
- **GeckoDriver not found (Windows 11)**: Rarely needed; ensure Firefox is up to date.
- **Missing libraries**: If you encounter an error, a popup should appear explaining how to install the missing library via pip.
- **Script won’t auto-update**: Ensure you have the `requests` library installed.  
- **Still stuck?**: Check the GUI log output for more details, or edit the config file manually.

## License

This project is licensed under the MIT License.

## Support and Contributions

- **Need Help?** Open an issue in the project’s repository.
- **Want to Contribute?** Submit pull requests with improvements or bugfixes.

Thank you for using rwkmulti!
