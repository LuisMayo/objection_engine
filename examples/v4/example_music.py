from objection_engine.make_movie import render_comment_list
from objection_engine.beans.comment import Comment

comments = [
    Comment(
        user_name="Phoenix",
        text_content="Hello, everyone. My name is Phoenix.",
    ),
    Comment(
        user_name="Phoenix",
        text_content="The defense is ready, Your Honor!"
    ),
    Comment(
        user_name="Phoenix",
        text_content="And here's a little more text! Isn't this cool?",
    )
]
render_comment_list(comments, music_code='dd')