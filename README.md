
# rwkmulti (RWK Multibox Client)

**rwkmulti** is a Python script designed to control multiple characters at once in **Race War Kingdoms**. It’s explicitly approved for use with this game, following its rules and restrictions.

## Disclaimer

This software is provided **"as is,"** with no warranties, express or implied. The author isn’t liable for any damages, data loss, or issues arising from its use. Run it at your own risk.

## Important Notes

- The main script is `rwkmulti.pyw`.
- Use the latest Firefox version to avoid a bug where pages scroll when keys are sent.
- Windows 11 users typically don’t need GeckoDriver—Selenium works directly with Firefox.

## What’s New

### Recent Updates & Fixes

**[Version 1.4.3]**
- **Key Rebinding:** Added support for rebinding keys (1:1 only) in the Config.  
  *Note:* `ignore_key` settings apply to the original key.  
  Example: if you rebind your "S" key to "C", you should ignore "S" for a fighter.

**[Version 1.4.2]**
- **Fixed Key-Sending Glitches:** No more missed keystrokes across windows.
- **Improved Key Queue:** Limits the queue to the last two pressed keys, preventing lag from rapid inputs.
- **Default Firefox Profile:** Optionally loads your main Firefox profile (with saved logins/cookies) instead of a temporary one. *(Thanks, Cagedangel!)*
- **Auto-Update Feature:** Checks for updates on startup and prompts to download if a newer version exists, preserving your config during updates.
- **Config Button & File:** A **Config** button opens an editor for `rwkmulti_settings.cfg`, storing your server URL, profile setting, and key ignore preferences.
- **Better Error Handling:** Popups guide you to install missing libraries (e.g., Selenium) if needed.


## Prerequisites

### Python 3
- [Download from python.org](https://www.python.org/downloads/).

### Python Libraries
Install via pip:

```bash
pip install selenium keyboard requests
```
- **`selenium`**: Drives Firefox automation.
- **`keyboard`**: Captures and sends keystrokes.
- **`requests`**: Enables auto-updates.

### Firefox Browser
- [Get the latest version from mozilla.org](https://www.mozilla.org/firefox/new/).

### GeckoDriver (Optional)
Only needed for older Windows versions. [Download from GitHub](https://github.com/mozilla/geckodriver/releases) and add to your PATH (e.g., `C:\Windows\System32`).

## Installation

1. Download `rwkmulti.pyw` and save it anywhere on your computer.
2. Double-click to run it.

## Usage

### Start the Script
- Launch `rwkmulti.pyw`.
- If an update’s available, you’ll get a prompt to download it.

### Set Up Windows
- Enter how many Firefox windows you want (default: 12).
- Optionally use your default Firefox profile for saved logins.

### GUI Controls
- **Start**: Opens your specified number of Firefox windows.
- **Pause/Resume**: Toggles keystroke broadcasting *(button text changes based on state)*.
- **Config**: Opens a window to edit settings *(or tweak `rwkmulti_settings.cfg` manually)*.
- **Copy Logs**: Copies the log output to your clipboard.

### Play the Game
- Log into Race War Kingdoms in each window.
- Keystrokes (e.g., arrows, letters) broadcast to all windows simultaneously.
- Close the GUI to exit.

## Configuration

Settings live in `rwkmulti_settings.cfg`, created on first run. Edit via the **Config** button or Notepad.

### Example Config File

```ini
[Settings]
# Server URL to connect to
server_url = https://r2p3.racewarkingdoms.com/
# Use default Firefox profile (0 = no, 1 = yes)
use_default_profile = 0
# Number of game windows to open
num_game_windows = 12
# Ignore keys by window title pattern (JSON format, e.g., {"Pattern": ["key1", "key2"]})
ignore_keys = {"Surzerker": ["c"], "Spongebob": ["a"]}
# Key rebinding (JSON format, e.g., {"c": "s", "s": "c"}) = 
key_rebindings = {"c": "s", "s": "c"}
```

- **Server URL:** Set your preferred Race War Kingdoms server.
- **Firefox Profile:** Toggle to `1` to use your main profile.
- **Number of Windows:** Adjust how many windows open.
- **Ignore Keys:** Define keys to block per window title *(e.g., `"Surzerker": ["c"]` stops `c` for titles containing "Surzerker")*. Edit the JSON to match your characters.
- **Key Rebindings:** Rules for rebinding single keys *(e.g., `"s": ["c"]` rebinds the `s` key to send `c` within the script. Edit the JSSON to add your own rebinds.

Changes persist across updates and apply on the next **Start** *(some, like profile settings, need a restart)*.

## Troubleshooting

- **Keys Scroll Pages:** Update Firefox to the latest version.
- **GeckoDriver Errors:** Rare on Windows 11; ensure Firefox is current.
- **Missing Libraries:** A popup will show install commands *(e.g., `pip install selenium`)*.
- **No Auto-Update:** Verify `requests` is installed.
- **Config Not Updating:** Edit in Notepad, save, then click **Config** to see changes—or restart the script.
- **Logs:** Check the GUI’s log for error details.

## License

MIT License—free to use, modify, and share.

## Support & Contributions

- **Help:** File an issue on the repo.
- **Contribute:** Submit pull requests with fixes or features.
