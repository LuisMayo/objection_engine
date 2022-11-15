from dataclasses import dataclass
from re import compile
from typing import Union
from copy import deepcopy
from objection_engine.beans.font_tools import get_best_font, split_str_into_newlines, split_with_joined_sentences
from objection_engine.beans.font_constants import FONT_ARRAY

@dataclass
class DialogueTag:
    name: str
    start: int
    end: int

    def range(self):
        return range(self.start, self.end)

@dataclass
class DialogueAction:
    name: str
    index: int

@dataclass
class DialogueTextChunk:
    text: str
    tags: list[str]

    def __len__(self) -> int:
        return len(self.text)

@dataclass
class DialoguePage:
    lines: list[list[DialogueTextChunk]]

    def __len__(self) -> int:
        lens = []
        for line in self.lines:
            for chunk in line:
                lens.append(len(chunk))
        return sum(lens)

    def get_raw_text(self) -> str:
        texts = []
        for line in self.lines:
            for chunk in line:
                texts.append(chunk.text)
        return ''.join(texts)

    def get_visible_text(self, visible_chars: int = 10) -> 'DialoguePage':
        """
        Iterate through each line, and within each line, its chunks.
        Count the characters and keep adding to a variable.
        Once the variable hits visible_chars, stop counting.
        The chunks we read should be added to a list, and the chunk we're reading right now
        should be cut off to its correct length before being added.
        """
        chars_remaining = visible_chars
        new_lines = []
        for line in self.lines:
            new_line = []
            for chunk in line:
                if chars_remaining >= len(chunk):
                    new_line.append(deepcopy(chunk))
                    chars_remaining -= len(chunk)
                elif chars_remaining > 0:
                    partial_copy = deepcopy(chunk)
                    partial_copy.text = partial_copy.text[:chars_remaining]
                    new_line.append(partial_copy)
                    chars_remaining = 0
                    break
                else:
                    break
            new_lines.append(new_line)
            if chars_remaining <= 0:
                break

        return DialoguePage(new_lines)

    def condense_chunks(self) -> 'DialoguePage':
        lines_of_chunks = []
        for line in self.lines:
            current_string = ""
            current_tags = None
            chunks: list[DialogueTextChunk] = []
            for chunk in line:
                if current_tags is None or chunk.tags == current_tags:
                    current_string += chunk.text
                    if current_tags is None:
                        current_tags = chunk.tags.copy()
                else:
                    chunks.append(DialogueTextChunk(current_string, current_tags))
                    current_string = chunk.text
                    current_tags = chunk.tags.copy()
            if len(current_string) > 0:
                chunks.append(DialogueTextChunk(current_string, current_tags))
            lines_of_chunks.append(chunks)
        return DialoguePage(lines_of_chunks)

    def use_rtl(self):
        best_font = get_best_font(self.get_raw_text(), FONT_ARRAY)
        return best_font.get("rtl", False)

@dataclass
class DialogueTextContent:
    cleaned_lines: str
    tags: list[Union[DialogueTag, DialogueAction]]

    def get_text_chunks(self) -> list[DialoguePage]:
        pages = []
        current_position = 0
        for box_text in split_with_joined_sentences(self.cleaned_lines):
            splitter_font_path = get_best_font(box_text, FONT_ARRAY)['path']
            wrapped_box_lines = split_str_into_newlines(box_text, splitter_font_path, 15).split('\n')
            lines: list[list[DialogueTextChunk]] = []
            for line in wrapped_box_lines:
                chunks: list[DialogueTextChunk] = []
                for char in line:
                    this_char_tags: list[str] = []
                    for tag in self.tags:
                        if isinstance(tag, DialogueTag) and current_position in tag.range():
                            this_char_tags.append(tag.name)
                    chunks.append(DialogueTextChunk(char, this_char_tags))
                    current_position += 1

                lines.append(chunks)

            new_page = DialoguePage(lines).condense_chunks()
            pages.append(new_page)
            
        return pages


# Group 1: Optional slash at the beginning (i.e. it's a closing tag)
# Group 2: Tag name
# Group 3: Arguments to tag
# Group 4: Optional slash at end (i.e. it's self-closing, like an action)
tag_re = compile(r"<(/??)([a-z]*?)(/??)>")

def parse_text(text: str) -> DialogueTextContent:
    tag_stack = []
    final_tags = []
    stripped_text = text.replace('\n', ' ').replace('\r', ' ').replace('\t', ' ')
    
    next_match = tag_re.search(stripped_text)
    while next_match is not None:
        start, end = next_match.span(0)
        stripped_text = stripped_text[:start] + stripped_text[end:]

        closing_slash, tag_name, self_closing_slash = next_match.group(1, 2, 3)
        is_closing_tag = closing_slash == "/"
        is_self_closing_tag = self_closing_slash == "/"

        if is_closing_tag and is_self_closing_tag:
            raise Exception(f"Tag at index {start} is both closing and self-closing")

        # Opening tag, like <red>
        if not is_closing_tag:
            tag_stack.append({
                "name": tag_name,
                "start": start
            })

        # Closing tag, like </red>
        elif is_closing_tag:
            if len(tag_stack) == 0:
                # Closing tag before opening tag
                return DialogueTextContent(text, [])
            tag = tag_stack.pop()
            if tag["name"] != tag_name:
                # Tag mismatch
                return DialogueTextContent(text, [])

            # I know it's confusing, sorry. This is the start index of the closing tag
            tag["end"] = start
            final_tags.append(tag)

        # Self-closing tag, like <shake/>
        if is_self_closing_tag:
            final_tags.append({
                "name": tag_name,
                "index": start
            })
        next_match = tag_re.search(stripped_text)

    # Construct list of tags and actions
    tag_objects = []
    for tag in final_tags:
        if "index" in tag:
            tag_objects.append(DialogueAction(**tag))
        else:
            tag_objects.append(DialogueTag(**tag))

    return DialogueTextContent(stripped_text, tag_objects)

def get_rich_boxes(text: str):
    """
    Given input `text`, returns a list of `DialoguePage` objects. Each object
    represents a single dialogue box.
    """
    return parse_text(text).get_text_chunks()
