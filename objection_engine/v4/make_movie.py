from objection_engine.v4.ace_attorney_scene import (
    AceAttorneyDirector,
    DialogueBoxBuilder,
)

from objection_engine.beans.comment import Comment

try:
    from rich import print
except:
    pass


def render_comment_list(
    comment_list: list["Comment"],
    output_filename: str = "hello.mp4",
    music_code: str = "pwr",
    resolution_scale: int = 1,
    assigned_characters: dict = None,
    adult_mode: bool = False,
):
    builder = DialogueBoxBuilder()
    builder.build_from_comments(
        comment_list, music_code, assigned_characters, adult_mode
    )

    director = AceAttorneyDirector()
    director.set_current_pages(builder.pages)
    director.render_movie(-15)
