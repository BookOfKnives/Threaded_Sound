import pathlib
import tkinter as tk
from tkinter import ttk
from tkinterdnd2 import Tk as TkinterDnDTk, DND_FILES

from pygame import mixer

import sound_panel
import top_panel
from keybind_manager import KeybindManager


class App:
    def __init__(self):
        self.main_frame = TkinterDnDTk()
        self.main_frame.title("Sound Player")
        self.main_frame.geometry("400x300")
        self.main_frame.drop_target_register(DND_FILES)
        self.main_frame.dnd_bind('<<Drop>>', self.on_drop) 
        self.sound_panels = []
        self.keybind_manager = KeybindManager()
        
        # Make the column expand to fill the window
        self.main_frame.columnconfigure(0, weight=1)
        
        # Handle window close to cleanup keyboard hooks
        self.main_frame.protocol("WM_DELETE_WINDOW", self.on_closing)

        # Top frame for controls
        self.top_frame = self.create_top_frame(self.main_frame)

        # Sound panel frames
        mixer.init()
        self.create_sound_panel([pathlib.Path("test_soundfile/explosions/explode2.wav").absolute().as_posix()])

        self.hit_it_counter = 0
        self.main_frame.bind('a', self.hit_it)
        self.main_frame.bind('b', self.hit_display_settings)
        self.main_frame.bind('<Return>', self.quit_it)
        self.main_frame.bind('<Escape>', self.quit_it)

        self.main_frame.mainloop()
    
    def hit_it(self, event):
        self.hit_it_counter += 1
        print(f'Hitting it! {self.hit_it_counter}')

    def hit_display_settings(self, event):
        for panel in self.sound_panels:
            print(panel.player.get_settings())
        # print(self.sound_panels[0].player.get_settings())
        

    def quit_it(self, event):
        print("Quitting it.")
        self.main_frame.destroy()

    def on_drop(self, event):
        """This is the function that handles the drag-dropped file."""
        files = list(self.main_frame.tk.splitlist(event.data))
        self.create_sound_panel(files)

    def create_sound_panel(self, filepaths):
        row_position = len(self.sound_panels) + 1
        
        # Create a colored background frame with alternating colors
        bg_color = "#d4e6f1" if row_position % 2 == 0 else "#f8f9f9"
        
        # Create the sound panel (which includes its own bg_frame)
        sound_panel_frame = sound_panel.Sound_panel(
            self.main_frame, 
            filepaths, 
            bg_color=bg_color, 
            keybind_manager=self.keybind_manager,
            on_close_callback=self.on_panel_closed
        )
        
        # Grid the bg_frame
        sound_panel_frame.bg_frame.grid(column=0, row=row_position, sticky="ew", padx=0, pady=0)
        
        self.sound_panels.append(sound_panel_frame)
        
        # Register global hotkey if keybind is set
        if sound_panel_frame.player.get_keybind():
            self.keybind_manager.register(sound_panel_frame.player.get_keybind(), sound_panel_frame.player.play_sound_once)
        
    def create_top_frame(self, main_frame):
        frame = top_panel.top_panel(main_frame, self)
        frame.grid(column=0, row=0, sticky="ew", padx=5, pady=5)
        return frame
    
    def on_panel_closed(self, panel):
        """Callback when a sound panel is closed"""
        if panel in self.sound_panels:
            self.sound_panels.remove(panel)
            # Reorganize remaining panels
            self.reorganize_panels()
    
    def reorganize_panels(self):
        """Update positions and colors of all panels after one is removed"""
        for index, panel in enumerate(self.sound_panels):
            row_position = index + 1
            
            # Update background color based on new position
            new_bg_color = "#d4e6f1" if row_position % 2 == 0 else "#f8f9f9"
            panel.update_bg_color(new_bg_color)
            
            # Update grid position
            panel.bg_frame.grid(column=0, row=row_position, sticky="ew", padx=0, pady=0)
    
    def on_closing(self):
        """Cleanup when closing the application"""
        self.keybind_manager.cleanup()
        self.main_frame.destroy()





if __name__ == "__main__":
    app = App()