from pynput import keyboard
from screenshoter import Screenshoter


class HotkeyListener:
    def __init__(self, image_format:str, jpeg_quality:int, save_path:str):
        self.image_format = image_format
        self.jpeg_quality = jpeg_quality
        self.save_path = save_path
        self.screenshoter = Screenshoter()
        self.hotkey = keyboard.Key.print_screen


    def run(self):
        with keyboard.Listener(on_press=self.on_press) as self.listener:
            self.listener.join()


    def on_press(self, key):
        if key == self.hotkey:
            self.screenshoter.take_screenshot(self.image_format, self.jpeg_quality, self.save_path)


    def quit(self):
        self.listener.stop()