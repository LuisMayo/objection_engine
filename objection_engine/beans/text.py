from enum import IntEnum
from typing import Dict
from PIL import Image, ImageDraw, ImageFont

from objection_engine.parse_tags import DialoguePage

try:
    from fontTools.ttLib import TTFont
except:
    from fonttools.ttLib import TTFont

class TextType(IntEnum):
    DIALOGUE = 0
    NAME = 1

FONT_ARRAY = [
        # AA-Like > Pixel > Generic
        # AA-like, Latin, hiragana, katakana, (part of) cyrillic
        {'path': './assets/igiari/Igiari.ttf'},
        # AA-like, Latin, hiragana, katakana, (part of) cyrillic
        {'path': './assets/igiari/Galmuri11.ttf'},
        # Pixel, Kanji, Hiragana, Katakana
        {'path':'./assets/igiari/jackeyfont.ttf'},
        # Arabic
        {'path':'./assets/igiari/arabic-1.ttf', 'size': 12, 'offset': {TextType.NAME: (0, -5)}},
        # Pixel-font, Hebrew
        {'path':'./assets/igiari/STANRG__.ttf'},
        # Generic
        {'path':'./assets/igiari/NotoSans-Regular.ttf'},
        # Pixel font, Arabic
        {'path':'./assets/igiari/bitsy-font-with-arabic.ttf', 'size': 10},
    ]

NAMETAG_FONT_ARRAY = [
    {'path': './assets/ace-name/ace-name.ttf', 'size': 8}
] + FONT_ARRAY



class AnimText:
    font_array = FONT_ARRAY
    def __init__(
        self,
        text: DialoguePage,
        *,
        x: int = 0,
        y: int = 0,
        font_path: str = None,
        font_size: int = 12,
        typewriter_effect: bool = False,
        colour: str = "#ffffff",
        text_type: TextType = TextType.DIALOGUE
    ):
        self.x = x
        self.y = y
        self.text = text
        # Used for font handling internals
        self._internal_text = text
        self.typewriter_effect = typewriter_effect

        print("Create AnimText with text:", self.text)
        
        self.text_type = text_type
        if self.text_type == TextType.DIALOGUE:
            self.font_array = FONT_ARRAY
        elif self.text_type == TextType.NAME:
            self.font_array = NAMETAG_FONT_ARRAY

        self.font_size = font_size

        if font_path is None:
            best_font = self._select_best_font()
            self.font_path = best_font['path']
            if 'size' in best_font:
                self.font_size = best_font['size']

            offsets = best_font.get('offset', {}).get(self.text_type, (0,0))
            self.x += offsets[0]
            self.y += offsets[1]

        else:
            self.font_path = font_path

        self.colour = colour
        self.font = ImageFont.truetype(self.font_path, self.font_size)

    def render(self, background: Image, frame: int = 0):
        draw = ImageDraw.Draw(background)
        _text = self.text
        print(_text)
        if self.typewriter_effect:
            if isinstance(_text, str):
                _text = _text[:frame]
            elif isinstance(_text, DialoguePage):
                _text = _text.get_visible_text(frame)

        if isinstance(_text, str):
            if self.font_path is not None:
                draw.text((self.x, self.y), _text, font=self.font, fill=self.colour)
            else:
                draw.text((self.x, self.y), _text, fill=self.colour)

        elif isinstance(_text, DialoguePage):
            ... # TODO: draw each block!!
        return background

    def get_text_size(self):
        return self.font.getsize(self.text)

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
        print(f'WARNING. NO OPTIMAL FONT FOUND, font score: {best_font_points}/{len(self._internal_text.get_raw_text())}, text {self._internal_text}')
        return best_font

    def _check_font(self, font):
        return score_font(font, self.text)

    def __str__(self):
        return self.text

def score_font(font, text):
    '''Scores a font based on a given text string'''
    font_path = font['path']
    font = TTFont(font_path)
    # We check all chars for presence on the font
    valid_char = 0

    text_iterator = None
    if isinstance(text, str):
        text_iterator = text
    elif isinstance(text, DialoguePage):
        text_iterator = text.get_raw_text()

    for char in text_iterator:
        # We check if the char is in any table of the font
        for table in font['cmap'].tables:
            if ord(char) in table.cmap:
                valid_char += 1
                break
    return valid_char

def is_renderable(text):
    '''Determines if a given string is renderable against default fonts'''
    score = 0
    for font in FONT_ARRAY:
        score = max(score, score_font(font, text))
    return score >= len(text)
