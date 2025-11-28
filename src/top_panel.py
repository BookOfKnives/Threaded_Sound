import tkinter as tk
from tkinter import ttk

import sound_player

class top_panel(ttk.Frame):
    def __init__(self, parent, app):
        super().__init__(parent, relief="raised", padding="3 3 12 12")
        self.app = app
        
        self.stop_all_button = ttk.Button(self, text="Stop All", command=self.stop_all_sounds)
        self.stop_all_button.grid(column=0, row=0, padx=5, pady=5)

    def stop_all_sounds(self):
        """Stops all sounds playing in all sound_player instances."""
        for panel in self.app.sound_panels:
            panel.player.stop_repeat_sound()