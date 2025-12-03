from pathlib import Path
import tkinter as tk
from tkinter import ttk

import sound_player
import sound_panel_settings

class Sound_panel(ttk.Frame):
    _instance_counter = 0  # Class variable to track instances
    
    def __init__(self, parent, filepaths : list[str]= [], bg_color=None, keybind_manager=None, on_close_callback=None):
        # Create background frame first
        self.bg_frame = tk.Frame(parent)
        
        # Create unique style for this instance
        Sound_panel._instance_counter += 1
        self._keybind_manager = keybind_manager  # Store keybind manager reference for settings
        self._on_close_callback = on_close_callback  # Callback to notify when panel is closed
        self.style_name = f"SoundPanel{Sound_panel._instance_counter}.TFrame"
        self.label_style_name = f"SoundPanel{Sound_panel._instance_counter}.TLabel"
        self.button_style_name = f"SoundPanel{Sound_panel._instance_counter}.TButton"
        self.scale_style_name = f"SoundPanel{Sound_panel._instance_counter}.Horizontal.TScale"
        
        # Initialize as child of bg_frame
        super().__init__(self.bg_frame, relief="groove", style=self.style_name)

        self.player = sound_player.sound_player(filepaths)
        self.settings_window = None  # Track the settings window
        
        # Pack self into bg_frame
        self.pack(fill="both", expand=True, padx=5, pady=5)
        
        # Apply background color using update_bg_color method
        if bg_color:
            self.update_bg_color(bg_color)

        #setup name frame
        self.name_frame = ttk.Frame(self, relief="raised", style=self.style_name)
        self.name_frame.grid(column=0, row=0, columnspan=5, sticky="ew")

        self.name = ttk.Label(self.name_frame, text=Path(filepaths[0]).name if filepaths else "Sound Panel", style=self.label_style_name)
        self.name.grid(column=0, row=0, sticky="w", padx=5)

        self.editNameButton = ttk.Button(self.name_frame, text="✏", command=self.edit_name, width=3, style=self.button_style_name)
        self.editNameButton.grid(column=1, row=0, sticky="w", padx=0)

        self.settingsButton = ttk.Button(self.name_frame, text="⚙", command=self.open_settings, width=3, style=self.button_style_name)
        self.settingsButton.grid(column=2, row=0, sticky="w", padx=0)

        self.closeButton = ttk.Button(self.name_frame, text="X", command=self.close, width=3, style=self.button_style_name)
        self.closeButton.grid(column=3, row=0, sticky="e", padx=0)
    
        self.name_frame.columnconfigure(0, weight=1)


        # Setup control buttons and sliders
        self.startButton = ttk.Button(self, text="▶", command=self.player.play, width=3, style=self.button_style_name)
        self.startButton.grid(column=0, row=1)

        self.stopButton = ttk.Button(self, text="⏹", command=self.player.stop_repeat_sound, width=3, style=self.button_style_name)
        self.stopButton.grid(column=1, row=1)

        self.repeatButton = ttk.Button(self, text="🔁", command=self.toggle_repeat, width=3, style=self.button_style_name)
        self.repeatButton.grid(column=2, row=1)
        self.update_repeat_button()

        self.volume_label = ttk.Label(self, text="🔊", style=self.label_style_name)
        self.volume_label.grid(column=3, row=1)

        self.volumeSlider = ttk.Scale(self, orient="horizontal", command=lambda value: self.player.set_volume(value), style=self.scale_style_name)
        self.volumeSlider.set(0.5)
        self.volumeSlider.grid(column=4, row=1, sticky="ew")
        self.volumeSlider.bind('<MouseWheel>', self.mouse_wheel_adjust_volume)
        
        # Make the slider column expand
        self.columnconfigure(4, weight=1)
    
    def update_bg_color(self, new_bg_color):
        """Update the background color of the panel and all its widgets"""
        # Update bg_frame
        self.bg_frame.config(bg=new_bg_color)
        
        # Update ttk styles
        style = ttk.Style()
        style.configure(self.style_name, background=new_bg_color)
        style.configure(self.label_style_name, background=new_bg_color)
        style.configure(self.button_style_name, background=new_bg_color)
        style.map(self.button_style_name, background=[('active', new_bg_color), ('!active', new_bg_color)])
        style.configure(self.scale_style_name, background=new_bg_color, troughcolor=new_bg_color)
    
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
        # Unregister keybind if it exists
        if self._keybind_manager and self.player.get_keybind():
            self._keybind_manager.unregister(self.player.play_sound_once)
        
        # Notify parent via callback
        if self._on_close_callback:
            self._on_close_callback(self)
        
        # Destroy player
        self.player.destroy()
        
        # Destroy panel and bg_frame
        self.destroy()
        self.bg_frame.destroy()

    def toggle_shuffle(self):
        self.player.set_shuffle(not self.player.get_shuffle())
    
    def toggle_repeat(self):
        """Toggle repeat mode and update button appearance"""
        new_repeat = not self.player.get_repeat()
        self.player.set_repeat(new_repeat)
        self.update_repeat_button()
    
    def update_repeat_button(self):
        """Update repeat button style based on repeat state"""
        if self.player.get_repeat():
            # Create a pressed/active style for repeat button
            style = ttk.Style()
            style.map(self.button_style_name, 
                     relief=[('pressed', 'sunken'), ('!pressed', 'sunken')])
            self.repeatButton.state(['pressed'])
        else:
            self.repeatButton.state(['!pressed'])

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
        """Open settings popup dialog"""
        # If settings window already exists, bring it to front
        if self.settings_window and self.settings_window.winfo_exists():
            self.settings_window.deiconify()
            self.settings_window.lift()
            self.settings_window.focus()
            return
        
        # Create new settings window
        panel_name = self.name.cget("text")
        self.settings_window = sound_panel_settings.sound_panel_settings(self, self.player, panel_name, self._keybind_manager)


