from typing import List
from beans.comment_bridge import CommentBridge
from beans.comment import Comment
from collections import Counter
import anim

def render_comment_list(comment_list: List[Comment], output_filename = 'hello.mp4', music_code = 'pwr'):
    counter = Counter()
    users_to_names = {} # This will serve to link @ids with usernames
    thread = []
    for comment in comment_list:
        effective_id = comment.user_id or comment.user_name
        users_to_names[effective_id] = comment.user_name
        counter.update({effective_id: 1})
        thread.append(CommentBridge(comment))
    most_common = [users_to_names[t[0]] for t in counter.most_common()]
    characters = anim.get_characters(most_common)
    if (output_filename[-4:] != '.mp4'):
        output_filename += '.mp4'
    return anim.comments_to_scene(thread, characters, name_music = music_code, output_filename=output_filename)


def get_characters(common: Counter):
    
