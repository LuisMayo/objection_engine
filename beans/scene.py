from typing import List
from beans.img import AnimImg
from beans.text import AnimText

class AnimScene:
    def __init__(self, arr: List, length: int, start_frame: int = 0):
        self.frames = []
        text_idx = 0
        #         print([str(x) for x in arr])
        for idx in range(start_frame, length + start_frame):
            if isinstance(arr[0], AnimImg):
                background = arr[0].render()
            else:
                background = arr[0]
            for obj in arr[1:]:
                if isinstance(obj, AnimText):
                    obj.render(background, frame=text_idx)
                else:
                    obj.render(background, frame=idx)
            self.frames.append(background)
            text_idx += 1
