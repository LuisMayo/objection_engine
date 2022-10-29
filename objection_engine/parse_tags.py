from curses.ascii import isspace
from dataclasses import dataclass
from re import compile
from typing import Union
from textwrap import wrap
from pprint import pprint
from copy import deepcopy

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
                


@dataclass
class DialogueTextContent:
    cleaned_lines: str
    tags: list[Union[DialogueTag, DialogueAction]]

    def get_text_chunks(self, line_width: int = 50, lines_per_box: int = 3) -> list[DialoguePage]:
        wrapped_lines = wrap(self.cleaned_lines, width=line_width)
        formatted_lines = []
        for line in wrapped_lines:
            start_index = self.cleaned_lines.index(line)
            chars_and_tags = []
            for i, char in enumerate(line):
                this_char_tags = []
                for tag in self.tags:
                    if isinstance(tag, DialogueAction) and i == tag.index + start_index:
                        this_char_tags.append(tag.name)
                            
                    elif isinstance(tag, DialogueTag) and i + start_index in tag.range():
                        this_char_tags.append(tag.name)

                chars_and_tags.append((char, this_char_tags))

            formatted_lines.append(chars_and_tags)


        # We have the big ugly list of characters, now we want to condense it into continuous chunks
        lines_of_chunks = []
        for line in formatted_lines:
            chunks = []
            current_string = ""
            current_tags = None
            for char, tags in line:
                char: str
                tags: list[str]
                if tags == current_tags or current_tags is None:
                    current_string += char
                    if current_tags is None:
                        current_tags = tags.copy()
                else:
                    chunks.append(DialogueTextChunk(current_string, current_tags))
                    current_tags = tags.copy()
                    current_string = char

            if len(current_string) > 0:
                chunks.append(DialogueTextChunk(current_string, current_tags))

            lines_of_chunks.append(chunks)

        lines_grouped_into_threes = [lines_of_chunks[i:i+lines_per_box] for i in range(0, len(lines_of_chunks), lines_per_box)]
        

        pages: list[DialoguePage] = [DialoguePage(group_of_lines) for group_of_lines in lines_grouped_into_threes]
        return pages


# Group 1: Optional slash at the beginning (i.e. it's a closing tag)
# Group 2: Tag name
# Group 3: Arguments to tag
# Group 4: Optional slash at end (i.e. it's self-closing, like an action)
tag_re = compile(r"<(/??)([a-z]*?)(/??)>")

def parse_text(text: str) -> DialogueTextContent:
    tag_stack = []
    final_tags = []
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
        if not is_closing_tag:
            tag_stack.append({
                "name": tag_name,
                "start": start
            })

        # Closing tag, like </red>
        elif is_closing_tag:
            tag = tag_stack.pop()
            if tag["name"] != tag_name:
                raise Exception(f"Closing tag {tag_name} does not correspond to opening tag {tag['name']}")

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

# def add_line_breaks(text: str, tags: list[dict], max_chars: int = 15):
#     lines = []

#     line_start_index = 0
#     line_end_index = 0

#     while line_end_index < len(text) - 1:
#         while line_end_index - line_start_index < max_chars:
#             line_end_index += 1

#         # If we're currently in the middle of a word, then move the line end index back to the previous space
#         # while line_end_index < len(text) and not text[line_end_index].isspace():
#         #     line_end_index -= 1
#         #     print(text[line_start_index:line_end_index])

#         new_line = text[line_start_index:line_end_index]

#         new_line_tags = []

        
#         for tag in tags:
#             name = tag["name"]
#             start = tag["start"]
#             rel_start = start - line_start_index
#             local_start = max(0, rel_start)

#             new_tag = {
#                 "name": name,
#                 "start": local_start
#             }

#             if "end" in tag:
#                 end = tag["end"]
#                 rel_end = rel_start + (end - start)
#                 local_end = min(len(new_line), rel_end)

#                 # If this tag doesn't overlap at all with this line of text, then skip it
#                 if rel_end < 0 or rel_start >= len(new_line):
#                     continue

#                 new_tag["end"] = local_end
#                 new_line_tags.append(new_tag)

#             else:
#                 if rel_start < 0 or rel_start >= len(new_line):
#                     continue

#                 new_line_tags.append(new_tag)

#         # Let's strip whitespace.
#         # First, strip whitespace from the beginning.
#         line_len_before_lstrip = len(new_line)
#         new_line = new_line.lstrip()
#         chars_removed = line_len_before_lstrip - len(new_line)
#         for tag in new_line_tags:
#             tag["start"] = max(0, tag["start"] - chars_removed)
#             if "end" in tag:
#                 tag["end"] = max(0, tag["end"] - chars_removed)

#         # Next, strip whitespace from the end.
#         line_len_before_rstrip = len(new_line)
#         new_line = new_line.rstrip()
#         chars_removed = line_len_before_rstrip - len(new_line)
#         for tag in new_line_tags:
#             if "end" in tag:
#                 tag["end"] = min(tag["end"] - chars_removed, len(new_line))

#         # Go to next line
#         lines.append((new_line, new_line_tags))
#         line_start_index = line_end_index

#     return lines

# def line_to_character_chunks(text: str, tags: list[dict]):
#     return [
#         (c, [
#             item["name"] for item in tags
#             if "end" not in item and item["start"] == i
#             or "end" in item and i in range(item["start"], item["end"])
#             ])
#         for i, c in enumerate(text)
#     ]

# def merge_character_chunks(characters: list[tuple[str, list[dict]]]):
#     current_string = ""
#     current_tags = characters[0][1]
#     chunks = []
#     for c, tags in characters:
#         c: str
#         tags: list[dict]
#         if tags == current_tags:
#             current_string += c
#         else:
#             chunks.append((current_string, current_tags))
#             current_string = ""
#             current_tags = tags.copy()
#             current_string += c

#     chunks.append((current_string, current_tags))
#     return chunks

# def reconstruct_string_for_box(chunks: list[list[tuple[str, list[dict]]]]):
#     output = ""
#     for list_of_line_chunks in chunks:
#         for line_chunk in list_of_line_chunks:
#             output += line_chunk[0]
#         output += " "
#     return output

def get_rich_boxes(text: str, line_width: int = 40, lines_per_box: int = 3):
    """
    Given input `text`, returns a list of `DialoguePage` objects. Each object
    represents a single dialogue box.
    """
    return parse_text(text).get_text_chunks(line_width, lines_per_box)

# test_string = "Hello, my name is <red>Bob</red> and I like to <green>eat avocados</green>. <shake/>Yum!<blue>(Wish I had more...)</blue> Here's some more text because we need this to be really long and go on for more than 3 lines. Wow this still isn't enough text? Time to go on for even longer, I guess. Maybe this is enough? Or should I go a bit farther?"
# get_rich_boxes(test_string, 40, 3)