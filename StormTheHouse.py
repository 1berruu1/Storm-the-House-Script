from PIL import ImageFilter, ImageEnhance, Image, ImageChops, ImageStat
from pyautogui import *
import pyautogui
import time
import keyboard
import win32api
import win32con
import pytesseract


#You need to have Tesseact installed and give the install path below
pytesseract.pytesseract.tesseract_cmd = r'Tesseract Path'

# pyautogui.displayMousePosition(1920,1080)
# top left corner 1714 854
# bottom right 1114 250


time.sleep(2)


# main game : 340, 230, 600, 600
# ammo : 340, 230, 300, 30

def click(x, y):
    win32api.SetCursorPos((x, y))
    win32api.mouse_event(win32con.MOUSEEVENTF_LEFTDOWN, 0, 0)
    win32api.mouse_event(win32con.MOUSEEVENTF_LEFTUP, 0, 0)


def double_click(x, y):
    win32api.SetCursorPos((x, y))
    win32api.mouse_event(win32con.MOUSEEVENTF_LEFTDOWN, 0, 0)
    win32api.mouse_event(win32con.MOUSEEVENTF_LEFTUP, 0, 0)
    time.sleep(0.01)
    win32api.mouse_event(win32con.MOUSEEVENTF_LEFTDOWN, 0, 0)
    win32api.mouse_event(win32con.MOUSEEVENTF_LEFTUP, 0, 0)

def space_press():
    time.sleep(0.5)
    keyboard.press('space')
    time.sleep(0.5)
    keyboard.release('space')

def gamescript():
    cooldown_time = 0.2
    last_click_time = 0

    # YOU NEED TO CHANGE THIS PATH TO THE PATH OF THE IMAGE YOU WANT TO USE
    grayscale_pic_path = r'DESIERED PATH \ammo_grayscale.png'

    reference_pic = Image.open(grayscale_pic_path)

    confidence_threshold = 0.1
    try:
        while not keyboard.is_pressed('q'):
            current_time = time.time()
            if current_time - last_click_time < cooldown_time:
                continue
            pic = pyautogui.screenshot(region=(340, 330, 600, 500))
            width, height = pic.size

            for x in range(0, width, 5):
                for y in range(0, height, 5):
                    r, g, b = pic.getpixel((x, y))
                    if b == 0:
                        double_click(x + 340, y + 330)
                        last_click_time = current_time
                        time.sleep(0.01)
                        break

            ammo_pic = pyautogui.screenshot(region=(550, 230, 38, 30)).convert('L')
            diff = ImageChops.difference(reference_pic, ammo_pic)
            stat = ImageStat.Stat(diff)
            diff_ratio = sum(stat.mean) / 255
            if diff_ratio < (1 - confidence_threshold):
                space_press()
            else:
                print("Images do not match")
            time.sleep(0.1)
    except Exception as e:
        print(f"Ane error occurred: {e}")
    finally:
        print("Script ended")



if __name__ == '__main__':
    gamescript()
