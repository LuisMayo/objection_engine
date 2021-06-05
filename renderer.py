from typing import List
from utils import get_characters
from beans.comment_bridge import CommentBridge
from beans.comment import Comment
from collections import Counter
import anim
import os
import requests
import zipfile


def render_comment_list(comment_list: List[Comment], output_filename = 'hello.mp4', music_code = 'PWR'):
    ensure_assets_are_available()
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

def ensure_assets_are_available():
    if not os.path.exists('assets'):
        print('Assets not present. Downloading them')
        response = requests.get('https://dl.luismayo.com/assets.zip')
        with open('assets.zip', 'wb') as file:
            file.write(response.content)
        with zipfile.ZipFile('assets.zip', 'r') as zip_ref:
            zip_ref.extractall('assets')
        os.remove('assets.zip')