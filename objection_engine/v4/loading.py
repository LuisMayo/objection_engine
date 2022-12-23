from difflib import get_close_matches
from toml import load
from os import DirEntry, scandir
from os.path import join
from PIL import Image, ImageFile

ImageFile.LOAD_TRUNCATED_IMAGES = True

from rich import print
from rich.traceback import install

install(show_locals=False)

ASSETS_FOLDER = "assets_v4"
CHARACTERS_FOLDER = "characters"
MUSIC_FOLDER = "music"


def _sprite_not_found_error(
    character_name: str,
    sprite_name: str,
    files_in_character_dir: list,
):
    error_string = f'[yellow][bold]NOTE[/bold] - Character "{character_name}" does not have "{sprite_name}"'
    matches = get_close_matches(
        sprite_name, [f.name for f in files_in_character_dir], cutoff=0.9
    )
    if len(matches) > 0:
        error_string += f' (is the filename "{matches[0]}" misspelled?)'

    error_string += "; this character will be removed from the possible characters"
    print(error_string)


def _sprite_corrupt_error(sprite_name: str):
    print(
        f'[yellow][bold]NOTE[/bold] - Sprite "{sprite_name}" cannot be opened; this character will be removed from the possible characters'
    )

def _no_sprites_error(character_name: str):
    print(
        f'[yellow][bold]NOTE[/bold] - Character "{character_name}" has no sprites; they will be removed from the possible characters'
    )

def _sprite_is_usable(sprite_file: DirEntry) -> bool:
    """
    Confirm that all of the frames in the sprite are usable
    """
    try:
        with Image.open(sprite_file.path) as img:
            if hasattr(img, "is_animated"):
                for frame_no in range(img.n_frames):
                    img.seek(frame_no)
                    img.convert("RGBA")
            else:
                img.convert("RGBA")
        return True
    except Exception:
        return False


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
            with open(join(f.path, "config.toml")) as config_file:
                characters[f.name] = load(config_file)
        except FileNotFoundError:
            print(f'ERROR - Character folder "{f.name}" has no config.toml')
            continue

    # Validate that all characters have the sprites they should
    characters_to_remove = set()
    for character_name, character_data in characters.items():
        files_in_character_dir = [
            f
            for f in scandir(join(ASSETS_FOLDER, CHARACTERS_FOLDER, character_name))
            if f.is_file()
        ]

        # First - let's confirm that all of the sprites are here.
        raw_sprites: dict = character_data.get("sprites", {})

        neutral_sprites = raw_sprites.get("neutral", [])
        positive_sprites = raw_sprites.get("positive", [])
        negative_sprites = raw_sprites.get("negative", [])
        spoiler_sprites = raw_sprites.get("spoiler", [])

        all_expected_sprites = []
        all_expected_sprites.extend(s for s in neutral_sprites)
        all_expected_sprites.extend(s for s in positive_sprites)
        all_expected_sprites.extend(s for s in negative_sprites)

        # If there are no sprites, then don't use this character
        if len(all_expected_sprites) == 0:
            _no_sprites_error(character_name)
            continue

        sprites_to_remove = set()
        for sprite in all_expected_sprites:
            sprite_prefix = f"{character_name}-{sprite}"
            idle_sprite_filename = f"{sprite_prefix}-idle.gif"
            talk_sprite_filename = f"{sprite_prefix}-talk.gif"

            idle_sprite = next(
                (f for f in files_in_character_dir if f.name == idle_sprite_filename),
                None,
            )
            talk_sprite = next(
                (f for f in files_in_character_dir if f.name == talk_sprite_filename),
                None,
            )

            if idle_sprite is None:
                _sprite_not_found_error(
                    character_name,
                    idle_sprite_filename,
                    files_in_character_dir,
                )
                sprites_to_remove.add(character_name)

            elif not _sprite_is_usable(idle_sprite):
                _sprite_corrupt_error(
                    character_name,
                    idle_sprite_filename,
                )
                sprites_to_remove.add(character_name)

            if talk_sprite is None:
                _sprite_not_found_error(
                    character_name,
                    talk_sprite_filename,
                    files_in_character_dir,
                )
                sprites_to_remove.add(character_name)

            elif not _sprite_is_usable(talk_sprite):
                _sprite_corrupt_error(
                    character_name,
                    talk_sprite_filename,
                )
                sprites_to_remove.add(character_name)

        # Remove bad sprites from all lists
        for sprite_to_remove in sprites_to_remove:
            while sprite_to_remove in neutral_sprites:
                neutral_sprites.remove(sprite_to_remove)
            while sprite_to_remove in positive_sprites:
                positive_sprites.remove(sprite_to_remove)
            while sprite_to_remove in negative_sprites:
                negative_sprites.remove(sprite_to_remove)
            while sprite_to_remove in spoiler_sprites:
                spoiler_sprites.remove(sprite_to_remove)

        # If the positive or negative lists are now empty, give them
        # the neutral sprites (and vice versa)
        if len(neutral_sprites) == 0:
            neutral_sprites.extend(positive_sprites)
            neutral_sprites.extend(negative_sprites)
        if len(positive_sprites) == 0:
            positive_sprites.extend(neutral_sprites)
        if len(negative_sprites) == 0:
            negative_sprites.extend(neutral_sprites)
        

    # Config file in characters folder gives high priority characters
    try:
        with open(join(ASSETS_FOLDER, CHARACTERS_FOLDER, "config.toml")) as config_file:
            data = load(config_file)
            high_priority_characters = data.get("high_priority", [])
    except FileNotFoundError:
        high_priority_characters = []

    for character in characters_to_remove:
        del characters[character]
        if character in high_priority_characters:
            high_priority_characters.remove(character)

    # Characters being children is specified in their config files
    omit_for_adult_mode = [
        c for c, data in characters.items() if data.get("is_child", False)
    ]

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
            with open(join(f.path, "config.toml")) as config_file:
                music_packs[f.name] = load(config_file)
        except FileNotFoundError:
            print(f'ERROR - Music folder "{f.name}" has no config.toml')
            continue

    return music_packs
