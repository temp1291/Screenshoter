from pynput import keyboard
from screenshoter import Screenshoter


class HotkeyListener:
    def run(self, image_format:str, jpeg_quality:int, save_path:str, hotkey:str):
        self.image_format = image_format
        self.jpeg_quality = jpeg_quality
        self.save_path = save_path
        self.screenshoter = Screenshoter()

        if hotkey in keyboard.Key.__dict__.keys():
            self.hotkey = getattr(keyboard.Key, hotkey)
        else:
            self.hotkey = keyboard.KeyCode(char=hotkey)

        with keyboard.Listener(on_press=self.on_press) as self.listener:
            self.listener.join()


    def on_press(self, key):
        if key == self.hotkey:
            self.screenshoter.take_screenshot(self.image_format, self.jpeg_quality, self.save_path)


    def quit(self):
        self.listener.stop()


    def capture_hotkey_input(self):
        with keyboard.Listener(on_press=self.handle_hotkey_change) as self.hotkey_change_listener:
            self.hotkey_change_listener.join()


    def handle_hotkey_change(self, key):
        self.hotkey_change_listener.stop()
        hotkey = str(key)
        hotkey_parts = hotkey.split('.')
        hotkey_parts_length = len(hotkey_parts)

        if hotkey_parts_length == 1:
            self.hotkey = hotkey[1]
        elif hotkey_parts_length == 2:
            self.hotkey = hotkey_parts[1]


    def get_hotkey(self) -> str:
        return self.hotkey