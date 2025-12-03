"""0312 2025
09:42
class for saving the sound information. It should take some settings data, and save it.
"""

import json

def save_settings(sound_player):
    #with open('settings.json', 'w') as json_file:
#this assumes the json  is ready to print
        #json.dump(sound_player, json_file)
    format_for_json(sound_player)

def format_for_json(sound_player): 
    #this  shoiuld make the json from t he settings
    json_savefile = {
        "volume": sound_player.get_volume()
    }
    print("new jsoin:", json_savefile)
