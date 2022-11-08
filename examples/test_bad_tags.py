from objection_engine.renderer import render_comment_list
from objection_engine.beans.comment import Comment
from time import time

comments = [
    Comment(user_name = 'a', text_content='Hello as I am the most common <red>I will be Phoenix</red>'),
    Comment(user_name= 'second person', text_content="Here is a closing tag</blue> without an opening tag. This should not crash."),
    Comment(user_name="third person", text_content="Here <red>are some <blue>mismatched tags</red></blue>."),
    Comment(user_name="another person", text_content="And here's <foobar>a tag that shouldn't exist</foobar>.")
]
render_comment_list(comments, f'output-{str(int(time()))}.mp4')
