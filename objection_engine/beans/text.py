from typing import Optional, List
from objection_engine.font_constants import FONT_ARRAY
from objection_engine.font_tools import get_font_score

def is_renderable(text: str, font_array: Optional[List[dict]] = None) -> bool:
    score = 0
    for font in FONT_ARRAY if font_array is None else font_array:
        score = max(score, get_font_score(font, text))
    return score >= len(text)