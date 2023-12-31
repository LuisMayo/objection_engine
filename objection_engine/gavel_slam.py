from objection_engine.loading import ASSETS_FOLDER, _print_note
from objection_engine.MovieKit import ImageObject, SceneObject
from os.path import join, exists

GAVEL_SLAM_PATH = join(ASSETS_FOLDER, "gavel_slam")

"""
https://www.youtube.com/watch?v=XBR35H_ya4g as reference
Single slam at 9:53
0 - 9 frames   (0.300s)
1 - 1 frame    (0.033s)
2 - 1 frame    (0.033s)
3 - 23 frames  (0.766s)

# Triple slam at 11:07
0 - 9 frames   (0.300s)
1 - 1 frame    (0.033s)
3 - 5 frames   (0.166s)
2 - 1 frame    (0.033s)
1 - 5 frames   (0.166s)
3 - 5 frames   (0.166s)
2 - 1 frame    (0.033s)
1 - 5 frames   (0.166s)
2 - 1 frame    (0.033s)
3 - 23 frames  (0.766s)

NOTE: using 0.033 for to indicate 1 frame didn't seem to work (it would simply
skip the frame) - instead, I rounded up fo 0.04.
"""

class GavelSlamObject(SceneObject):
    def __init__(self, parent: SceneObject = None, name: str = "", pos: tuple[int, int, int] = (0, 0, 0)):
        super().__init__(parent, name, pos)
        if not exists(GAVEL_SLAM_PATH):
            _print_note(
                f"Gavel slam assets not found at {GAVEL_SLAM_PATH}"
            )
            return

        self.bg_img = ImageObject(
            parent=self,
            name="Gavel Slam BG",
            pos=(0, 0, 11),
            filepath=join(GAVEL_SLAM_PATH, "gavel_slam_bg.png"),
        )

        self.block_img = ImageObject(
            parent=self,
            name="Gavel Slam Block",
            pos=(0, 0, 11),
            filepath=join(GAVEL_SLAM_PATH, "gavel_slam_block.png"),
        )

        self.gavel_frames = [
            ImageObject(
                parent=self,
                name="Gavel Frame 1",
                pos=(0, 0, 11),
                filepath=join(GAVEL_SLAM_PATH, "gavel_slam_gavel_1.png"),
            ),
            ImageObject(
                parent=self,
                name="Gavel Frame 2",
                pos=(0, 0, 11),
                filepath=join(GAVEL_SLAM_PATH, "gavel_slam_gavel_2.png"),
            ),
            ImageObject(
                parent=self,
                name="Gavel Frame 3",
                pos=(0, 0, 11),
                filepath=join(GAVEL_SLAM_PATH, "gavel_slam_gavel_3.png"),
            ),
        ]
        self.set_gavel_frame(0)

    def set_gavel_frame(self, frame: int = 0):
        for f in self.gavel_frames: f.hide()
        if frame <= 0 or frame > len(self.gavel_frames):
            return
        self.gavel_frames[frame - 1].show()
