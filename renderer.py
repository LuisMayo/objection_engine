from typing import List
from utils import get_characters
from beans.comment_bridge import CommentBridge
from beans.comment import Comment
from collections import Counter
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
