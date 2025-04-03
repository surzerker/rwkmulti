## Changelog
### [Version 1.5.8]

- **Firefox GPU Acceleration**: Firefox windows will now attempt to launch with hardware acceleration mode enabled to offload some page rendering to an available GPU.
- **Replaced Keyboard Library**: Replaced the windows-only "keyboard" library with pynput which is compatible with Linux and should dramatically improve performance.
- **Key Suppression**: Due to technical limitations and for added safety, keyboard inputs outside RWK are blocked unless rwkmulti is paused.

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
- **Default Firefox Profile:** Optionally loads your main Firefox profile (with saved logins/cookies) instead of a temporary one.
- **Auto-Update Feature:** Checks for updates on startup and prompts to download if a newer version is available.
- **Config Button & File:** A **Config** button opens an editor for `rwkmulti_settings.cfg`, storing your server URL, profile setting, and key ignore preferences.
- **Better Error Handling:** Popups guide you to install missing libraries (e.g., Selenium) if needed.
