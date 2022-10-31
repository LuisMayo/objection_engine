from objection_engine.beans.font_constants import FONT_ARRAY


try:
    from fontTools.ttLib import TTFont
except:
    from fonttools.ttLib import TTFont

def get_font_score(font, text):
    font_path = font['path']
    font = TTFont(font_path)

    # We check all chars for presence on the font
    valid_chars = 0
    for char in text:
        # We check if the char is in any table of the font
        for table in font['cmap'].tables:
            if ord(char) in table.cmap:
                valid_chars += 1
                break
    return valid_chars

def get_best_font(text, font_array):
    best_font = font_array[-1]
    best_font_points = 0
    for font in font_array:
        pts = get_font_score(font, text)
        if pts > best_font_points:
            best_font_points = pts
            best_font = font
        if best_font_points >= len(text):
            return font
    print(f'WARNING. NO OPTIMAL FONT FOUND, font score: {best_font_points}/{len(text)}, text {text}')
    return best_font