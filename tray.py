from pystray import Icon, MenuItem, Menu
from PIL import Image


class Tray:
    def __init__(self, app):
        self.app = app


    def run(self):
        menu = Menu(
            MenuItem('Quit', self.app.quit)
        )
        self.icon = Icon('Screenshoter', self.create_image(), menu=menu)
        self.icon.run()


    def create_image(self):
        image = Image.new('RGB', (64, 64), color='green')
        return image


    def quit(self):
        self.icon.stop()
        


