from direct.showbase.ShowBase import ShowBase
from direct.gui.OnscreenText import OnscreenText
from direct.gui.DirectGui import *
from direct.gui.DirectGui import DirectWaitBar
from direct.task import Task
from direct.actor import Actor
from direct.interval.IntervalGlobal import *
from panda3d.core import *
import speech_recognition as sr
import pyaudio
import pygame
import numpy as np
import threading

# change to AudioIOManager
class audioManager:
    def __init__(self, base):
        self.base = base

        self.recognizer = sr.Recognizer()
        self.pyaudio = pyaudio.PyAudio()
        self.inputDevice = None
        self.outputDevice = None
        self.stream = None
        pygame.mixer.init()

        #Sound effects library 
        self.soundEffects = {
            "errorSound" : pygame.mixer.Sound('../Neural_Noir/Assets/Audio/ErrorSound.mp3')
        }

        #self.soundTest = self.soundEffects.get("testMusic")
        #self.soundTest.play()
    
    ''' Additional functionality for audio devices that can be handled instead by the OS

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
    '''

    def testAudioInput(self):
        self.dialog = DirectDialog(
            frameSize=(-0.5, 0.5, -0.3, 0.3),
            fadeScreen=0.4,
            text="Say Something!",
            text_align=TextNode.ACenter,
            text_scale=0.1
        )

        self.audio_detected = False

        def check_mic_input(task):
            try:
                while True:
                    with sr.Microphone() as source:
                        audio = self.recognizer.listen(source, timeout=0.5, phrase_time_limit=0.5)
                        data = np.frombuffer(audio.frame_data, dtype=np.int16) # calculate volume in percentage
                        volume = (np.abs(data).mean() / 32768.0) * 100

                        if volume > 0:
                            self.audio_detected = True
                            self.close_dialog()
                            self.dialog = DirectDialog(
                                frameSize=(-0.8, 0.8, -0.3, 0.3),
                                fadeScreen=0.4,
                                text="Microphone Recognized!",
                                text_align=TextNode.ACenter,
                                text_scale=0.1
                            )
                            self.base.taskMgr.doMethodLater(3, self.close_dialog, "CloseDialog")  # close box after 3 seconds
                            return Task.done
            except sr.WaitTimeoutError:
                pass

            return Task.cont

        def check_no_audio(task):
            if not self.audio_detected:
                self.dialog['text'] = "No Audio Detected!"
                self.base.taskMgr.doMethodLater(3, self.close_dialog, "CloseDialog")  # close box after 2 seconds
            return Task.done

        # Check for audio and handle no audio after 5 seconds
        self.base.taskMgr.add(check_mic_input, "CheckMicInput")
        self.base.taskMgr.doMethodLater(5, check_no_audio, "CheckNoAudio")

    # explicitly destroy the message box so it disappears from the audio settings menu
    def close_dialog(self, task=None):
        if hasattr(self, "dialog") and self.dialog:
            self.dialog.destroy()
            self.dialog = None
        return Task.done

    def testAudioOutput(self):
        self.soundEffects['errorSound'].play()
    
    # Change to setOutputVolumeValue
    def setVolumeValue(self, value):
        for self.name, self.sound in self.soundEffects.items():
            self.sound.set_volume(value)

    def playSound(self, sound):
        self.soundName = self.soundEffects.get(sound)
        self.soundName.play()