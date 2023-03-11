from objection_engine.v4.math_helpers import lerp
from .MovieKit import SceneObject
from PIL import Image, ImageDraw, ImageFont

VERDICT_FONT_SIZE = 70
VERDICT_FONT_START_SIZE_RATIO = 8 / 3
VERDICT_STROKE_WIDTH_RATIO = 1 / 14
VERDICT_STROKE_WIDTH = int(VERDICT_FONT_SIZE * VERDICT_STROKE_WIDTH_RATIO)

VERDICT_MAX_WIDTH = 230
VERDICT_SLAM_SPEED = 8.0


class JudgeVerdictTextObject(SceneObject):
    def __init__(
        self, parent: SceneObject = None, name: str = "", text: str = "Guilty"
    ):
        super().__init__(parent, name, (0, 0, 10))
        self._text = text

        self.normal_font = ImageFont.truetype(
            "./assets_v4/verdict/DFMinchoStd-W12.otf", VERDICT_FONT_SIZE
        )

        self.characters = self.calculate_positions()

    def get_text_bbox(self, text):
        bb = self.normal_font.getbbox(text)
        x1, y1, x2, y2 = bb

        padding = VERDICT_STROKE_WIDTH
        x1 -= padding
        y1 -= padding
        x2 += padding
        y2 += padding
        h = y2 - y1
        w = x2 - x1

        return (w, h)

    def calculate_positions(self):
        w, h = self.get_text_bbox(self._text)

        x_squish = min(1.0, VERDICT_MAX_WIDTH / w)
        chars = []
        for i, c in enumerate(self._text):
            next_char = "" if i == len(self._text) - 1 else self._text[i + 1]
            next_char_width = self.normal_font.getlength(next_char)
            char_width = self.normal_font.getlength(c + next_char) - next_char_width

            # For each character, make an image and store it along with the character
            # it holds and its getlength value
            char_img = Image.new("RGBA", self.get_text_bbox(c), (255, 0, 255, 128))
            char_img_ctx = ImageDraw.Draw(char_img)
            args = {
                "xy": (VERDICT_STROKE_WIDTH, VERDICT_STROKE_WIDTH),
                "text": c,
                "fill": (0, 0, 0),
                "stroke_width": VERDICT_STROKE_WIDTH,
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

            # Get bounding box stuff!
            # From https://github.com/python-pillow/Pillow/issues/3921#issuecomment-533085656
            bottom_1 = self.normal_font.getsize(self._text[i])[1]
            right, bottom_2 = self.normal_font.getsize(self._text[: i + 1])
            bottom = bottom_1 if bottom_1 < bottom_2 else bottom_2
            width, height = self.normal_font.getmask(c).size
            top = bottom - height
            left = right - width

            rect = (left, top, right, bottom)

            chars.append(
                {
                    "img": char_img,
                    "char": c,
                    "width": true_char_width,
                    "rect": rect,
                    "scale": VERDICT_FONT_START_SIZE_RATIO,
                    "visible": True,
                }
            )

        width_sum = sum([i["width"] for i in chars])
        return {"chars": chars, "width_sum": width_sum, "height": h}
    

    def update(self, delta):
        for character in self.characters["chars"]:
            if not character["visible"]:
                continue
            character["scale"] = max(
                1.0, character["scale"] - delta * VERDICT_SLAM_SPEED
            )


    def render(self, img: Image.Image, ctx: ImageDraw.ImageDraw):
        width_so_far = -int(self.characters["width_sum"] / 2)
        for character in self.characters["chars"]:
            if not character["visible"]:
                continue
            char_img: Image.Image = character["img"]
            char_width = character["width"]

            x = width_so_far
            y = character["rect"][1] - int(self.characters["height"] / 2)
            w = char_img.width
            h = char_img.height

            scale = character["scale"]
            scaled_w = int(char_img.width * scale)
            scaled_h = int(char_img.height * scale)

            # https://math.stackexchange.com/a/3055687
            scaled_x = x + int(w / 2) - int(scaled_w / 2)
            scaled_y = y + int(h / 2) - int(scaled_h / 2)
            scaled_char_img = char_img.resize(
                (scaled_w, scaled_h), resample=Image.Resampling.NEAREST
            )

            img.alpha_composite(
                scaled_char_img,
                (scaled_x + int(img.width / 2), scaled_y + int(img.height / 2)),
            )
            width_so_far += char_width
