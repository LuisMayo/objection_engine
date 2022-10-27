from curses.ascii import isspace
from re import compile

# Group 1: Optional slash at the beginning (i.e. it's a closing tag)
# Group 2: Tag name
# Group 3: Arguments to tag
# Group 4: Optional slash at end (i.e. it's self-closing, like an action)
tag_re = compile(r"<(/??)([a-z]*?)(/??)>")

def parse_text(text: str):
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
                "start": start
            })
        next_match = tag_re.search(stripped_text)

    return (stripped_text, final_tags)

def add_line_breaks(text: str, tags: list[dict], max_chars: int = 15):
    lines = []

    line_start_index = 0
    line_end_index = 0

    while line_end_index < len(text) - 1:
        while line_end_index - line_start_index < max_chars:
            line_end_index += 1

        # If we're currently in the middle of a word, then move the line end index back to the previous space
        # while line_end_index < len(text) and not text[line_end_index].isspace():
        #     line_end_index -= 1
        #     print(text[line_start_index:line_end_index])

        new_line = text[line_start_index:line_end_index]

        new_line_tags = []

        
        for tag in tags:
            name = tag["name"]
            start = tag["start"]
            rel_start = start - line_start_index
            local_start = max(0, rel_start)

            new_tag = {
                "name": name,
                "start": local_start
            }

            if "end" in tag:
                end = tag["end"]
                rel_end = rel_start + (end - start)
                local_end = min(len(new_line), rel_end)

                # If this tag doesn't overlap at all with this line of text, then skip it
                if rel_end < 0 or rel_start >= len(new_line):
                    continue

                new_tag["end"] = local_end
                new_line_tags.append(new_tag)

            else:
                if rel_start < 0 or rel_start >= len(new_line):
                    continue

                new_line_tags.append(new_tag)

        # Let's strip whitespace.
        # First, strip whitespace from the beginning.
        line_len_before_lstrip = len(new_line)
        new_line = new_line.lstrip()
        chars_removed = line_len_before_lstrip - len(new_line)
        for tag in new_line_tags:
            tag["start"] = max(0, tag["start"] - chars_removed)
            if "end" in tag:
                tag["end"] = max(0, tag["end"] - chars_removed)

        # Next, strip whitespace from the end.
        line_len_before_rstrip = len(new_line)
        new_line = new_line.rstrip()
        chars_removed = line_len_before_rstrip - len(new_line)
        for tag in new_line_tags:
            if "end" in tag:
                tag["end"] = min(tag["end"] - chars_removed, len(new_line))

        # Go to next line
        lines.append((new_line, new_line_tags))
        line_start_index = line_end_index

    return lines

def line_to_character_chunks(text: str, tags: list[dict]):
    return [
        (c, [
            item["name"] for item in tags
            if "end" not in item and item["start"] == i
            or "end" in item and i in range(item["start"], item["end"])
            ])
        for i, c in enumerate(text)
    ]

def merge_character_chunks(characters: list[tuple[str, list[dict]]]):
    current_string = ""
    current_tags = characters[0][1]
    chunks = []
    for c, tags in characters:
        c: str
        tags: list[dict]
        if tags == current_tags:
            current_string += c
        else:
            chunks.append((current_string, current_tags))
            current_string = ""
            current_tags = tags.copy()
            current_string += c

    chunks.append((current_string, current_tags))
    return chunks


def show_max_chars(chunks: list[list[tuple[str, list[dict]]]], chars: int):
    """
    TODO: Given the chunks array, remove text/chunks outside of the max char count!
    """
    ...

def group_into_lines(chunks: list[tuple[str, list[dict]]], lines: int = 3):
    return [chunks[i:i+lines] for i in range(0, len(chunks), lines)]

def reconstruct_string_for_box(chunks: list[list[tuple[str, list[dict]]]]):
    output = ""
    for list_of_line_chunks in chunks:
        for line_chunk in list_of_line_chunks:
            output += line_chunk[0]
        output += " "
    return output

# test_string = "Hello, my name is <red>Bob</red> and I like to <green>eat avocados</green>. <shake/>Yum! <blue>(Wish I had more...)</blue> Here's some more text because we need this to be really long and go on for more than 3 lines."

def get_rich_boxes(text: str, line_length: int, num_lines = 3):
    parsed_text, tags = parse_text(text)
    lines = add_line_breaks(parsed_text, tags, line_length)
    character_chunk_lines = [line_to_character_chunks(*i) for i in lines]
    continuous_chunks = [merge_character_chunks(line) for line in character_chunk_lines]
    grouped_in_threes = group_into_lines(continuous_chunks, num_lines)
    return grouped_in_threes

# print(get_rich_boxes(test_string, 40, 3))