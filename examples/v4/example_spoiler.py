from objection_engine.v4.make_movie import render_comment_list
from objection_engine.beans.comment import Comment

comments = [
    Comment(
        user_name="first guy",
        text_content="Bad. Sad. Not good at all. Sad crying. I am very unhappy.",
    ),
    Comment(
        user_name="first guy",
        text_content="Puppies happy smile. Ice cream and yum cookies.",
        evidence_path="examples/puppies.jpeg",
    ),
]
render_comment_list(comments, assigned_characters={"first guy": "matt"}, avoid_spoiler_sprites=True)
