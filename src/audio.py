from direct.showbase.ShowBase import ShowBase
from direct.gui.OnscreenText import OnscreenText
from direct.gui.DirectGui import *
from direct.gui.DirectGui import DirectWaitBar
from direct.task import Task
from panda3d.core import *
import speech_recognition as sr
import pyaudio
import numpy as np
# import sys

# change to AudioIOManager
class audioManager:
    def __init__(self, base):
        self.base = base

        self.recognizer = sr.Recognizer()
        self.pyaudio = pyaudio.PyAudio()
        self.inputDevice = None
        self.outputDevice = None
        self.stream = None

        #Sound effects library 
        self.soundEffects = {
            "testMusic" : self.base.loader.loadSfx('../Assets/Audio/testSong.mp3'),
            "testSound" : self.base.loader.loadSfx('../Assets/Audio/testSound.mp3')
        }

        #self.soundEffects['testSound'].play()
    
    def itemSel(self, selection):
        self.selectedDevice = selection

    def listAudioInput(self):
        self.inputDeviceList = []
        seenDevices = set()

        for i in range(self.pyaudio.get_device_count()):
            inputDevice = self.pyaudio.get_device_info_by_index(i)
            
            if (
                inputDevice['maxInputChannels'] > 0
                and inputDevice['name'] not in seenDevices
                and "Microsoft" not in inputDevice['name']
                and "Mapper" not in inputDevice['name']
                and "Primary" not in inputDevice['name']
                and "Array" not in inputDevice['name']
                and "Sonar" not in inputDevice['name']
                and "Hands-Free" not in inputDevice['name']
                and (
                    "Microphone" in inputDevice['name'] or
                    "Headset" in inputDevice['name']
                )
            ):
                self.inputDeviceList.append(inputDevice['name'])
                seenDevices.add(inputDevice['name'])
                
        return self.inputDeviceList
    
    def selectAudioInput(self):
        self.audInMenu = DirectOptionMenu(
            text="Audio Output",
            scale=0.12,
            command=self.itemSel,
            items=self.listAudioInput(),
            initialitem=1,
            highlightColor=(0.65, 0.65, 0.65, 1)
        )

    def listAudioOutput(self):
        self.outputDeviceList = []
        seenDevices = set()

        for i in range(self.pyaudio.get_device_count()):
            outputDevice = self.pyaudio.get_device_info_by_index(i)
            
            if (
                outputDevice['maxOutputChannels'] > 0
                and outputDevice['name'] not in seenDevices
                and "Microsoft" not in outputDevice['name']
                and "Mapper" not in outputDevice['name']
                and "Primary" not in outputDevice['name']
                and "Array" not in outputDevice['name']
                and "Sonar" not in outputDevice['name']
                and "Hands-Free" not in outputDevice['name']
                and (
                    "Speakers" in outputDevice['name'] or
                    "Headset" in outputDevice['name'] or
                    "Headphones" in outputDevice['name']
                )
            ):
                self.outputDeviceList.append(outputDevice['name'])
                seenDevices.add(outputDevice['name'])
                
        return self.outputDeviceList

    def selectAudioOutput(self):
        self.audInMenu = DirectOptionMenu(
            text="Audio Output",
            scale=0.12,
            command=self.itemSel,
            items=self.listAudioOutput(),
            initialitem=1,
            highlightColor=(0.65, 0.65, 0.65, 1)
        )

    def testAudioInput(self):
        try:
            with sr.Microphone(device_index=self.inputDevice) as source:
                self.volumeBar = DirectWaitBar(
                    text="",
                    value=0,
                    range=100,
                    pos=(0, 0, 0)
                )

            def updateVolume():
                try:
                    audio = self.recognizer.listen(source, timeout = 5, phrase_time_limit=5)
                    data = np.frombuffer(audio.frame_data, dtype=np.int16)
                    volume = (np.abs(data).mean() / 32768.0) * 100
                    self.volumeBar['value'] = volume

                    print(f"Volume Level: {volume}%")

                except sr.WaitTimeoutError:
                    self.volumeBar['value'] = 0

            self.base.taskMgr.add(updateVolume, "Update Volume")


        except:
            print("Microphone not recognized")

    def testAudioOutput(self):
        self.testOutputDevice = DirectButton(
                text="Stop",
                scale=0.1,
                pos=(0,0,0.8),
                command=self.soundEffects['testSound'].play()
            )
        
    # Change to setOutputVolumeValue
    def setVolumeValue(self, value):
        for self.name, self.sound in self.soundEffects.items():
            self.sound.setVolume(value)