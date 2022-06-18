from typing import List
from . import scene
import cv2
import os
import numpy as np
import random

class AnimVideo:
    def __init__(self, scenes: List[scene.AnimScene], fps: int = 10, resolution_scale: int = 1):
        self.scenes = scenes
        self.fps = fps
        self.resolution_scale = resolution_scale
    # @profile
    def render(self, output_path: str = None):
        if output_path is None:
            if not os.path.exists("tmp"):
                os.makedirs("tmp")
            rnd_hash = random.getrandbits(64)
            output_path = f"tmp/{rnd_hash}.mp4"

        fourcc = cv2.VideoWriter_fourcc(*"h264") if os.getenv('OE_DIRECT_H264_ENCODING', 'false') == 'true' else cv2.VideoWriter_fourcc(*"mp4v")
        background = self.scenes[0].frames[0]
        if os.path.isfile(output_path):
            os.remove(output_path)
        video_dimensions = background.size
        if self.resolution_scale != 1:
            video_dimensions = (background.size[0] * self.resolution_scale, background.size[1] * self.resolution_scale)
        video = cv2.VideoWriter(output_path, fourcc, self.fps, video_dimensions)
        for scene in self.scenes:
            for frame in scene.frames:
                cv2_frame = cv2.cvtColor(np.array(frame), cv2.COLOR_RGB2BGR)
                if(self.resolution_scale > 1):
                    # use cv2.resize to scale the frame with integer scaling
                    cv2_frame = cv2.resize(cv2_frame, (0, 0), fx=self.resolution_scale, fy=self.resolution_scale, interpolation=cv2.INTER_NEAREST)
                video.write(cv2_frame)
        video.release()
        return output_path
