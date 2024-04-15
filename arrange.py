import pygetwindow as gw
import pyautogui
import time

def tile_windows(layout):
    screensize = pyautogui.size()
    windows = gw.getWindowsWithTitle('Mozilla Firefox')

    if len(windows) < len(layout):
        print("Not enough windows to match the layout")
        return

    if layout == '2x2':
        width = screensize.width // 2
        height = screensize.height // 2
        positions = [(0, 0), (width, 0), (0, height), (width, height)]
    elif layout == '4x1':
        width = screensize.width // 4
        height = screensize.height
        positions = [(i * width, 0) for i in range(4)]
    else:
        print("Unsupported layout")
        return

    for win, pos in zip(windows, positions):
        win.moveTo(pos[0], pos[1])
        win.resizeTo(width, height)

# Example usage
layout = '4x1'  # Choose '2x2' or '4x1'
tile_windows(layout)
