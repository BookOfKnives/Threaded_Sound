import tkinter as tk
from tkinter import ttk

import sound_player

class Sound_panel(ttk.Frame):
    def __init__(self, parent, filepaths : list[str] = []):
        super().__init__(parent, relief="groove")

        self.player = sound_player.sound_player(filepaths)
        
        self.grid()

        self.startButton = ttk.Button(self, text="Play", command=self.player.play_sound_once)
        self.startButton.grid(column=0, row=0)

        self.stopButton = ttk.Button(self, text="Stop", command=self.player.stop_repeat_sound)
        self.stopButton.grid(column=1, row=0)

        self.repeatButton = ttk.Button(self, text="repeat", command=self.player.play_sound_repeat)
        self.repeatButton.grid(column=2, row=0)

        self.shuffleButton = ttk.Checkbutton(self, text="Shuffle")
        self.shuffleButton.grid(column=3, row=0)
        self.shuffleButton.config(command=self.toggle_shuffle)

        self.closeButton = ttk.Button(self, text="X", command=self.destroy)
        self.closeButton.grid(column=4, row=0)

        self.volume_label = ttk.Label(self, text="VOL")
        self.volume_label.grid(column=0, row=1)

        self.volumeSlider = ttk.Scale(self, orient="horizontal", command=lambda value: self.player.set_volume(value))
        # self.volumeSlider
        self.volumeSlider.grid(column=1, row=1)

        self.interval_label = ttk.Label(self, text="Interval")
        self.interval_label.grid(column=2, row=1)

        self.interval_slider = ttk.Scale(self, from_=0, to=50, orient="horizontal", command=lambda value: self.player.set_interval(value))
        self.interval_slider.grid(column=3, row=1)

    def toggle_shuffle(self):
        self.player.shuffle = not self.player.shuffle


