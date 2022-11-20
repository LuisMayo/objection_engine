from dataclasses import dataclass, field
from re import compile
from typing import Union
from copy import deepcopy
from .font_tools import get_best_font, split_str_into_newlines, split_with_joined_sentences
from .font_constants import FONT_ARRAY

@dataclass
class DialogueTag:
    name: str = ""
    start: int = 0
    end: int = 0

    def range(self):
        return range(self.start, self.end)

class BaseDialogueItem:
    completed: bool = False

    def __repr__(self) -> str:
        return f"BaseDialogueItem()"

class DialogueAction(BaseDialogueItem):
    name: str = ""
    index: int = 0

    def __init__(self, name: str, index: str):
        self.name = name
        self.index = index

    def __repr__(self) -> str:
        return f"DialogueAction(\'{self.name}\', {self.index})"

class DialogueTextLineBreak(BaseDialogueItem):
    def __repr__(self) -> str:
        return f"DialogueTextLineBreak()"

class DialogueTextChunk(BaseDialogueItem):
    text: str = ""
    tags: list[str] = field(default_factory=list)
    position: int = 0

    def __init__(self, text: str, tags: list[str]):
        self.text = text
        self.tags = tags

    def __len__(self) -> int:
        return len(self.text)

    def __repr__(self) -> str:
        return f"DialogueTextChunk(\'{self.text}\', {self.tags}, {self.position})"

class DialoguePage:
    commands: list[BaseDialogueItem]
    current_item: int

    def __init__(self, commands: list[BaseDialogueItem]):
        self.commands = commands

    def __repr__(self) -> str:
        return f"DialoguePage({self.commands})"

    def get_current_item(self):
        for command in self.commands:
            if not command.completed:
                return command
        return None

    def __len__(self) -> int:
        lens = []
        for command in self.commands:
            if isinstance(command, DialogueTextChunk):
                lens.append(len(command))
        return sum(lens)

    def get_raw_text(self) -> str:
        texts = []
        for command in self.commands:
            if isinstance(command, DialogueTextChunk):
                texts.append(command.text)
        return ''.join(texts)

    def get_visible_text(self, visible_chars: int = 10) -> 'DialoguePage':
        """
        Iterate through each line, and within each line, its chunks.
        Count the characters and keep adding to a variable.
        Once the variable hits visible_chars, stop counting.
        The chunks we read should be added to a list, and the chunk we're reading right now
        should be cut off to its correct length before being added.
        """
        read_everything = True
        chars_remaining = visible_chars
        new_lines = []
        for line in self.commands:
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

        d = DialoguePage(new_lines)
        # print("output from get_visible_text", d)
        return d

    def condense_chunks(self) -> 'DialoguePage':
        chunks = []
        current_string = ""
        current_tags = None
        for chunk in self.commands:
            if isinstance(chunk, DialogueTextChunk) and (current_tags is None or chunk.tags == current_tags):
                current_string += chunk.text
                if current_tags is None:
                    current_tags = chunk.tags.copy()
            elif isinstance(chunk, DialogueTextChunk):
                chunks.append(DialogueTextChunk(current_string, current_tags))
                current_string = chunk.text
                current_tags = chunk.tags.copy()
            elif isinstance(chunk, DialogueAction):
                if len(current_string) > 0:
                    chunks.append(DialogueTextChunk(current_string, current_tags))
                chunks.append(chunk)
                current_string = ""
                current_tags = None
            elif isinstance(chunk, DialogueTextLineBreak):
                if len(current_string) > 0:
                    chunks.append(DialogueTextChunk(current_string, current_tags))
                chunks.append(chunk)
                current_string = ""
                current_tags = None
        if len(current_string) > 0:
            chunks.append(DialogueTextChunk(current_string, current_tags))

        d = DialoguePage(chunks)
        print("condensed chunks:", d)
        return d

@dataclass
class DialogueTextContent:
    cleaned_lines: str
    tags: list[DialogueTag]
    actions: list[DialogueAction]

    def get_text_chunks(self) -> list[DialoguePage]:
        pages = []
        current_position = 0
        for box_text in split_with_joined_sentences(self.cleaned_lines):
            splitter_font_path = get_best_font(box_text, FONT_ARRAY)['path']
            wrapped_box_lines = split_str_into_newlines(box_text, splitter_font_path, 15).split('\n')
            chunks: list[list[DialogueTextChunk]] = []

            for line in wrapped_box_lines:
                for char in line:
                    # print(f"Processing char {char} at position {current_position}")
                    # First, process actions
                    for action in [a for a in self.actions if a.index == current_position]:
                        # print(f"Action {action} takes place at this position, so insert it")
                        chunks.append(action)

                    this_char_tags: list[str] = []
                    for tag in self.tags:
                        if current_position in tag.range():
                            this_char_tags.append(tag.name)
                    chunks.append(DialogueTextChunk(char, this_char_tags))
                    current_position += 1

                chunks.append(DialogueTextLineBreak())
            new_page = DialoguePage(chunks).condense_chunks()
            pages.append(new_page)
            
        return pages


# Group 1: Optional slash at the beginning (i.e. it's a closing tag)
# Group 2: Tag name
# Group 3: Arguments to tag
# Group 4: Optional slash at end (i.e. it's self-closing, like an action)
tag_re = compile(r"<(/?)(.*?)(/??)>")

def parse_text(text: str) -> DialogueTextContent:
    tag_stack = []
    final_tags = []
    final_actions = []
    stripped_text = text
    
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
        if not is_closing_tag and not is_self_closing_tag:
            tag_stack.append({
                "name": tag_name,
                "start": start
            })

        # Closing tag, like </red>
        elif is_closing_tag:
            if len(tag_stack) == 0:
                # Closing tag before opening tag
                print(f"Error - tag stack is empty on closing tag {tag_name}")
                return DialogueTextContent(text, [])
            tag = tag_stack.pop()
            if tag["name"] != tag_name:
                # Tag mismatch
                print(f"Error - tag mismatch (opening tag {tag['name']}, closing tag {tag_name})")
                return DialogueTextContent(text, [])

            # I know it's confusing, sorry. This is the start index of the closing tag
            tag["end"] = start
            final_tags.append(tag)

        # Self-closing tag, like <shake/>
        elif is_self_closing_tag:
            final_actions.append({
                "name": tag_name,
                "index": start
            })
        next_match = tag_re.search(stripped_text)

    # Construct list of tags and actions
    tag_objects = []
    for tag in final_tags:
        tag_objects.append(DialogueTag(**tag))

    action_objects = []
    for action in final_actions:
        action_objects.append(DialogueAction(**action))

    return DialogueTextContent(stripped_text, tag_objects, action_objects)

def get_rich_boxes(text: str):
    """
    Given input `text`, returns a list of `DialoguePage` objects. Each object
    represents a single dialogue box.
    """
    return parse_text(text).get_text_chunks()
