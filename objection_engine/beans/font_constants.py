from enum import IntEnum

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
        # Better Arabic
        {'path':'./assets/igiari/KawkabMono-Regular.ttf', 'size': 8, 'offset': {TextType.NAME: (0, -2)}, 'rtl': True},
        # Arabic
        {'path':'./assets/igiari/arabic-1.ttf', 'size': 12, 'offset': {TextType.NAME: (0, -5)}, 'rtl': True},
        # Pixel-font, Hebrew
        {'path':'./assets/igiari/STANRG__.ttf'},
        # Generic
        {'path':'./assets/igiari/NotoSans-Regular.ttf'},
        # Pixel font, Arabic
        {'path':'./assets/igiari/bitsy-font-with-arabic.ttf', 'size': 10, 'rtl': True},
    ]

NAMETAG_FONT_ARRAY = [
    {'path': './assets/ace-name/ace-name.ttf', 'size': 8}
] + FONT_ARRAY

TEXT_COLORS = {
    "red": (240, 112, 56),
    "blue": (104, 192, 240),
    "green": (0, 240, 0)
}

MAX_LINE_WIDTH = 220