from difflib import get_close_matches
from tomllib import load
from os import scandir
from os.path import join

try:
    from rich import print
except:
    pass

ASSETS_FOLDER = "assets_v4"
CHARACTERS_FOLDER = "characters"
MUSIC_FOLDER = "music"

def _sprite_not_found_error(character_name: str, sprite_name: str, files_in_character_dir: list, characters_to_remove: set):
    error_string = f'[yellow][bold]NOTE[/bold] - Character folder "{character_name}" does not have "{sprite_name}"'
    matches = get_close_matches(sprite_name, [f.name for f in files_in_character_dir], cutoff=0.9)
    if len(matches) > 0:
        error_string += f" (is the filename \"{matches[0]}\" misspelled?)"
    
    error_string += '; this character will be removed from the possible characters'
    print(error_string)
    characters_to_remove.add(character_name)

def load_character_data() -> dict:
    # Find all of the characters
    characters = {}
    folders = [f for f in scandir(join(ASSETS_FOLDER, CHARACTERS_FOLDER)) if f.is_dir()]
    for f in folders:
        # Allow us to skip characters by prefixing their name with
        # an underscore
        if f.name.startswith("_"):
            continue
        try:
            with open(join(f.path, "config.toml"), "rb") as config_file:
                characters[f.name] = load(config_file)
        except FileNotFoundError:
            print(f'ERROR - Character folder "{f.name}" has no config.toml')
            continue

    # Validate that all characters have the sprites they should
    characters_to_remove = set()
    for character_name, character_data in characters.items():
        files_in_character_dir = [f for f in scandir(join(ASSETS_FOLDER, CHARACTERS_FOLDER, character_name)) if f.is_file()]
        all_expected_sprites = [sprite for sprite_list in character_data.get("sprites", {}).values() for sprite in sprite_list]
        for sprite in all_expected_sprites:
            sprite_prefix = f"{character_name}-{sprite}"
            idle_sprite = f"{sprite_prefix}-idle.gif"
            talk_sprite = f"{sprite_prefix}-talk.gif"

            idle_sprite_exists = any(f.name == idle_sprite for f in files_in_character_dir)
            talk_sprite_exists = any(f.name == talk_sprite for f in files_in_character_dir)

            if not idle_sprite_exists:
                _sprite_not_found_error(character_name, idle_sprite, files_in_character_dir, characters_to_remove)

            if not talk_sprite_exists:
                _sprite_not_found_error(character_name, talk_sprite, files_in_character_dir, characters_to_remove)

    # Config file in characters folder gives high priority characters
    try:
        with open(join(ASSETS_FOLDER, CHARACTERS_FOLDER, "config.toml"), "rb") as config_file:
            data = load(config_file)
            high_priority_characters = data.get("high_priority", [])
    except FileNotFoundError:
        high_priority_characters = []


    for character in characters_to_remove:
        del characters[character]
        if character in high_priority_characters:
            high_priority_characters.remove(character)

    # Characters being children is specified in their config files
    omit_for_adult_mode = [c for c, data in characters.items() if data.get("is_child", False)]

    return {
        "characters": characters,
        "high_priority": high_priority_characters,
        "omit_for_adult_mode": omit_for_adult_mode,
    }


def load_music_data() -> dict:
    # Find all of the music packs
    music_packs = {}
    folders = [f for f in scandir(join(ASSETS_FOLDER, MUSIC_FOLDER)) if f.is_dir()]
    for f in folders:
        try:
            with open(join(f.path, "config.toml"), "rb") as config_file:
                music_packs[f.name] = load(config_file)
        except FileNotFoundError:
            print(f'ERROR - Music folder "{f.name}" has no config.toml')
            continue

    return music_packs
