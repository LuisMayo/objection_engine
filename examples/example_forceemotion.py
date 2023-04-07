from objection_engine.renderer import render_comment_list
from objection_engine.beans.comment import Comment
from time import time

comments = [
    Comment(
        user_name="Phoenix",
        text_content="This is a neutral sentence.",
    ),
    Comment(
        user_name="Phoenix",
        text_content="Grr I'm so angry I hate you so much!!"
    ),
    Comment(
        user_name="Phoenix",
        text_content="Now with forced positive sentiment..."
    ),
    Comment(
        user_name="Phoenix",
        text_content="Grr I'm so angry I hate you so much!!",
        score=1
    ),
    Comment(
        user_name="Phoenix",
        text_content="Now let's test the opposite. A positive comment:"
    ),
    Comment(
        user_name="Phoenix",
        text_content="I love you so much I love puppies and cats they are cute :)",
    ),
    Comment(
        user_name="Phoenix",
        text_content="And with forced negative sentiment..."
    ),
    Comment(
        user_name="Phoenix",
        text_content="I love you so much I love puppies and cats they are cute :)",
        score=-1
    ),
]

render_comment_list(comments, output_filename=f"output-{int(time())}.mp4", resolution_scale=2.0)