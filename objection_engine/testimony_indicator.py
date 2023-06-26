from PIL import Image, ImageDraw, ImageFont
from os.path import join, exists
from objection_engine.MovieKit import SceneObject
from objection_engine.loading import ASSETS_FOLDER

TESTIMONY_STROKE_WIDTH = 2
TESTIMONY_INDICATOR_FONT_PATH = join(ASSETS_FOLDER, "testimony_indicator", "DINCondensed-Bold.ttf")

class TestimonyIndicatorTextObject(SceneObject):
    def __init__(self, parent: SceneObject = None, name: str = ""):
        super().__init__(parent, name, (0, 0, 10))
        self.font = None

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
    
    def set_text(self, text: str):
        self._text = text

        if self.font is None:
            return

        img = Image.new("RGBA", self.get_text_bbox(self._text), (255, 0, 255, 0))
        ctx = ImageDraw.Draw(img)
        ctx.fontmode = "1"
        ctx.text(
            xy=(TESTIMONY_STROKE_WIDTH, TESTIMONY_STROKE_WIDTH),
            text=self._text,
            fill=(255,255,255),
            stroke_width=TESTIMONY_STROKE_WIDTH,
            stroke_fill=(0,192,56),
            font=self.font,
            anchor="lt"
        )

        self.testimony_img = img.resize(
            (int(round(img.width * 0.65)), img.height),
            resample=Image.Resampling.NEAREST
        ).convert("RGBA")

    def render(self, img: Image.Image, ctx: ImageDraw.ImageDraw):
        if self.font is None:
            return
        img.paste(self.testimony_img,
                  (int(TESTIMONY_STROKE_WIDTH / 2) - 1, int(TESTIMONY_STROKE_WIDTH / 2) - 1),
                  self.testimony_img
                  )
