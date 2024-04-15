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
    elif layout == '2x3':
        width = screensize.width // 2
        height = screensize.height // 3
        positions = [(0, 0), (width, 0), (0, height), (width, height), (0, 2 * height), (width, 2 * height)]
    elif layout == '3x2':
        width = screensize.width // 3
        height = screensize.height // 2
        positions = [(0, 0), (width, 0), (2 * width, 0), (0, height), (width, height), (2 * width, height)]
    elif layout == '4x1':
        width = screensize.width // 4
        height = screensize.height
        positions = [(i * width, 0) for i in range(4)]
    elif layout == '6x1':
        width = screensize.width // 6
        height = screensize.height
        positions = [(i * width, 0) for i in range(6)]
    else:
        print("Unsupported layout")
        return

    for win, pos in zip(windows, positions):
        win.moveTo(pos[0], pos[1])
        win.resizeTo(width, height)

# Example usage
layout = '4x1'  # Choose '2x2', '2x3', '3x2', '4x1' or '6x1'
tile_windows(layout)
