from pathlib import Path
import tkinter as tk
from tkinter import ttk

from pygame import mixer

import keybind_manager
import sound_player

class sound_panel_settings(tk.Toplevel):
    def __init__(self, parent, player : sound_player.sound_player, panel_name: str = "Sound Panel", keybind_manager : keybind_manager =None):
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
        for row, index in enumerate(self.player.get_sound_indexes()):
            sound_setting = _sound_setting(scrollable_frame, self.player, index)
            sound_setting.grid(column=0, row=row, sticky="ew", padx=5, pady=2)
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
    def __init__(self, parent, player: sound_player.sound_player, index: int):
        super().__init__(parent)
        self.player = player
        self.index = index
        
        # Get initial values from player
        name = self.player.get_name_per_id(index)
        volume = self.player.get_volume_per_id(index)
        interval = self.player.get_interval_per_id(index)
        
        self.label = ttk.Label(self, text=name)
        self.label.grid(column=0, row=0, padx=5, pady=5, sticky="w")
        
        self.volume_label = ttk.Label(self, text="🔊")
        self.volume_label.grid(column=1, row=0, padx=5, pady=5)
        
        self.vscale = ttk.Scale(self, orient="horizontal", from_=0.0, to=1.0, command=self._on_volume_change)
        self.vscale.set(volume)
        self.vscale.grid(column=2, row=0, padx=5, pady=5, sticky="ew")
        
        self.interval_label = ttk.Label(self, text="⏳")
        self.interval_label.grid(column=3, row=0, padx=5, pady=5)
        
        # Add editable entry for interval value
        self.interval_var = tk.StringVar(value=f"{interval:.2f}")
        self.interval_entry = ttk.Entry(self, textvariable=self.interval_var, width=8)
        self.interval_entry.grid(column=4, row=0, padx=5, pady=5)
        self.interval_entry.bind("<Return>", self._on_interval_entry_change)
        self.interval_entry.bind("<FocusOut>", self._on_interval_entry_change)
        
        self.iscale = ttk.Scale(self, orient="horizontal", from_=0.01, to=5.0, command=self._on_interval_change)
        self.iscale.set(interval)
        self.iscale.grid(column=5, row=0, padx=5, pady=5, sticky="ew")
        
        # Make scales expand
        self.columnconfigure(2, weight=1)
        self.columnconfigure(4, weight=1)
    
    def _on_volume_change(self, value):
        """Update volume through player"""
        self.player.set_volume_per_id(self.index, float(value))
    
    def _on_interval_change(self, value):
        """Update interval through player and entry box"""
        interval = float(value)
        self.player.set_interval_per_id(self.index, interval)
        self.interval_var.set(f"{interval:.2f}")
    
    def _on_interval_entry_change(self, event=None):
        """Update interval from entry box"""
        try:
            interval = float(self.interval_var.get())
            # Clamp to valid range
            interval = max(0.01, min(5.0, interval))
            self.player.set_interval_per_id(self.index, interval)
            self.iscale.set(interval)
            self.interval_var.set(f"{interval:.2f}")
        except ValueError:
            # Reset to current value if invalid input
            current = self.player.get_interval_per_id(self.index)
            self.interval_var.set(f"{current:.2f}")