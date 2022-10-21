from .constants import Character
import random
from collections import Counter
import os
import requests
import zipfile


def ensure_assets_are_available():
    if not os.path.exists('assets') or not os.listdir('assets'):
        print('Assets not present. Downloading them')
        response = requests.get('https://dl.luismayo.com/assets.zip')
        with open('assets.zip', 'wb') as file:
            file.write(response.content)
        with zipfile.ZipFile('assets.zip', 'r') as zip_ref:
            zip_ref.extractall('assets')
        os.remove('assets.zip')

def get_characters(common: Counter, assigned_characters: dict = None):
    if assigned_characters is None:
        assigned_characters = {}
    else:
        assigned_characters = assigned_characters.copy()

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

    # If Phoenix was manually assigned, then assign him to his user.
    # Otherwise, assign him to the user with the most comments.
    if Character.PHOENIX in assigned_characters:
        users_to_characters[assigned_characters[Character.PHOENIX]] = Character.PHOENIX
        del assigned_characters[Character.PHOENIX]
    else:
        try:
            users_to_characters[most_common[0]] = Character.PHOENIX
        except IndexError:
            pass

    # Same for Edgeworth, but in the case of no manual assignment,
    # assign him to the user with the second-most comments.
    if Character.EDGEWORTH in assigned_characters:
        users_to_characters[assigned_characters[Character.EDGEWORTH]] = Character.EDGEWORTH
        del assigned_characters[Character.EDGEWORTH]
    else:
        try:
            users_to_characters[most_common[1]] = Character.EDGEWORTH
        except IndexError:
            pass

    # Before we start randomly assigning characters, let's match up all of the
    # manually assigned characters to their user IDs.
    for character, user_id in assigned_characters.items():
        users_to_characters[user_id] = character
        all_rnd_characters.remove(character)

    # Finally, from the remaining pool of characters, let's assign them randomly
    # to the remaining user IDs.
    rnd_characters = []
    for user_id in most_common:
        # Skip users who were manually assigned characters.
        if user_id in users_to_characters:
            continue

        # Reload the choosable characters, if we ran out.
        if len(rnd_characters) == 0:
            rnd_characters = all_rnd_characters.copy()

        # Assign a character randomly chosen from the list to this user,
        # and remove them from the pool.
        rnd_character = random.choice(rnd_characters)
        rnd_characters.remove(rnd_character)
        users_to_characters[user_id] = rnd_character

    return users_to_characters

def get_all_music_available():
    ensure_assets_are_available()
    available_music = os.listdir('assets/music')
    available_music.append('rnd')
    return available_music

def is_music_available(music: str) -> bool:
    music = music.lower()
    ensure_assets_are_available()
    available_music = os.listdir('assets/music')
    available_music.append('rnd')
    return music in available_music
