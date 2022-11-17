import random
from typing import List
from .utils import get_characters
from .beans.comment_bridge import CommentBridge
from .beans.comment import Comment
from collections import Counter
from . import anim
import os
from .utils import ensure_assets_are_available
import requests


def render_comment_list(comment_list: List[Comment], output_filename: str = 'hello.mp4', music_code: str = 'PWR', resolution_scale: int = 1, assigned_characters: dict = None, adult_mode = False):
    """
    Given a list of Comments, writes a resulting video to disk at the
    location specified by `output_filename`.

    :param List[Comment] comment_list: A list of Comment objects,
    each one representing a screen in the final video
    :param str output_filename: The location that the final video
    will be rendered to
    :param str music_code: A string code representing which game's
    music should be used
    - "PWR" uses music from "Phoenix Wright: Ace Attorney"
    - "JFA" uses music from "Justice for All"
    - "TAT" uses music from "Trials and Tribulations"
    - "RND" chooses a random game
    :param int resolution_scale: How much to scale the outputted video by
    :param list[dict] assigned_characters: A dictionary with string user ID keys \
        and Character values that manually assign a given user to be portrayed \
        by a specific character. Any users who do not have a character \
        assigned to them via this dictionary will have one assigned at random.
    :param bool adult_mode: The video may contain adult themes and the engine should
    take this into consideration. Example: When "True" Pearl won't appear on videos since she's a kid
    """
    ensure_assets_are_available()
    try:
        collect_stats()
    except:
        pass
    music_code = process_music_code(music_code)

    # Count how many comments each user in the comment_list has.
    # The user with the most comments will be Phoenix, and the
    # user with the second-most comments will be Edgeworth.
    counter = Counter()
    for comment in comment_list:
        counter.update({comment.effective_user_id: 1})
    characters = get_characters(counter, assigned_characters=assigned_characters, adult_mode=adult_mode)

    # Construct the information about the sequence of "shots" in
    # the finished video (e.g. the text spoken and which character
    # is speaking it).
    thread = []
    for comment in comment_list:
        comment.character = characters[comment.effective_user_id]
        thread.append(CommentBridge(comment))

    # Ensure that the output filename has an mp4 file extension.
    if (output_filename[-4:] != '.mp4'):
        output_filename += '.mp4'

    # Finally, render the video.
    return anim.comments_to_scene(thread, name_music = music_code, output_filename=output_filename, resolution_scale=resolution_scale)

def process_music_code(music_code: str) -> str:
    """
    Ensures that the requested music code is valid.

    Valid music codes are the names of folders in 'assets/music'.
    Currently, there are three:
    
    - "pwr" (Phoenix Wright: Ace Attorney)
    - "jfa" (Phoenix Wright: Ace Attorney ~ Justice for All)
    - "tat" (Phoenix Wright: Ace Attorney ~ Trials and Tribulations)
    - "rnd" (Choose a random game)

    If one of these strings (case insensitive) is entered, music
    from that game will be used. A string that does not correspond
    to a folder in 'assets/music' will result in the first available
    choice being used instead.

    :param str music_code: A requested music code to use
    :return: A valid music code, either matching the requested one, or a default
    """
    music_code = music_code.lower()
    available_music = os.listdir('assets/music')
    if (music_code == 'rnd'):
        music_code = random.choice(available_music)
    elif (music_code not in available_music):
        music_code = available_music[0]
    return music_code

def collect_stats():
    if len(os.getenv('oe_stats_server', '')) > 0:
        directory_path = os.getcwd()
        folder_name = os.path.basename(directory_path)
        requests.post(os.getenv('oe_stats_server', '') + '/' + folder_name)
