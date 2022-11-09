from enum import IntEnum
from typing import Dict
from PIL import Image, ImageDraw, ImageFont
from objection_engine.beans.font_tools import get_best_font, get_font_score

from objection_engine.parse_tags import DialoguePage
from objection_engine.beans.font_constants import FONT_ARRAY, NAMETAG_FONT_ARRAY, TEXT_COLORS, TextType

try:
    from fontTools.ttLib import TTFont
except:
    from fonttools.ttLib import TTFont

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
        force_no_rtl: bool = False,
        colour: str = "#ffffff",
        text_type: TextType = TextType.DIALOGUE
    ):
        self.x = x
        self.y = y
        self.text = text
        # Used for font handling internals
        self._internal_text = text
        self.typewriter_effect = typewriter_effect
        
        self.text_type = text_type
        if self.text_type == TextType.DIALOGUE:
            self.font_array = FONT_ARRAY
        elif self.text_type == TextType.NAME:
            self.font_array = NAMETAG_FONT_ARRAY

        self.font_size = font_size
        self.use_rtl = False

        if font_path is None:
            best_font = self._select_best_font()
            self.font_path = best_font['path']
            if 'size' in best_font:
                self.font_size = best_font['size']

            self.use_rtl = best_font.get("rtl", False) and not force_no_rtl

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
            for line_no, line in enumerate(_text.lines):
                if self.use_rtl:
                    x_offset = 256 - 11 - 11
                else:
                    x_offset = 0
                for chunk_no, chunk in enumerate(line):
                    drawing_args = {
                        "xy": (self.x + x_offset, self.y + (self.font_size + 3) * line_no),
                        "text": chunk.text,
                        "fill": (255,0,255),
                        "anchor": ("r" if self.use_rtl else "l") + "a"
                    }

                    if len(chunk.tags) == 0:
                        drawing_args["fill"] = (255,255,255)
                    else:
                        drawing_args["fill"] = TEXT_COLORS.get(chunk.tags[-1], (255,255,255))

                    if self.font_path is not None:
                        drawing_args["font"] = self.font

                    draw.text(**drawing_args)

                    try:
                        add_to_x_offset = draw.textlength(chunk.text, font=self.font)
                        if chunk_no < len(line) - 1:
                            next_char = line[chunk_no + 1].text[0]
                            add_to_x_offset = draw.textlength(chunk.text + next_char, self.font) - draw.textlength(next_char, self.font)
                    except UnicodeEncodeError:
                        print(f"Couldn't use textlength() to determine length of \"{chunk.text}\", so using getsize() instead")
                        add_to_x_offset = self.font.getsize(chunk.text)[0]
                    
                    if self.use_rtl:
                        x_offset -= add_to_x_offset
                    else:
                        x_offset += add_to_x_offset
                        
        return background

    def get_text_size(self):
        return self.font.getsize(self.text)

    def _select_best_font(self):
        if isinstance(self._internal_text, str):
            return get_best_font(self._internal_text, self.font_array)
        elif isinstance(self._internal_text, DialoguePage):
            return get_best_font(self._internal_text.get_raw_text(), self.font_array)

    def _check_font(self, font):
        return score_font(font, self.text)

    def __str__(self):
        return self.text

def score_font(font, text):
    '''Scores a font based on a given text string'''
    if isinstance(text, DialoguePage):
        text = text.get_raw_text()
    return get_font_score(font, text)

def is_renderable(text):
    '''Determines if a given string is renderable against default fonts'''
    score = 0
    for font in FONT_ARRAY:
        score = max(score, score_font(font, text))
    return score >= len(text)
