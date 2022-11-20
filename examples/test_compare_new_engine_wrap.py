from objection_engine.renderer import render_comment_list
from objection_engine.beans.comment import Comment
from time import time

comments = [
    Comment(user_name='Phoenix right', text_content='I am going to slam the desk! I just did it! Did you see that? Was i cool?'),
    Comment(user_name='Phoenix right', text_content='...Hello? ...Is anyone there?'),
    Comment(user_name='Mr edge worth', text_content='Yes, I saw it. But it was not very impressive. Look, I can do the same thing. See?'),
]
render_comment_list(comments, f'test-compare-wrapping-{str(int(time()))}.mp4')