from objection_engine.renderer import render_comment_list
from objection_engine.beans.comment import Comment
from time import time

comments = [
    Comment(user_name = 'Phoenix', text_content="The <red>text up here works</red>. But\nI just <red>did a line break</red>"),
]

render_comment_list(comments, f'test-line-breaks-{str(int(time()))}.mp4')
