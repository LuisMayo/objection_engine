from collections import Counter
from tomllib import load
from os import walk, scandir
from os.path import join
from random import choice
from objection_engine.v4.ace_attorney_scene import (
    AceAttorneyDirector,
    get_boxes_with_pauses,
)

from objection_engine.v4.parse_tags import DialogueAction, DialoguePage
from ..beans.comment import Comment

try:
    from rich import print
except:
    pass


def load_character_data():
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


def load_music_data():
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


def get_characters(
    common: Counter, assigned_characters: dict = None, adult_mode: bool = False
):
    users_to_characters = (
        {} if assigned_characters is None else assigned_characters.copy()
    )
    most_common = [t[0] for t in common.most_common()]

    # Get characters
    character_data = load_character_data()

    high_priority_character_names = character_data["high_priority"]
    character_names = [
        name
        for name in character_data["characters"]
        if not adult_mode
        or (adult_mode and name not in character_data["omit_for_adult_mode"])
    ]
    rnd_character_names = [
        name for name in character_names if name not in high_priority_character_names
    ]

    # Assign high priority characters first
    i: int = 0
    for name in high_priority_character_names:
        try:
            if (
                name not in users_to_characters.values()
                and most_common[i] not in users_to_characters
            ):
                users_to_characters[most_common[i]] = name
        except IndexError:
            pass
        i += 1

    # Everyone else is chosen at random
    rnd_characters = [
        c for c in rnd_character_names if c not in users_to_characters.values()
    ]
    for user_id in most_common:
        # Skip users who were manually assigned characters
        if user_id in users_to_characters:
            continue

        # Reload choosable characters if we ran out
        if len(rnd_characters) == 0:
            rnd_characters = rnd_character_names.copy()

        # Assign a character randomly chosen from the list to this user,
        # and remove them from the pool
        rnd_character = choice(rnd_characters)
        rnd_characters.remove(rnd_character)
        users_to_characters[user_id] = rnd_character

    return users_to_characters


def render_comment_list(
    comment_list: list["Comment"],
    output_filename: str = "hello.mp4",
    music_code: str = "pwr",
    resolution_scale: int = 1,
    assigned_characters: dict = None,
    adult_mode: bool = False,
):
    counter = Counter()
    for comment in comment_list:
        counter.update({comment.effective_user_id: 1})

    characters = get_characters(
        counter, assigned_characters=assigned_characters, adult_mode=adult_mode
    )

    # Get music
    all_music_data = load_music_data()
    if music_code in all_music_data:
        music_pack = all_music_data[music_code]
    else:
        raise KeyError(
            f'Music code "{music_code}" not found. Ensure that a folder for it exists in the "music" folder, and that it has a "config.toml" file.'
        )
    print("Chose music pack:", music_code, music_pack)

    pages: list[DialoguePage] = []

    # Start the relaxed music
    relaxed_track = choice(music_pack["relaxed"])
    pages.append(DialoguePage([DialogueAction(f"music start {join(music_code, relaxed_track)}", 0)]))

    # Add all of the comments
    for comment in comment_list:
        pages.extend(
            get_boxes_with_pauses(
                user_name=comment.user_name,
                character=characters[comment.effective_user_id],
                text=comment.text_content,
            )
        )

    director = AceAttorneyDirector()
    director.set_current_pages(pages)
    director.render_movie(-15)
