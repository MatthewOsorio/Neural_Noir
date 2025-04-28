from direct.showbase.ShowBase import ShowBase
from panda3d.core import MovieTexture, CardMaker, TransparencyAttrib, AudioSound, TextureStage, Filename
from direct.task import Task
import os

def to_panda_path(path):
    path = os.path.abspath(path).replace("\\", "/")
    if path[1] == ":":
        path = "/" + path[0].lower() + path[2:]
    return path

class StoryScene:
    def __init__(self, base):
        self.base = base

        # Paths
        early_scene_path = to_panda_path("Assets/Scenes/earlyPhaseScene.mp4")
        mid_scene_path = to_panda_path("Assets/Scenes/midPhaseScene.mp4")
        final_scene_path = to_panda_path("Assets/Scenes/finalPhaseScene.mp4")

        # Load movie textures
        self.storySceneEarly = MovieTexture("earlyScene")
        if not self.storySceneEarly.read(early_scene_path):
            print(f"Failed to load Early Scene from {early_scene_path}")

        self.storySceneMid = MovieTexture("midScene")
        if not self.storySceneMid.read(mid_scene_path):
            print(f"Failed to load Mid Scene from {mid_scene_path}")

        self.storySceneFinal = MovieTexture("finalScene")
        if not self.storySceneFinal.read(final_scene_path):
            print(f"Failed to load Final Scene from {final_scene_path}")

        # Prevent looping
        self.storySceneEarly.setLoop(False)
        self.storySceneMid.setLoop(False)
        self.storySceneFinal.setLoop(False)

        # Load audio for each scene
        self.earlySceneAudio = self.base.loader.loadSfx(early_scene_path)
        self.midSceneAudio = self.base.loader.loadSfx(mid_scene_path)
        self.finalSceneAudio = self.base.loader.loadSfx(final_scene_path)

        # Fullscreen movie card
        hSize = self.base.getAspectRatio()
        cm = CardMaker("cutscene_card")
        cm.setFrame(-1.315 * hSize, 1.315 * hSize, -1, 1)
        self.cutsceneCard = self.base.aspect2d.attachNewNode(cm.generate())
        self.cutsceneCard.setTransparency(TransparencyAttrib.MAlpha)
        self.cutsceneCard.setTexture(self.storySceneEarly)
        self.cutsceneCard.setBin('fixed', 1)
        self.cutsceneCard.hide()

        self.currentTexture = None
        self.currentAudio = None
        self.onSuccessCallback = None

    def playScene(self, sceneTexture, sceneAudio, onSuccessCallback=None):
        if self.currentTexture and self.currentTexture.isPlaying():
            self.currentTexture.stop()
        if self.currentAudio and self.currentAudio.status() == AudioSound.PLAYING:
            self.currentAudio.stop()

        self.cutsceneCard.setTexture(sceneTexture)
        self.cutsceneCard.show()

        texScale = sceneTexture.getTexScale()
        self.cutsceneCard.setTexScale(TextureStage.getDefault(), texScale[0], texScale[1])
        self.cutsceneCard.setTexOffset(TextureStage.getDefault(), 0, 0)

        sceneTexture.play()
        sceneAudio.setTime(0.0)
        sceneAudio.play()

        self.currentTexture = sceneTexture
        self.currentAudio = sceneAudio
        self.onSuccessCallback = onSuccessCallback

        self.base.taskMgr.add(self.checkMovieDone, "check_movie_done")

    def checkMovieDone(self, task):
        if self.currentTexture.getTime() >= self.currentTexture.getVideoLength():
            self.cutsceneCard.hide()

            if self.currentAudio and self.currentAudio.status() == AudioSound.PLAYING:
                self.currentAudio.stop()

            self.afterCutscene()

            return task.done
        return task.cont
    
    def afterCutscene(self):
        if self.onSuccessCallback:
            self.onSuccessCallback()

    def playEarlyScene(self,onSuccessCallback=None):
        self.playScene(self.storySceneEarly, self.earlySceneAudio, onSuccessCallback)

    def playMidScene(self, onSuccessCallback=None):
        self.playScene(self.storySceneMid, self.midSceneAudio, onSuccessCallback)

    def playFinalScene(self, onSuccessCallback=None):
        self.playScene(self.storySceneFinal, self.finalSceneAudio, onSuccessCallback)
 