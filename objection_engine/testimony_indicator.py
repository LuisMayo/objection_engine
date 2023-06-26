from PIL import Image, ImageDraw, ImageFont
from os.path import join, exists
from objection_engine.MovieKit import SceneObject
from objection_engine.loading import ASSETS_FOLDER

TESTIMONY_STROKE_WIDTH = 2
TESTIMONY_INDICATOR_FONT_PATH = join(
    ASSETS_FOLDER, "testimony_indicator", "DINCondensed-Bold.ttf"
)

"""
Visible for 43 frames (1.433s)
Invisible for 10 frames (0.34s)
"""


class TestimonyIndicatorTextObject(SceneObject):
    def __init__(self, parent: SceneObject = None, name: str = ""):
        super().__init__(parent, name, (0, 0, 10))
        self.text_visible_time = 1.43
        self.text_invisible_time = 0.34
        self.font = None
        self.time_remaining = self.text_visible_time
        self.text_visible = True
        self.can_be_displayed = False

        self.stroke_color = (0, 192, 56)
        self.fill_color = (255, 255, 255)

        if not exists(TESTIMONY_INDICATOR_FONT_PATH):
            return

        self.font = ImageFont.truetype(TESTIMONY_INDICATOR_FONT_PATH, 32)
        self.set_text("Testimony")

    def get_text_bbox(self, text: str):
        x1, y1, x2, y2 = self.font.getbbox(text)
        x1 -= TESTIMONY_STROKE_WIDTH
        y1 -= TESTIMONY_STROKE_WIDTH
        x2 += TESTIMONY_STROKE_WIDTH
        y2 += TESTIMONY_STROKE_WIDTH
        return (x2 - x1, y2 - y1)

    def set_fill_color(self, color: tuple[int, int, int] = None):
        self.fill_color = color if color is not None else (255,255,255)
        self.render_internal_graphic()

    def set_stroke_color(self, color: tuple[int, int, int] = None):
        self.stroke_color = color if color is not None else (0, 192, 56)
        self.render_internal_graphic()

    def set_text(
        self,
        text: str
    ):
        self._text = text
        self.render_internal_graphic()
        
    def render_internal_graphic(self):
        if self.font is None:
            return
        img = Image.new("RGBA", self.get_text_bbox(self._text), (255, 0, 255, 0))
        ctx = ImageDraw.Draw(img)
        ctx.fontmode = "1"
        ctx.text(
            xy=(TESTIMONY_STROKE_WIDTH, TESTIMONY_STROKE_WIDTH),
            text=self._text,
            fill=self.fill_color,
            stroke_width=TESTIMONY_STROKE_WIDTH,
            stroke_fill=self.stroke_color,
            font=self.font,
            anchor="lt",
        )

        self.testimony_img = img.resize(
            (int(round(img.width * 0.65)), img.height),
            resample=Image.Resampling.NEAREST,
        ).convert("RGBA")

    def make_visible(self):
        self.can_be_displayed = True
        self.reset_timing()

    def make_invisible(self):
        self.can_be_displayed = False

    def reset_timing(self):
        self.text_visible = True
        self.time_remaining = self.text_visible_time

    def update(self, delta):
        self.time_remaining -= delta

        while self.time_remaining < 0.0:
            if self.text_visible:
                self.text_visible = False
                self.time_remaining += self.text_invisible_time
            else:
                self.text_visible = True
                self.time_remaining += self.text_visible_time

    def render(self, img: Image.Image, ctx: ImageDraw.ImageDraw):
        if self.font is None:
            return

        if not self.can_be_displayed:
            return
        
        if not self.text_visible:
            return

        img.paste(
            self.testimony_img,
            (int(TESTIMONY_STROKE_WIDTH / 2) - 1, int(TESTIMONY_STROKE_WIDTH / 2) - 1),
            self.testimony_img,
        )
