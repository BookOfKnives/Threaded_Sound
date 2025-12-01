import pathlib
import tkinter as tk
from tkinter import ttk
from tkinterdnd2 import Tk as TkinterDnDTk, DND_FILES

from pygame import mixer

import sound_panel
import top_panel


class App:
    def __init__(self):
        self.main_frame = TkinterDnDTk()
        self.main_frame.title("Sound Player")
        self.main_frame.geometry("400x300")
        self.main_frame.drop_target_register(DND_FILES)
        self.main_frame.dnd_bind('<<Drop>>', self.on_drop) 
        self.sound_panels = []
        
        # Make the column expand to fill the window
        self.main_frame.columnconfigure(0, weight=1)

        # Top frame for controls
        self.top_frame = self.create_top_frame(self.main_frame)

        # Sound panel frames
        mixer.init()
        self.create_sound_panel([pathlib.Path("test_soundfile/explosions/explode2.wav").absolute().as_posix()])

        self.main_frame.mainloop()

    def on_drop(self, event):
        """This is the function that handles the drag-dropped file."""
        print("File dropped:", event.data)
        files = list(self.main_frame.tk.splitlist(event.data))
        print("Files list:", files)
        self.create_sound_panel(files)

    def create_sound_panel(self, filepaths):
        sound_panel_frame = sound_panel.Sound_panel(self.main_frame, filepaths)
        row_position = len(self.sound_panels) + 1 
        sound_panel_frame.grid(column=0, row=row_position, sticky="ew", padx=5, pady=5)
        
        # Create a unique style for this panel
        style_name = f"Panel{row_position}.TFrame"
        style = ttk.Style()
        bg_color = "#f0f0f0" if row_position % 2 == 0 else "#ffffff"
        style.configure(style_name, background=bg_color)
        sound_panel_frame.configure(style=style_name)
        
        self.sound_panels.append(sound_panel_frame)
        
    def create_top_frame(self, main_frame):
        frame = top_panel.top_panel(main_frame, self)
        frame.grid(column=0, row=0, sticky="ew", padx=5, pady=5)
        return frame





if __name__ == "__main__":
    app = App()