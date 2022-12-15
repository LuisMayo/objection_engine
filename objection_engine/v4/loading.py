from tomllib import load
from os import scandir
from os.path import join

try:
    from rich import print
except:
    pass


def load_character_data() -> dict:
    # Find all of the characters
    characters = {}
    folders = [f for f in scandir("assets_v4/character_sprites") if f.is_dir()]
    for f in folders:
        try:
            with open(join(f.path, "config.toml"), "rb") as config_file:
                characters[f.name] = load(config_file)
        except FileNotFoundError:
            print(f'ERROR - Character folder "{f.name}" has no config.toml')
            continue

    # Config file in character_sprites gives high priority characters
    # and child characters (to exclude if adult mode is on)
    try:
        with open("assets_v4/character_sprites/config.toml", "rb") as config_file:
            data = load(config_file)
            high_priority_characters = data.get("high_priority", [])
            omit_for_adult_mode = data.get("omit_for_adult_mode", [])
    except FileNotFoundError:
        high_priority_characters = []
        omit_for_adult_mode = []

    for character in omit_for_adult_mode:
        del characters[character]

    return {
        "characters": characters,
        "high_priority": high_priority_characters,
        "omit_for_adult_mode": omit_for_adult_mode,
    }


def load_music_data() -> dict:
    # Find all of the music packs
    music_packs = {}
    folders = [f for f in scandir("assets_v4/music") if f.is_dir()]
    for f in folders:
        try:
            with open(join(f.path, "config.toml"), "rb") as config_file:
                music_packs[f.name] = load(config_file)
        except FileNotFoundError:
            print(f'ERROR - Music folder "{f.name}" has no config.toml')
            continue

    return music_packs
