from objection_engine.renderer import render_comment_list
from objection_engine.beans.comment import Comment

comments = [
    Comment(
        user_name="Athena",
        text_content="Hi, I'm Athena. How are you doing?",
    ),
    Comment(
        user_name="Athena",
        text_content="I'm doing awful terrible bad bad sad."
    ),

    Comment(
        user_name="Athena",
        text_content="Happy good yay good happy time smile!",
    )
]
render_comment_list(comments, assigned_characters={"Athena": "athena"})
