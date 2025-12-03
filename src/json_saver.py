"""0312 2025
09:42
class for saving the sound information. It should take some settings data, and save it.
"""

import json
import pathlib

#make file dialog

def save_settings(sound_player):
    """write the file to  disk."""
    json_savefile = format_for_json(sound_player)
    try:
        with open(pathlib.Path('saves/save.json'), 'w') as file: 
            json.dump(json_savefile, file)
        print("operation complete")
    except Exception as e:
        print(f'An error occured in save_settings() in {__name__}: {e}')

def format_for_json(sound_player): 
    """formats the sound settings into json"""
    json_savefile = {
        "volume": sound_player.get_volume(),
        "keybind": sound_player.get_keybind(),
        "shuffle": sound_player.get_shuffle(),
        "filepaths": sound_player.get_filepaths(),
    }
    return json_savefile

