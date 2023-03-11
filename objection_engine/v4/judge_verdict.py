from matplotlib.scale import scale_factory
from torch import clamp

from objection_engine.v4.math_helpers import lerp
from .MovieKit import SceneObject
from PIL import Image, ImageDraw, ImageFont

VERDICT_FONT_START_SIZE_RATIO = 5 / 3


class JudgeVerdictTextObject(SceneObject):
    def __init__(
        self, parent: SceneObject = None, name: str = "", text: str = "Guilty"
    ):
        super().__init__(parent, name, (0, 0, 10))
        self._text = text
        self.cache_image()

    def cache_image(self):
        font = ImageFont.truetype("./assets_v4/verdict/DFMinchoStd-W12.otf", int(54 * VERDICT_FONT_START_SIZE_RATIO))
        bb = font.getbbox(self._text)
        x1, y1, x2, y2 = bb

        stroke_width = int(font.size / 14)
        padding = stroke_width * 2
        x1 -= padding
        y1 -= padding
        x2 += padding
        y2 += padding

        h = y2 - y1
        w = x2 - x1
        text_img = Image.new("RGBA", (w, h), (255, 0, 255, 100))
        text_ctx = ImageDraw.Draw(text_img)
        args = {
            "xy": (int(w / 2), int(h / 2)),
            "text": self._text,
            "fill": (0, 0, 0),
            "stroke_width": stroke_width,
            "stroke_fill": (255, 255, 255),
            "font": font,
            "anchor": "mm",
        }
        text_ctx.text(**args)
        text_img = text_img.resize(
            (int(text_img.width * 0.8), text_img.height),
            resample=Image.Resampling.NEAREST,
        )
        self.text_img = text_img

        self.scale_amt = 1.0
        self.duration = 0.2
        self.time = 0.0

    def update(self, delta):
        t = self.time / self.duration
        self.scale_amt = lerp(1.0, 0.6, t)
        if t >= 1.0:
            self.scale_amt = 0.6
        self.time += delta

    def render(self, img: Image.Image, ctx: ImageDraw.ImageDraw):
        img_this_frame = self.text_img.resize((int(self.text_img.width * self.scale_amt), int(self.text_img.height * self.scale_amt)), resample=Image.Resampling.NEAREST)
        img.alpha_composite(
            img_this_frame,
            (
                int(img.width / 2 - img_this_frame.width / 2),
                int(img.height / 2 - img_this_frame.height / 2),
            ),
        )
