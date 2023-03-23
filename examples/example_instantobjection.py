from objection_engine.renderer import render_comment_list
from objection_engine.beans.comment import Comment

comments = [
    Comment(
        user_name="Phoenix",
        text_content="I HATE YOU SO MUCH!!",
    ),
    Comment(user_name="Phoenix", text_content="(not really i just really needed to trigger the objection bubble)"),
    Comment(
        user_name="Edgeworth",
        text_content="I am Edgeworth, because I have the second-most lines.",
    ),
]

render_comment_list(comments)