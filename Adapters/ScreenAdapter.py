from PIL import ImageGrab

def ScreenShot(start_x, start_y, width, height):
    screenshot = ImageGrab.grab(bbox=(start_x, start_y, start_x + width, start_y + height))
    return screenshot