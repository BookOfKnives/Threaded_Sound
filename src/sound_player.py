from pygame import mixer
import pygame
import random
import threading
import json_saver

"""0112 2025
10:57
contains all sound-playing logic, volume, repeat, intervals, etc.
"""

class sound_player:
    _used_channels = set()  # Class variable to track which channels are in use
    
    def __init__(self, filepaths : list[str]):
        if mixer.get_init() is None:
            raise Exception("Pygame mixer not initialized.")
        if not filepaths:
            raise ValueError("No filepaths provided to sound_player.")

        # Initialize sound settings
        self._settings = _sound_settings()
        self._settings.files = [_sound_file_setting(file) for file in filepaths]
        self._settings.repeat = False
        self._settings.shuffle = False
        self._settings.keybind = ""  # Global keybind for this sound player
        self._settings.interval = 0.05  # default interval between repeats in seconds
        self._settings.channel_volume = 0.5
        
        # Make set: _sound_file_setting -> mixer.Sound
        self.sounds = {file_setting: mixer.Sound(file_setting.filepath) for file_setting in self._settings.files}
        
        # Setup variables for playback control
        self.repeat_thread = None
        self._current_sound_index = 0
        
        # Allocate a unique channel for this sound_player
        self.channel_id = self._find_free_channelID()
        self.channel = mixer.Channel(self.channel_id)
        sound_player._used_channels.add(self.channel_id)
        self.channel.set_volume(float(self._settings.channel_volume))

    def play(self):
        if self._settings.repeat:
            self.play_sound_repeat()
        else:
            self.play_sound_once()

    def play_sound_once(self):
        if self._settings.shuffle:
            sound = random.choice(list(self.sounds.values()))
        else:
            sound = self.sounds[self._settings.files[self._current_sound_index]]
            self._current_sound_index = (self._current_sound_index + 1) % len(self._settings.files)
        self.channel.play(sound)

    def play_sound_repeat(self):
        self._settings.repeat = True
        if self.repeat_thread is None or not self.repeat_thread.is_alive():
            self.repeat_thread = threading.Thread(target=self._repeat_loop, daemon=True)
            self.repeat_thread.start()

    def _repeat_loop(self):
        while self._settings.repeat:
            if self._settings.shuffle:
                sound = random.choice(list(self.sounds.values()))
            else:
                sound = self.sounds[self._settings.files[self._current_sound_index]]
                self._current_sound_index = (self._current_sound_index + 1) % len(self._settings.files)
            self.channel.play(sound)
            while self.channel.get_busy() and self._settings.repeat:  # Wait until the sound has finished playing
                pygame.time.delay(10)  # Small delay to avoid busy-waiting
            
            variation = random.uniform(0.9, 1.1) # Add random +-10% variation to the interval
            pygame.time.delay(int(self._settings.interval * 1000 * variation))  # delay expects milliseconds

    def stop_repeat_sound(self):
        self._settings.repeat = False
        self.channel.fadeout(1000)
    
    def set_volume(self, value):
        self._settings.channel_volume = float(value)
        self.channel.set_volume(self._settings.channel_volume)
    
    def set_interval(self, value):
        self.interval = float(value)

    def set_keybind(self, keybind: str):
        self._settings.keybind = keybind

    def set_shuffle(self, shuffle: bool):
        self._settings.shuffle = shuffle
    
    def set_repeat(self, repeat: bool):
        self._settings.repeat = repeat
    
    def get_repeat(self):
        return self._settings.repeat

    def destroy(self):
        """Stop playback and release the channel"""
        self.stop_repeat_sound()
        sound_player._used_channels.discard(self.channel_id)
    
    def __del__(self):
        """Release the channel when this sound_player is destroyed"""
        self.destroy()

    def _find_free_channelID(self):
        """Find and return a free channel ID, expanding channels if necessary."""
        num_channels = mixer.get_num_channels()
        channel_id = 0
        while channel_id in sound_player._used_channels:
            channel_id += 1
        
        # Expand channels if needed
        if channel_id >= num_channels:
            mixer.set_num_channels(channel_id + 1)
        
        return channel_id
    
    def get_settings(self): 
        """Exposes private sound settings for saving func."""
        print("hitting get_settings")
        print(self._settings)

    def get_volume(self):
        return self._settings.channel_volume
    
    def get_keybind(self):
        return self._settings.keybind
    
    def get_shuffle(self):
        return self._settings.shuffle
    
    def get_filepaths(self):
        return [file.filepath for file in self._settings.files]

    def save_settings(self):
        json_saver.save_settings(self)


class _sound_settings:
    """0112 2025
    11:00
    contains all info necessary to create sound_panel from a saved state."""
    def __init__(self):
        self.repeat = False
        self.shuffle = False
        self.interval = 0.05
        self.files = []
        self.channel_volume : float = 0.5  
        self.keybind = ""
        
    def __str__(self):
        return "str of _sound_settings: \n" + "Repeats: " + str(self.repeat) + ", Shuffle: " +  str(self.shuffle)
   
class _sound_file_setting:
    def __init__(self, filepath: str, volume: float = 0.5, interval: float = 0.05):
        self.name = filepath.split("/")[-1]  # Extract the file name from the path
        self.filepath = filepath
        self.volume = volume
        self.interval = interval
