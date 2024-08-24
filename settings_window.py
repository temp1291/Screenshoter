from tkinter import *
from tkinter import ttk
from tkinter.messagebox import askquestion, showwarning
from tkinter.filedialog import askdirectory
import json
from hotkey_listener import HotkeyListener


class SettingsWindow(Tk):
    def __init__(self):
        super().__init__()
        self.title('Options')
        self.geometry('320x180')
        self.resizable(False, False)
        self.protocol('WM_DELETE_WINDOW', self.on_close)

        for c in range(14): self.columnconfigure(index=c, weight=1)
        for r in range(7): self.rowconfigure(index=r, weight=1)

        self.hotkey_listener = HotkeyListener()
        self.image_formats = ('PNG', 'JPEG', 'BMP', 'GIF', 'TIFF', 'WEBP')
        
        self.load_data_from_json()
        self.put_widgets()


    def put_widgets(self):
        label_format = ttk.Label(self, text='Format')
        label_format.grid(column=0, row=0, columnspan=7, sticky=W)

        combobox_format = ttk.Combobox(self, values=self.image_formats, textvariable=self.image_format, state='readonly')
        combobox_format.grid(column=8, row=0, columnspan=7)

        label_jpeg_quality = ttk.Label(self, text='JPEG quality')
        label_jpeg_quality.grid(column=0, row=1, columnspan=7, sticky=W)

        scale_jpeg_quality = ttk.Scale(self, from_=1.0, to=95.0, orient=HORIZONTAL, variable=self.jpeg_quality, command=self.update_label_value)
        scale_jpeg_quality.grid(column=8, row=1, columnspan=6)

        self.label_jpeg_quality_value = ttk.Label(self, text=int(self.jpeg_quality.get()), width=2)
        self.label_jpeg_quality_value.grid(column=13, row=1)

        label_save_path = ttk.Label(text='Save path for screenshots')
        label_save_path.grid(column=0, row=2, columnspan=7, sticky=W)

        path_validate_command = (self.register(self.is_valid_path), '%P')
        self.entry_save_path = ttk.Entry(textvariable=self.save_path, validate='focusout', validatecommand=path_validate_command)
        self.entry_save_path.grid(column=8, row=2, columnspan=5)

        button_choose_save_path = ttk.Button(text='...', width=2, command=self.choose_save_path)
        button_choose_save_path.grid(column=13, row=2, padx=5)

        label_hotkey = ttk.Label(text='Hotkey')
        label_hotkey.grid(column=0, row=3)

        self.button_choose_hotkey = ttk.Button(text=self.hotkey, command=self.change_hotkey)
        self.button_choose_hotkey.grid(column=8, row=3, columnspan=6)


        self.button_ok = ttk.Button(self, text='Ok', command=self.close_with_save)
        self.button_ok.grid(column=7, row=6, columnspan=3)

        self.button_cancel = ttk.Button(self, text='Cancel', command=self.on_close)
        self.button_cancel.grid(column=10, row=6, columnspan=3)


    def update_label_value(self, value:str):
        self.label_jpeg_quality_value.config(text=int(self.jpeg_quality.get()))


    def load_data_from_json(self):
        with open('config.json', 'r') as file:
            data = json.load(file)

        self.image_format = StringVar(value=data['image_format'])
        self.jpeg_quality = IntVar(value=data['jpeg_quality'])
        self.save_path = StringVar(value=data['save_path'])
        self.hotkey = data['hotkey']
        

    def close_with_save(self):
        data = {
            'image_format': self.image_format.get(),
            'jpeg_quality': int(self.jpeg_quality.get()),
            'save_path': self.save_path.get(),
            'hotkey': self.hotkey
        }
        with open('config.json', 'w') as file:
            json.dump(data, file, indent=4)

        self.destroy()


    def on_close(self):
        answer = askquestion("Unsaved Changes", "Are you sure you want to exit without saving your changes?")

        if answer == "yes":
            self.destroy()
        else:
            pass


    def is_valid_path(self, path):
        from pathlib import Path
        if Path(path).is_dir():
            return True
        else:
            self.save_path.set(value='Screenshots')
            showwarning(message='Invalid path')
            return False
    

    def choose_save_path(self):
        path = askdirectory(title='Choose Save Path')
        if path:
            self.save_path.set(value=path)


    def change_hotkey(self):
        self.button_choose_hotkey.config(text='Press any key...')
        self.hotkey_listener.capture_hotkey_input()
        self.hotkey = self.hotkey_listener.get_hotkey()
        self.button_choose_hotkey.config(text=self.hotkey)


if __name__ == '__main__':
    window = SettingsWindow()
    window.mainloop()

