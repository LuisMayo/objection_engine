from typing import List
from beans.comment_bridge import CommentBridge
from beans.comment import Comment
from collections import Counter
import anim

def render_comment_list(comment_list: List[Comment], output_filename: str, music_code: str):
    counter = Counter()
    users_to_names = {} # This will serve to link @ids with usernames
    for comment in comment_list:
        users_to_names[comment.user_id] = comment.user_name
        counter.update({comment.user_id: 1})
    most_common = [users_to_names[t[0]] for t in counter.most_common()]
    characters = anim.get_characters(most_common)
    if (output_filename[-4:] is not '.mp4'):
        output_filename += '.mp4'
    return anim.comments_to_scene(thread, characters, name_music = music_code, output_filename=output_filename)