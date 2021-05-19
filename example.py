from renderer import render_comment_list
from beans.comment import Comment
import anim

comments = [
    Comment(user_name = 'a', text_content='Hello as I am the most common I will be Phoenix'),
    Comment(user_name = 'b', text_content='wassup I\'m edgyboy', user_id='id1'),
    Comment(user_name = 'c', text_content='I\'m someone random and I\'m angry'),
    Comment(user_name = 'b', text_content='im now phoenix hehe', user_id="id2"),
    Comment(user_name = 'd', text_content='Hello OwO'),
    Comment(user_name = 'e', text_content='Hello OwO'),
    Comment(user_name = 'f', text_content='Hello OwO'),
    Comment(user_name = 'g', text_content='Hello OwO'),
    Comment(user_name = 'h', text_content='Hello OwO'),
    Comment(user_name = 'i', text_content='Hello OwO'),
    Comment(user_name = 'j', text_content='Hello OwO'),
    Comment(user_name = 'k', text_content='Hello OwO'),
    Comment(user_name = 'l', text_content='Hello OwO'),
    Comment(user_name = 'm', text_content='Hello OwO'),
    Comment(user_name = 'n', text_content='Hello OwO'),
    Comment(user_name = 'o', text_content='Hello OwO')
]  *  1
render_comment_list(comments)
