from direct.showbase.ShowBase import ShowBase
from panda3d.core import MovieTexture, CardMaker
from panda3d.core import TransparencyAttrib
from panda3d.core import AudioSound
from direct.task import Task

class StoryScene(ShowBase):
    def __init__(self):
        super().__init__()

        # Movie textures for each scene
        self.storySceneInitial = MovieTexture("initialScene")
        if not self.storySceneInitial.read("../Assets/Scenes/initialScene.mp4"):
            print("Failed to load Initial Scene!")

        self.storySceneEarly = MovieTexture("earlyScene")
        if not self.storySceneEarly.read("../Assets/Scenes/earlyPhaseScene.mp4"):
            print("Failed to load Early Scene!")

        self.storySceneMid = MovieTexture("midScene")
        if not self.storySceneMid.read("../Assets/Scenes/midPhaseScene.mp4"):
            print("Failed to load Mid Scene!")

        self.storySceneFinal = MovieTexture("finalScene")
        if not self.storySceneFinal.read("../Assets/Scenes/finalPhaseScene.mp4"):
            print("Failed to load Final Scene!")

        # Audio files
        self.initialSceneAudio = self.loader.loadSfx("../Assets/Scenes/initialScene.mp4")
        self.earlySceneAudio = self.loader.loadSfx("../Assets/Scenes/earlyPhaseScene.mp4")
        self.midSceneAudio = self.loader.loadSfx("../Assets/Scenes/midPhaseScene.mp4")
        self.finalSceneAudio = self.loader.loadSfx("../Assets/Scenes/finalPhaseScene.mp4")

        # Card for the movies
        cm = CardMaker("cutscene_card")
        cm.setFrameFullscreenQuad()
        self.cutsceneCard = self.render2d.attachNewNode(cm.generate())
        self.cutsceneCard.setTransparency(TransparencyAttrib.MAlpha)
        self.cutsceneCard.hide()

        self.currentTexture = None
        self.currentAudio = None

    def playScene(self, sceneTexture, sceneAudio):
        if self.currentTexture and self.currentTexture.isPlaying():
            self.currentTexture.stop()
        if self.currentAudio and self.currentAudio.status() == AudioSound.PLAYING:
            self.currentAudio.stop()

        self.cutsceneCard.setTexture(sceneTexture)
        self.cutsceneCard.show()
        sceneTexture.play()

        sceneAudio.setTime(0.0)
        sceneAudio.play()

        self.currentTexture = sceneTexture
        self.currentAudio = sceneAudio

        self.taskMgr.add(self.checkMovieDone, "check_movie_done")

    def checkMovieDone(self, task):
        if self.currentTexture and not self.currentTexture.isPlaying():
            self.cutsceneCard.hide()

            if self.currentAudio and self.currentAudio.status() == AudioSound.PLAYING:
                self.currentAudio.stop()

            self.taskMgr.remove("check_movie_done")
            print("Cutscene ended.")
            return Task.done
        return Task.cont

    def playInitialScene(self):
        self.playScene(self.storySceneInitial, self.initialSceneAudio)

    def playEarlyScene(self):
        self.playScene(self.storySceneEarly, self.earlySceneAudio)

    def playMidScene(self):
        self.playScene(self.storySceneMid, self.midSceneAudio)

    def playFinalScene(self):
        self.playScene(self.storySceneFinal, self.finalSceneAudio)
