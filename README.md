# rwkmulti (RWK Multibox Client)

**rwkmulti** is a Python script designed to control multiple characters at once in **Race War Kingdoms**. It’s explicitly approved for use with this game, following its rules and restrictions.

## Disclaimer

This software is provided **"as is,"** with no warranties, express or implied. The author isn’t liable for any damages, data loss, or issues arising from its use. Run it at your own risk.

## Important Notes

- The main script is `rwkmulti.pyw`.
- Use the latest Firefox version to avoid a bug where pages scroll when keys are sent.
- Windows 11 users typically don’t need GeckoDriver—Selenium works directly with Firefox.

## What’s New
### [Version 1.5.8]

- **Firefox GPU Acceleration**: Firefox windows will now attempt to launch with hardware acceleration mode enabled to offload some page rendering to an available GPU.
- **Replaced Keyboard Library**: Replaced the windows-only "keyboard" library with pynput which is compatible with Linux and should dramatically improve performance.

### [Versions 1.4.4 to 1.5.7]

- **Auto-Arrange Checkbox**: Toggle auto-positioning of windows in a grid layout.
- **Auto-Arrange JSON Layout**: Define specific layout with monitor, rows, columns, and position.
- **Horizontal and Vertical Offsets**: Adjust individual window sizes and placement for fine-tuning layout.
- **Clear Temp Data Button**: Frees disk space by removing old Selenium profiles.
- **Checksum Mismatch Update Mechanism**: Verifies updates even if version numbers match, using SHA-256.

### [Version 1.4.3]

- **Key Rebinding:** Added support for rebinding keys (1:1 only) in the Config.  
  *Note:* `ignore_key` settings apply to the original key.  
  Example: if you rebind your "S" key to "C", you should ignore "S" for a fighter.

### [Version 1.4.2]

- **Fixed Key-Sending Glitches:** No more missed keystrokes across windows.
- **Improved Key Queue:** Limits the queue to the last two pressed keys, preventing lag from rapid inputs.
- **Default Firefox Profile:** Optionally loads your main Firefox profile (with saved logins/cookies) instead of a temporary one. *(Thanks, Cagedangel!)*
- **Auto-Update Feature:** Checks for updates on startup and prompts to download if a newer version exists, preserving your config during updates.
- **Config Button & File:** A **Config** button opens an editor for `rwkmulti_settings.cfg`, storing your server URL, profile setting, and key ignore preferences.
- **Better Error Handling:** Popups guide you to install missing libraries (e.g., Selenium) if needed.

## Prerequisites

### Python 3
- [Download from python.org](https://www.python.org/downloads/)

### Python Libraries
Install via pip:

```bash
pip install selenium pynput requests
```

- **`selenium`**: Drives Firefox automation.
- **`pynput`**: Captures and sends keystrokes.
- **`requests`**: Enables auto-updates.

### Firefox Browser
- [Get the latest version from mozilla.org](https://www.mozilla.org/firefox/new/)

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
- **Clear Temp Data**: Removes old Selenium profile folders to save space.
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
# Ignore keys by window title pattern (JSON format)
ignore_keys = {"Surzerker": ["c"], "Spongebob": ["a"]}
# Key rebinding (JSON format)
key_rebindings = {"c": "s", "s": "c"}
# Enable auto-arrange grid layout
auto_arrange = 1
# Horizontal/vertical offsets
window_border_offset_horizontal = 16
window_border_offset_vertical = -30
# Window layout config (JSON)
window_layouts = {
  "0": [1, 3, 5, 1],
  "1": [1, 3, 5, 2],
  "14": [1, 3, 5, 15]
}
```

- **Key Rebindings:** `"s": "c"` remaps the `s` key to send `c`. Only 1:1 bindings supported.
- **Auto-Arrange:** When enabled (`1`), applies layout grid using `window_layouts`.
- **Offsets:** Adjust window sizing/placement in pixels.
- **Window Layouts:** `"0": [1, 3, 5, 1]` → monitor 1, 3 rows, 5 cols, position 1.

## Troubleshooting

- **Keys Scroll Pages:** Update Firefox.
- **GeckoDriver Issues:** Usually unnecessary on Windows 11.
- **Missing Libraries:** Install via pip.
- **No Auto-Update:** Ensure `requests` is installed.
- **Config Not Saving:** Edit manually, then restart or re-open Config window.
- **Checksum Mismatch Prompt:** Accept update if prompted after launch.

## License

MIT License—free to use, modify, and share.

## Support & Contributions

- **Need Help?** File an issue on the repo.
- **Want to Contribute?** Submit pull requests with improvements or bugfixes.
