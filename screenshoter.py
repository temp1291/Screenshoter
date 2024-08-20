import mss
from PIL import Image
from datetime import datetime


class Screenshoter:
    def __init__(self):
        ...


    def take_screenshot(self, format, quality, path):
        now = datetime.now()
        with mss.mss() as screenshot_tool:
            screenshot = screenshot_tool.grab(screenshot_tool.monitors[1])
            image = Image.frombytes('RGB', 
                                    (screenshot.width, screenshot.height),
                                    screenshot.rgb)
            
        name = f'{path}/Screenshot {now.hour:02}-{now.minute:02}-{now.second:02}-{now.microsecond:03d} {now.day:02}.{now.month:02}.{now.year}.{format.lower()}'
        image = image.convert('RGB')
        image.save(name, format, quality=quality)
