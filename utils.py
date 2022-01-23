from constants import Character
import random
from collections import Counter
import os

def get_characters(common: Counter):
    users_to_characters = {}
    most_common =  [t[0] for t in common.most_common()]
    all_rnd_characters = [
        Character.GODOT,
        Character.FRANZISKA,
        Character.JUDGE,
        Character.LARRY,
        Character.MAYA,
        Character.KARMA,
        Character.PAYNE,
        Character.MAGGEY,
        Character.PEARL,
        Character.LOTTA,
        Character.GUMSHOE,
        Character.GROSSBERG,
        Character.APOLLO,
        Character.KLAVIER,
        Character.MIA,
        Character.WILL,
        Character.OLDBAG,
        Character.REDD,
    ]
    rnd_characters = []
    if len(most_common) > 0:
        users_to_characters[most_common[0]] = Character.PHOENIX
        if len(most_common) > 1:
            users_to_characters[most_common[1]] = Character.EDGEWORTH
            for character in most_common[2:]:
                if len(rnd_characters) == 0:
                    rnd_characters = all_rnd_characters.copy()
                rnd_character = random.choice(
                    rnd_characters
                )
                rnd_characters.remove(rnd_character)
                users_to_characters[character] = rnd_character
    return users_to_characters

def get_all_music_available():
    available_music = os.listdir('assets/music')
    return available_music

def is_music_available(music: str):
    music = music.lower()
    available_music = os.listdir('assets/music')
    available_music.append('rnd')
    return music in available_music
