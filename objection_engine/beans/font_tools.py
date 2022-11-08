from objection_engine.beans.font_constants import FONT_ARRAY
from PIL import ImageFont
from typing import List, Dict, Union
from textwrap import wrap
import spacy

nlp = spacy.blank("xx")
nlp.add_pipe('sentencizer')

try:
    from fontTools.ttLib import TTFont
except:
    from fonttools.ttLib import TTFont

def get_text_width(text, font_size = 15, font = None):
    if font is None:
        font = get_best_font(text, FONT_ARRAY)
    font_path = font['path']
    font_obj = ImageFont.truetype(font_path, font_size)
    return font_obj.getlength(text)

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
    text = text.replace('\n', '').replace('\r', '').replace('\t', '')
    for font in font_array:
        pts = get_font_score(font, text)
        if pts > best_font_points:
            best_font_points = pts
            best_font = font
        if best_font_points >= len(text):
            return font
    print(f'WARNING. NO OPTIMAL FONT FOUND, font: {best_font}, font score: {best_font_points}/{len(text)}, text \"{text}\"\n')
    return best_font


def fit_words_within_width(words: Union[list[str], str], font: ImageFont.FreeTypeFont, insert_space: bool):
    new_text = ""
    space = " " if insert_space else ""
    for word in words:
        last_sentence = new_text.split("\n")[-1] + word + space
        if font.getlength(text=last_sentence) >= 240:
            if new_text.split("\n")[-1] != "":
                new_text += "\n"
            new_text += fit_words_within_width(word, font, False) + space
        else:
            new_text += word + space

    return new_text

def split_str_into_newlines(text: str, font_path, font_size):
    font = ImageFont.truetype(font_path, font_size)
    words = text.split(" ")
    return fit_words_within_width(words, font, True)


def split_with_joined_sentences(text: str):
    """
    """
    tokens = nlp(text)
    sentences = [sent.text.strip() for sent in tokens.sents]
    joined_sentences = []
    i = 0
    while i < len(sentences):
        sentence = sentences[i]
        if len(sentence) > 85: # Long sentences should be wrapped to multiple shorter lines
            text_chunks = [chunk for chunk in wrap(sentence, 85)]
            joined_sentences = [*joined_sentences, *text_chunks]
            i += 1
        else:
            if i + 1 < len(sentences) and len(f"{sentence} {sentences[i+1]}") <= 85: # Maybe we can join two different sentences
                joined_sentences.append(sentence + " " + sentences[i+1])
                i += 2
            else:
                joined_sentences.append(sentence)
                i += 1

    return joined_sentences