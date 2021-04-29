from typing import List
from beans import scene
import cv2
import os
import numpy as np

class AnimVideo:
    def __init__(self, scenes: List[scene.AnimScene], fps: int = 10):
        self.scenes = scenes
        self.fps = fps
    # @profile
    def render(self, output_path: str = None):
        if output_path is None:
            if not os.path.exists("tmp"):
                os.makedirs("tmp")
            rnd_hash = random.getrandbits(64)
            output_path = f"tmp/{rnd_hash}.mp4"
        fourcc = cv2.VideoWriter_fourcc(*"avc1")
        background = self.scenes[0].frames[0]
        if os.path.isfile(output_path):
            os.remove(output_path)
        video = cv2.VideoWriter(output_path, fourcc, self.fps, background.size)
        for scene in self.scenes:
            for frame in scene.frames:
                video.write(cv2.cvtColor(np.array(frame), cv2.COLOR_RGB2BGR))
        video.release()
        return output_path
