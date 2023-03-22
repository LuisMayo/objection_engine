from .constants import Character
import random
from collections import Counter
import os
import requests
import zipfile
import shutil
import json
from toml import dump

def ensure_assets_are_available():
    if not os.path.exists('assets') or not os.listdir('assets'):
        download_assets()
        os.remove('assets.zip')
    else:
        # This is in case there are only some missing assets that have been added in updates
        detect_old_assets_format()

def download_assets():
    print('Assets not present. Downloading them')
    response = requests.get('https://dl.luismayo.com/assetsv4.zip')
    with open('assets.zip', 'wb') as file:
        file.write(response.content)
    with zipfile.ZipFile('assets.zip', 'r') as zip_ref:
        zip_ref.extractall('assets')

def detect_old_assets_format():
    if os.path.exists('./assets/igiari'):
        print("Old assets format detected. Moving assets folder to assets_old")
        os.rename("./assets", "./assets_old")
        download_assets()
        print("Migrating music (if any) to the new assets folder with the new assets config")
        for music_folder in os.listdir("./assets_old/music"):
            if not os.path.exists("./assets/music/" + music_folder):
                print("Migrating " + music_folder)
                try:
                    shutil.copytree("./assets_old/music/" + music_folder, "./assets/music/" + music_folder)
                except Exception as e:
                    print("Error while copying" + str(e))
                    continue 
                try:
                    with open("./assets/music/" + music_folder + "/config.json",'rt') as file_json:
                        old_config = json.load(file_json)
                        with open("./assets/music/" + music_folder + "/config.toml",'wt') as file_toml:
                            dump(old_config, file_toml)
                except Exception as e:
                    print("Error trying to convert the music format config file. Removing the folder")
                    try:
                        shutil.rmtree("./assets/music/" + music_folder)
                    except Exception as e2:
                        print("Error while trying to remove the folder. Music may be corrupted")
            else:
                print("Folder " + music_folder + " already existed on destination, omiting migration")



def get_characters(common: Counter, assigned_characters: dict = None, adult_mode: bool = False):
    users_to_characters = {} if assigned_characters is None else assigned_characters.copy()
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

    if not adult_mode:
        all_rnd_characters.append(Character.PEARL)

    # Confirm that all of the assigned characters are valid.
    all_characters = all_rnd_characters + [Character.PHOENIX, Character.EDGEWORTH]
    for character in users_to_characters.values():
        if character not in all_characters:
            raise ValueError(f"\"{character}\" is not a valid character")

    # If Phoenix was not manually assigned and the user with
    # the most comments wasn't manually assigned a character,
    # assign Phoenix to the user with the most comments.
    try:
        if Character.PHOENIX not in users_to_characters.values() and most_common[0] not in users_to_characters:
            users_to_characters[most_common[0]] = Character.PHOENIX
    except IndexError:
        pass

    # Same for Edgeworth, but to the user with the second-most comments.
    try:
        if Character.EDGEWORTH not in users_to_characters.values() and most_common[1] not in users_to_characters:
            users_to_characters[most_common[1]] = Character.EDGEWORTH
    except IndexError:
        pass

    # Finally, from the remaining pool of characters, let's assign them randomly
    # to the remaining user IDs.
    rnd_characters = [c for c in all_rnd_characters if c not in users_to_characters.values()]
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
