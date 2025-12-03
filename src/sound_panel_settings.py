from pathlib import Path
import tkinter as tk
from tkinter import ttk

from pygame import mixer

import sound_player

class sound_panel_settings(tk.Toplevel):
    def __init__(self, parent, player : sound_player.sound_player, panel_name: str = "Sound Panel", keybind_manager=None):
        super().__init__(parent)
        self.player = player
        self.keybind_manager = keybind_manager
        self.old_keybind = player.get_keybind()
        
        # Configure the popup window
        self.title(f"Settings - {panel_name}")
        self.resizable(True, True)
        
        # Configure window grid to expand
        self.columnconfigure(0, weight=1)
        self.rowconfigure(0, weight=1)
        
        # Create main frame with padding
        main_frame = ttk.Frame(self, padding="10 10 10 10")
        main_frame.grid(column=0, row=0, sticky="nsew")
        
        # Global settings frame at the top
        global_frame = ttk.Frame(main_frame)
        global_frame.grid(column=0, row=0, columnspan=2, sticky="ew", padx=5, pady=5)
        
        # Keybind entry
        ttk.Label(global_frame, text="Keybind:").grid(column=0, row=0, sticky="w", padx=(0, 5))
        self.keybind_var = tk.StringVar(value=self.player.get_keybind())
        self.keybind_entry = ttk.Entry(global_frame, textvariable=self.keybind_var, width=15)
        self.keybind_entry.grid(column=1, row=0, sticky="w", padx=5)
        self.keybind_entry.bind("<KeyRelease>", self.update_keybind)
        
        # Shuffle checkbox
        self.shuffle_var = tk.BooleanVar(value=self.player.get_shuffle())
        self.shuffle_check = ttk.Checkbutton(global_frame, text="Shuffle", variable=self.shuffle_var, command=self.update_shuffle)
        self.shuffle_check.grid(column=2, row=0, sticky="w", padx=15)
        
        # Create scrollable frame for sound settings if there are many sounds
        canvas = tk.Canvas(main_frame)
        scrollbar = ttk.Scrollbar(main_frame, orient="vertical", command=canvas.yview)
        scrollable_frame = ttk.Frame(canvas)
        
        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )
        
        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)
        
        # Create _sound_setting for each sound
        self.sound_settings = []
        for i, (sound, filepath) in enumerate(zip(self.player.sounds, self.player.get_filepaths())):
            filename = Path(filepath).name
            sound_setting = _sound_setting(scrollable_frame, sound, filename)
            sound_setting.grid(column=0, row=i, sticky="ew", padx=5, pady=2)
            self.sound_settings.append(sound_setting)
        
        canvas.grid(column=0, row=1, sticky="nsew", padx=5, pady=5)
        scrollbar.grid(column=1, row=1, sticky="ns", pady=5)
        
        # Add close button
        close_button = ttk.Button(main_frame, text="Close", command=self.destroy)
        close_button.grid(column=0, row=2, sticky="e", padx=5, pady=10)
        
        # Configure grid weights
        main_frame.columnconfigure(0, weight=1)
        main_frame.rowconfigure(1, weight=1)
        
        # Position window near parent but not centered (to allow multiple windows)
        self.update_idletasks()
        x = parent.winfo_rootx() + 50
        y = parent.winfo_rooty() + 50
        self.geometry(f"+{x}+{y}")
    
    def update_shuffle(self):
        """Update shuffle setting in real-time"""
        self.player.set_shuffle(self.shuffle_var.get())
    
    def update_keybind(self, event=None):
        """Update keybind setting in real-time"""
        new_keybind = self.keybind_var.get()
        if self.keybind_manager:
            self.keybind_manager.update(self.player.play_sound_once, self.old_keybind, new_keybind)
            self.old_keybind = new_keybind
        self.player.set_keybind(new_keybind)

class _sound_setting(ttk.Frame):
    def __init__(self, parent, sound: mixer.Sound, filepath: str):
        super().__init__(parent)
        
        self.label = ttk.Label(self, text=filepath)
        self.label.grid(column=0, row=0, padx=5, pady=5, sticky="w")
        
        self.volume = ttk.Label(self, text="Vol")
        self.volume.grid(column=1, row=0, padx=5, pady=5)
        
        self.vscale = ttk.Scale(self, orient="horizontal")
        self.vscale.grid(column=2, row=0, padx=5, pady=5, sticky="ew")
        
        self.interval = ttk.Label(self, text="Interval")
        self.interval.grid(column=3, row=0, padx=5, pady=5)
        
        self.iscale = ttk.Scale(self, orient="horizontal")
        self.iscale.grid(column=4, row=0, padx=5, pady=5, sticky="ew")