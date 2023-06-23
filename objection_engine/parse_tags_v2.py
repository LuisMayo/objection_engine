from objection_engine.ace_attorney_scene import MAX_WIDTH
from objection_engine.font_constants import FONT_ARRAY
from objection_engine.font_tools import get_best_font, get_text_width
from objection_engine.parse_tags import BaseDialogueItem, DialogueAction, DialoguePage, DialogueTextChunk, DialogueTextLineBreak
from re import compile

__tag_matcher = compile(r"\[(.*?)\]")
def parse_line(text: str) -> DialoguePage:
    current_line_width = 0.0

    page_content: list[BaseDialogueItem] = []

    remaining_text = text
    while len(remaining_text) > 0:
        re_match = __tag_matcher.match(remaining_text)
        if re_match is not None:
            # Tag found at beginning of string, let's get it
            match_content = re_match.group(1)

            if match_content == "br":
                page_content.append(DialogueTextLineBreak())
            else:
                page_content.append(DialogueAction(match_content, 0))
            remaining_text = remaining_text[len(re_match.group(0)):]
        else:
            char = remaining_text[0]
            page_content.append(DialogueTextChunk(char, []))

            char_width = get_text_width(char, font=get_best_font(char, FONT_ARRAY))

            # Uncomment for auto line breaking (but its stinky)
            # current_line_width += char_width
            # if current_line_width > MAX_WIDTH:
            #     page_content.append(DialogueTextLineBreak())
            #     current_line_width = 0.0
                
            remaining_text = remaining_text[1:]

    return page_content
            