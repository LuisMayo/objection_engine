from typing import Dict
from PIL import Image, ImageDraw, ImageFont
from fontTools.ttLib import TTFont

class AnimText:
    font_array = [
        # AA-Like > Pixel > Generic
        # AA-like, Latin, hiragana, katakana, (part of) cyrillic
        {'path': './assets/igiari/Igiari.ttf'},
        # AA-like, Latin, hiragana, katakana, (part of) cyrillic
        {'path': './assets/igiari/Galmuri11.ttf'},
        # Pixel, Kanji, Hiragana, Katakana
        {'path':'./assets/igiari/jackeyfont.ttf'},
        # Arabic
        {'path':'./assets/igiari/arabic-1.ttf', 'size': 12},
        # Pixel-font, Hebrew
        {'path':'./assets/igiari/STANRG__.ttf'},
        # Generic
        {'path':'./assets/igiari/NotoSans-Regular.ttf'},
        # Pixel font, Arabic
        {'path':'./assets/igiari/bitsy-font-with-arabic.ttf', 'size': 10},
    ]
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
        # Used for font handling internals
        self._internal_text = text.replace('\n', '').replace('\r', '').replace('\t', '')
        self.typewriter_effect = typewriter_effect
        self.font_size = font_size
        self.font = self._select_best_font()
        self.font_path = self.font['path']
        if ('size' in self.font):
            self.font_size = self.font['size']
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
        best_font = self.font_array[-1]
        best_font_points = 0
        for font in self.font_array:
            font_points = self._check_font(font)
            if font_points > best_font_points:
                best_font_points = font_points
                best_font = font
            if best_font_points >= len(self._internal_text):
                return font
        print(f'WARNING. NO OPTIMAL FONT FOUND, font score: {best_font_points}/{len(self._internal_text)}, text {self._internal_text}')
        return best_font

    def _check_font(self, font):
        font_path = font['path']
        font = TTFont(font_path)
        # We check all chars for presence on the font
        valid_char = 0
        for char in self._internal_text:
            # We check if the char is in any table of the font
            for table in font['cmap'].tables:
                if ord(char) in table.cmap:
                    valid_char += 1
                    break
        return valid_char

    def __str__(self):
        return self.text
