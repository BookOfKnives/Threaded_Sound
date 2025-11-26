from pygame import mixer
import random

class sound_player:
    def __init__(self, filepaths : list[str]):
        if mixer.get_init() is None:
            raise Exception("Pygame mixer not initialized.")
        if not filepaths:
            raise ValueError("No filepaths provided to sound_player.")
        self.sounds = [mixer.Sound(file) for file in filepaths]
        self.repeat = False

    def play_sound_once(self):
        sound = mixer.Sound(self.sounds[random.randint(0, len(self.sounds) - 1)])
        sound.play()

    # def play_sound_repeat(self, sound_file):
    #     while self.repeat:
    #         sound = self._mixer.Sound(sound_file)
    #     sound.play(-1)  # -1 means loop until stop() is called

    # def stop_repeat_sound(self, sound_file):
    #     sound = self._mixer.Sound(sound_file)
    #     sound.stop()