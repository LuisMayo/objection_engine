from PIL import Image, ImageDraw, ImageFont
from fontTools.ttLib import TTFont

class AnimText:
    font_array = ['./assets/igiari/Igiari.ttf', './assets/igiari/STANRG__.ttf']
    def __init__(
        self,
        text: str,
        *,
        x: int = 0,
        y: int = 0,
        font_path: str = None,
        font_size: int = 12,
        typewriter_effect: bool = False,
        colour: str = "#ffffff",
    ):
        self.x = x
        self.y = y
        self.text = text
        self.typewriter_effect = typewriter_effect
        self.font_path = self._select_best_font()
        self.font_size = font_size
        self.colour = colour

    def render(self, background: Image, frame: int = 0):
        draw = ImageDraw.Draw(background)
        _text = self.text
        if self.typewriter_effect:
            _text = _text[:frame]
        if self.font_path is not None:
            font = ImageFont.truetype(self.font_path, self.font_size)
            draw.text((self.x, self.y), _text, font=font, fill=self.colour)
        else:
            draw.text((self.x, self.y), _text, fill=self.colour)
        return background

    def _select_best_font(self):
        for font_path in self.font_array:
            if self._check_font(font_path):
                return font_path
        print('WARNING. NO SUITABLE FONT FOUND')
        return self.font_array[0]

    def _check_font(self, font_path):
        font = TTFont(font_path)
        # We check all chars for presence on the font
        for char in self.text:
            valid_char = False
            # We check if the char is in any table of the font
            for table in font['cmap'].tables:
                if ord(char) in table.cmap:
                    valid_char = True
                    break
            if not valid_char:
                return False
        return True

    def __str__(self):
        return self.text
