from renderer import render_comment_list
from beans.comment import Comment
import anim

comments = [
    Comment(user_name = 'a', text_content='Hello שלום'),
    Comment(user_name = 'e', text_content='Bye!'),
]  *  1
render_comment_list(comments)