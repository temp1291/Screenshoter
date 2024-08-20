import json
import threading
from tray import Tray
from hotkey_listener import HotkeyListener


class App:
    def __init__(self):
        self.load_data_from_json()

        self.tray = Tray(self)
        self.hotkey_listener = HotkeyListener(self.image_format, self.jpeg_quality, self.save_path)

        tray_thread = threading.Thread(target=self.tray.run)
        hotkey_listener_thread = threading.Thread(target=self.hotkey_listener.run)

        tray_thread.start()
        hotkey_listener_thread.start()

        tray_thread.join()
        hotkey_listener_thread.join()


    def load_data_from_json(self):
        with open('config.json', 'r') as file:
            data = json.load(file)

        self.image_format = data['image_format']
        self.jpeg_quality = data['jpeg_quality']
        self.save_path = data['save_path']


    def quit(self):
        self.tray.quit()
        self.hotkey_listener.quit()


if __name__ == '__main__':
    App()