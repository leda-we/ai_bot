import os
import io
import time
from PIL import Image
import pyautogui
from google import genai
from google.genai import types

def take_screenshot() -> str:
    print("\n[Скриншот экрана...]")
    screenshot = pyautogui.screenshot()

    scale_factor = 0.7
    new_width = int(screenshot.width * scale_factor)
    new_height = int(screenshot.height * scale_factor)
    screenshot = screenshot.resize((new_width, new_height), Image.Resampling.LANCZOS)

    temp_path = "temp_celestia_vision.jpg"
    screenshot.save(temp_path, format="JPEG", quality=80)
    return temp_path
