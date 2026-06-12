import os
import io
import time
from PIL import Image
import pyautogui
from google import genai
from google.genai import types
from dotenv import load_dotenv
load_dotenv()

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
class CelestiaAssistant:
    def __init__(self):
        self.client = genai.Client()
        self.model_name = "gemini-2.5-flash"
        self.system_instruction = ("PROMPT_AI_BOT")
        self.chat = self.client.chats.create(
            model=self.model_name,
            config=types.GenerateContentConfig(
                system_instruction=self.system_instruction,
                tools=[take_screenshot],
                temperature=0.7
            )
        )
    def ask(self, user_text: str):
        print(f"\nВы: {user_text}")

        response = self.chat.send_message(user_text)
        if response.function_calls:
            for call in response.function_calls:
                if call.name == "take_screenshot":
                    img_path = take_screenshot()
                    print("[Отправка изображения...]")
                    image_part = self.client.files.upload(file=img_path)
                    follow_up_response = self.chat.send_message(
                        message=[
                            image_part,
                            "Я сделал скриншот. Посмотри на него внимательно и ответь на мой предыдущий вопрос."
                        ]
                    )

                    if os.path.exists(ing_path):
                        os.remove(img_path)

                    return follow_up_response.text
        return response.text