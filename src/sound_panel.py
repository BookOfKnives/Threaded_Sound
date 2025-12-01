from pathlib import Path
import tkinter as tk
from tkinter import ttk

import sound_player

class Sound_panel(ttk.Frame):
    def __init__(self, parent, filepaths : list[str]= []):
        super().__init__(parent, relief="groove")

        self.player = sound_player.sound_player(filepaths)
        
        self.grid()

        #setup name frame
        self.name_frame = ttk.Frame(self, relief="raised")
        self.name_frame.grid(column=0, row=0, columnspan=5, sticky="ew")

        self.name = ttk.Label(self.name_frame, text=Path(filepaths[0]).name if filepaths else "Sound Panel")
        self.name.grid(column=0, row=0, sticky="w", padx=5)

        self.editNameButton = ttk.Button(self.name_frame, text="✏", command=self.edit_name, width=3)
        self.editNameButton.grid(column=1, row=0, sticky="w", padx=0)

        self.settingsButton = ttk.Button(self.name_frame, text="⚙", command=self.open_settings, width=3)
        self.settingsButton.grid(column=2, row=0, sticky="w", padx=0)

        self.closeButton = ttk.Button(self.name_frame, text="X", command=self.close, width=3)
        self.closeButton.grid(column=3, row=0, sticky="e", padx=0)
    
        self.name_frame.columnconfigure(0, weight=1)


        # Setup control buttons and sliders
        self.startButton = ttk.Button(self, text="Play", command=self.player.play_sound_once, width=6)
        self.startButton.grid(column=0, row=1)

        self.stopButton = ttk.Button(self, text="Stop", command=self.player.stop_repeat_sound, width=6)
        self.stopButton.grid(column=1, row=1)

        self.repeatButton = ttk.Button(self, text="Repeat", command=self.player.play_sound_repeat, width=6)
        self.repeatButton.grid(column=2, row=1)

        # self.shuffleButton = ttk.Checkbutton(self, text="Shuffle")
        # self.shuffleButton.grid(column=3, row=1)
        # self.shuffleButton.config(command=self.toggle_shuffle)

        self.volume_label = ttk.Label(self, text="VOL")
        self.volume_label.grid(column=3, row=1)

        self.volumeSlider = ttk.Scale(self, orient="horizontal", command=lambda value: self.player.set_volume(value))
        self.volumeSlider.set(0.5)
        self.volumeSlider.grid(column=4, row=1, sticky="ew")
        self.volumeSlider.bind('<MouseWheel>', self.mouse_wheel_adjust_volume)
        
        # Make the slider column expand
        self.columnconfigure(4, weight=1)

        # self.interval_label = ttk.Label(self, text="Interval")
        # self.interval_label.grid(column=2, row=2)

        # self.interval_slider = ttk.Scale(self, from_=0, to=50, orient="horizontal", command=self.setInterval)
        # self.interval_slider.grid(column=3, row=2)
    
    def mouse_wheel_adjust_volume(self, event):
        adjustment_step = 0.025
        if event.delta > 0:
            self.player.set_volume(self.player.get_volume() + adjustment_step)
            self.volumeSlider.set(self.player.get_volume() + adjustment_step)
        else:
            self.player.set_volume(self.player.get_volume() - adjustment_step)
            self.volumeSlider.set(self.player.get_volume() - adjustment_step)

    def close(self):
        """Clean up resources before destroying the panel"""
        self.player.destroy()
        self.destroy()

    def toggle_shuffle(self):
        self.player.shuffle = not self.player.shuffle

    def setInterval(self, value):
        fvalue = round(float(value), 3)
        self.player.set_interval(fvalue)
    
    def edit_name(self):
        """Switch to edit mode for the name"""
        current_name = self.name.cget("text")
        self.name.grid_forget()
        
        # Create entry widget in place of label
        self.name_entry = ttk.Entry(self.name_frame)
        self.name_entry.insert(0, current_name)
        self.name_entry.grid(column=0, row=0, sticky="ew", padx=5)
        self.name_entry.focus()
        self.name_entry.select_range(0, tk.END)
        
        # Bind Enter and focus out to finish editing
        self.name_entry.bind("<Return>", lambda e: self.finish_edit_name())
        self.name_entry.bind("<FocusOut>", lambda e: self.finish_edit_name())
    
    def finish_edit_name(self):
        """Finish editing and restore the label"""
        if hasattr(self, 'name_entry'):
            new_name = self.name_entry.get()
            self.name_entry.destroy()
            if new_name:
                self.name.config(text=new_name)
            self.name.grid(column=0, row=0, sticky="w", padx=5)
    
    def open_settings(self):
        """Open settings panel or dialog"""
        # Placeholder for settings functionality
        print("Settings button clicked")


