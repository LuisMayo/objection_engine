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
            print(f"Current line: \"{text[line_start_index:line_end_index]}\"")

        # If we're currently in the middle of a word, then move the line end index back to the previous space
        while line_end_index < len(text) and not text[line_end_index].isspace():
            line_end_index -= 1

        new_line = text[line_start_index:line_end_index]
        new_line_length = len(new_line)
        
        # TODO: Strip whitespace from start and end
        # TODO: Adjust tag indices to match:
        # Difference in starting whitespace should be subtracted from all indices within this block and after?
        # Difference in ending whitespace should be subtracted from all indices after this block?
        # Not sure

        
        # Go to next line
        lines.append(text[line_start_index:line_end_index])
        line_start_index = line_end_index
    
    print(lines)

test_string = "Hello, my name is <red>Bob</red> and I like to <green>eat avocados</green>. <shake/>Yum! <blue>(Wish I had more...)</blue>"
text, tags = parse_text(test_string)
add_line_breaks(text, tags, 20)