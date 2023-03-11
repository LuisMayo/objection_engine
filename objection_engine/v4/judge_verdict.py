from matplotlib.scale import scale_factory
from torch import clamp

from objection_engine.v4.math_helpers import lerp
from .MovieKit import SceneObject
from PIL import Image, ImageDraw, ImageFont

VERDICT_FONT_SIZE = 54
VERDICT_FONT_START_SIZE_RATIO = 5 / 3
VERDICT_STROKE_WIDTH_RATIO = 1 / 14

VERDICT_MAX_WIDTH = 221


class JudgeVerdictTextObject(SceneObject):
    def __init__(
        self, parent: SceneObject = None, name: str = "", text: str = "Guilty"
    ):
        super().__init__(parent, name, (0, 0, 10))
        self._text = text

        self.normal_font = ImageFont.truetype(
            "./assets_v4/verdict/DFMinchoStd-W12.otf", VERDICT_FONT_SIZE
        )

        self.cache_image()
        self.characters = self.calculate_positions()
        print(self.characters)

    def get_text_bbox(self, text):
        bb = self.normal_font.getbbox(text)
        x1, y1, x2, y2 = bb
        stroke_width = int(self.normal_font.size * VERDICT_STROKE_WIDTH_RATIO)
        padding = stroke_width
        x1 -= padding
        y1 -= padding
        x2 += padding
        y2 += padding
        h = y2 - y1
        w = x2 - x1

        return (w, h)

    def calculate_positions(self):
        bb = self.normal_font.getbbox(self._text)
        x1, y1, x2, y2 = bb
        stroke_width = int(self.normal_font.size * VERDICT_STROKE_WIDTH_RATIO)
        padding = stroke_width * 2
        x1 -= padding
        y1 -= padding
        x2 += padding
        y2 += padding
        h = y2 - y1
        w = x2 - x1

        x_squish = min(1.0, VERDICT_MAX_WIDTH / w)
        print(f"Verdict max width is {VERDICT_MAX_WIDTH} and width is {w}, so x squish will be {x_squish}")

        chars = []
        for i, c in enumerate(self._text):
            next_char = "" if i == len(self._text) - 1 else self._text[i + 1]
            next_char_width = self.normal_font.getlength(next_char)

            char_width = self.normal_font.getlength(c + next_char) - next_char_width

            # TODO: For each character, make an image and store it along with the character
            # it holds and its getlength value
            char_img = Image.new("RGBA", self.get_text_bbox(c), (255, 0, 255, 128))
            char_img_ctx = ImageDraw.Draw(char_img)
            args = {
                "xy": (0,0),#(int(char_img.width / 2), int(char_img.height / 2)),
                "text": c,
                "fill": (0, 0, 0),
                "stroke_width": int(VERDICT_FONT_SIZE * VERDICT_STROKE_WIDTH_RATIO),
                "stroke_fill": (255, 255, 255),
                "font": self.normal_font,
                "anchor": "lt",
            }
            char_img_ctx.text(**args)

            # Squish character on X axis if the whole string will be too wide
            char_img = char_img.resize(
                (int(char_img.width * x_squish), char_img.height)
            )
            true_char_width = int(char_width * x_squish)

            chars.append({"img": char_img, "width": true_char_width})

        return chars

    def cache_image(self):
        font = ImageFont.truetype(
            "./assets_v4/verdict/DFMinchoStd-W12.otf",
            int(VERDICT_FONT_SIZE * VERDICT_FONT_START_SIZE_RATIO),
        )

        bb = font.getbbox(self._text)
        x1, y1, x2, y2 = bb
        stroke_width = int(font.size * VERDICT_STROKE_WIDTH_RATIO)
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
        width_so_far = 0
        for character in self.characters:
            char_img = character["img"]
            char_width = character["width"]

            img.alpha_composite(char_img, (width_so_far, 0))
            width_so_far += char_width
