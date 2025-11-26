"""2611 2025
10:08
threading control for soundboks"""

from tkinter import *
import queue
from tkinter import ttk
from tkinterdnd2 import DND_FILES, TkinterDnD
from pygame import mixer
import threading
import time
import random
import concurrent.futures 
from pathlib import Path

"""1810 2025
20:59
importing pdb for finding out where the mixer comes from"""

import pdb #debugger



randomGen = random.Random()
keep_playing = True
#truly the product is not important
global_mod_object_for_thread_options = "testing 1 1 1"
def soundplayerThread(sounds, timeToWait, queue): #sounds is a list
    """this threads the soundplaying, to keep the gui responsive."""
    counter = 0 #how many times should it  play?
    while counter < 2: #her skal jeg lægge lyd afspilnings logikken
        print("sounds counting,", counter)
        if (keep_playing):
            print("its true")
        else:
            print("its false")
        print(global_mod_object_for_thread_options)
        for sound in sounds:
            print("inside sound in sounds for loop of soundplayerThread")
            sound.set_volume(0.2)
        randomInt = randomGen.randrange(0, len(sounds))
        sounds[randomInt].play() #it just does ok
        time.sleep(2) #how long should it wait between plays?
        counter += 1

class PlayerGUI:
    def __init__(self, root):
        self.pool = concurrent.futures.ThreadPoolExecutor()
        self.root = root
        self.mixer = mixer.init()
        #breakpoint()
        self.root.title("SoundPlayer 001 dropper")
        self.label = ttk.Label(root, text="Drag here sound files", relief="groove")
        self.label.grid(column=0, row=0)

        self.root.drop_target_register(DND_FILES)
        self.root.dnd_bind('<<Drop>>', self.start_file)     

        self.area = ttk.Frame(root, padding="3 3 12 12", relief="raised")
        self.area.grid(column=0, row=0)
        
        self.text = ttk.Label(self.area, text="Top", relief="groove") #top
        self.text.grid(column=1, row=1)

        self.area2 = ttk.Frame(root, padding="3 3 12 12", relief="raised") #bottom
        self.area2.grid(column=0, row=1)
        
        self.text2 = ttk.Label(self.area2, text="bottom", relief="groove")
        self.text2.grid(column=0, row=0)

        self.text3 = ttk.Label(self.area2, text="bottom-1")
        
        self.root.bind("<Return>", self.quitIt)
        self.root.bind("<Escape>", self.quitIt)
        self.root.bind("a", self.hitIt)
        
        self.soundBox = ttk.Frame(self.area2, relief="groove") #den første soundboks holder
        self.soundBox.grid() 

        self.startButton = ttk.Button(self.soundBox, text="Play")
        self.startButton.grid(column=0, row=0)

        self.stopButton = ttk.Button(self.soundBox, text="Stop")
        self.stopButton.grid(column=1, row=0)

        self.repeatButton = ttk.Button(self.soundBox, text="repeat")
        self.repeatButton.grid(column=2, row=0)

        self.volume_label = ttk.Label(self.soundBox, text="VOL")
        self.volume_label.grid(column=0, row=1)

        self.volumeSlider = ttk.Scale(self.soundBox, orient="horizontal")
        self.volumeSlider.grid(column=1, row=1)

        self.interval_label = ttk.Label(self.soundBox, text="Interval")
        self.interval_label.grid(column=2, row=1)

        self.interval_slider = ttk.Scale(self.soundBox, orient="horizontal")
        self.interval_slider.grid(column=3, row=1)


    def quitIt(self, event):
        """easy-acccess quitting on enter or escape key."""
        print("Quitting!")
        self.root.destroy()
    
    hitItCounter = 0
    def hitIt(self, event):
        """easy-access program interaction, for testing if it hangs."""
        print("hitting it!", self.hitItCounter)
        self.hitItCounter += 1

    def start_file(self, event):
        newQueue = queue.Queue()
        """This is the function that handles the drag-dropped file."""
        print("start_file")
        print("sf, self:", self)
        timeToWait = 2500
        print("event.data in start_file:", event.data)
        files = list(self.root.tk.splitlist(event.data))
        print("files list in start_file:", files)
        sounds = []
        for file in files:
            sound = mixer.Sound(file)
            sound.set_volume(0.2) #sets volume to low, for testing purpose
            sounds.append(sound)
        self.pool.submit(soundplayerThread, sounds, timeToWait, queue)
        self.add_playerbox(self, event)

    def add_playerbox(self, event, thing):
        print("file dropped, im gonna be a new box")
        print("self:", self)
        print("event:", event)
        print("thing:", thing)

test = True
if __name__ == "__main__":

    root = TkinterDnD.Tk()
    PlayerGUI(root)
    root.geometry("400x300")

    if (test):
        filepath = Path("testfile.mp3").absolute()
        print("file is:", filepath.is_file())
        
        # PlayerGUI.start_file(list(str(event)), 1)

root.mainloop()