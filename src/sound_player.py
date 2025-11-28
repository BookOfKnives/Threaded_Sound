from pygame import mixer
import pygame
import random
import threading

class sound_player:
    def __init__(self, filepaths : list[str]):
        if mixer.get_init() is None:
            raise Exception("Pygame mixer not initialized.")
        if not filepaths:
            raise ValueError("No filepaths provided to sound_player.")
        self.sounds = [mixer.Sound(file) for file in filepaths]
        self.repeat = False
        self.shuffle = False
        self.current_sound_index = 0
        self.interval = 0.05  # default interval between repeats in seconds
        self.repeat_thread = None
        self.channel = mixer.find_channel()

    def play_sound_once(self):
        if self.shuffle:
            sound = self.sounds[random.randint(0, len(self.sounds) - 1)]
        else:
            sound = self.sounds[self.current_sound_index]
            self.current_sound_index = (self.current_sound_index + 1) % len(self.sounds)
        self.channel.play(sound)

    def play_sound_repeat(self):
        self.repeat = True
        if self.repeat_thread is None or not self.repeat_thread.is_alive():
            self.repeat_thread = threading.Thread(target=self._repeat_loop, daemon=True)
            self.repeat_thread.start()

    def _repeat_loop(self):
        while self.repeat:
            if self.shuffle:
                sound = self.sounds[random.randint(0, len(self.sounds) - 1)]
            else:
                sound = self.sounds[self.current_sound_index]
                self.current_sound_index = (self.current_sound_index + 1) % len(self.sounds)
            self.channel.play(sound)
            while self.channel.get_busy() and self.repeat:  # Wait until the sound has finished playing
                pygame.time.delay(10)  # Small delay to avoid busy-waiting
            # Add random +-10% variation to the interval
            variation = random.uniform(0.9, 1.1)
            pygame.time.delay(int(self.interval * 1000 * variation))  # delay expects milliseconds

    def stop_repeat_sound(self):
        self.repeat = False
        self.channel.fadeout(1000)
    
    def set_volume(self, value):
        self.channel.set_volume(float(value))
