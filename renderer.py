from typing import List
from beans.comment_bridge import CommentBridge
from beans.comment import Comment
from collections import Counter
from constants import Character
import random
import anim

def render_comment_list(comment_list: List[Comment], output_filename = 'hello.mp4', music_code = 'PWR'):
    counter = Counter()
    thread = []
    for comment in comment_list:
        counter.update({comment.effective_user_id: 1})
    characters = get_characters(counter)
    for comment in comment_list:
        comment.character = characters[comment.effective_user_id]
        thread.append(CommentBridge(comment))
    if (output_filename[-4:] != '.mp4'):
        output_filename += '.mp4'
    return anim.comments_to_scene(thread, name_music = music_code, output_filename=output_filename)


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
    ]
    rnd_characters = []
    if len(most_common) > 0:
        users_to_characters[most_common[0]] = Character.PHOENIX
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
