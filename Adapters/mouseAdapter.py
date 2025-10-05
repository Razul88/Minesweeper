import pyautogui

def MouseLeftClick(pixel_index):
    pyautogui.moveTo(pixel_index[0], pixel_index[1])
    pyautogui.leftClick()

def MouseRightClick(pixel_index):
    pyautogui.moveTo(pixel_index[0], pixel_index[1])
    pyautogui.rightClick()

def MouseMove(pixel_index):
    pyautogui.moveTo(pixel_index[0], pixel_index[1])