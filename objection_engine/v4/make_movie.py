from objection_engine.v4.ace_attorney_scene import (
    AceAttorneyDirector,
    DialogueBoxBuilder,
)

from objection_engine.beans.comment import Comment
from objection_engine.v4.parse_tags import DialoguePage

from rich import print
from rich.live import Live
from rich.table import Table
from rich.progress import (
    Progress,
    TextColumn,
    BarColumn,
    MofNCompleteColumn,
    TaskProgressColumn,
    TimeElapsedColumn,
)


def render_comment_list(
    comment_list: list["Comment"],
    output_filename: str = "hello.mp4",
    music_code: str = "pwr",
    resolution_scale: int = 1,
    assigned_characters: dict = None,
    adult_mode: bool = False,
    avoid_spoiler_sprites: bool = False,
):
    with Progress(
        TextColumn("[progress.description]{task.description}"),
        BarColumn(),
        TaskProgressColumn(),
        MofNCompleteColumn(),
        TimeElapsedColumn(),
    ) as progress:
        process_comments_task = progress.add_task(
            "Processing comments...", start=True, total=len(comment_list), visible=False
        )
        complete_pages_task = progress.add_task(
            "Rendering video...", total=0, start=False, visible=False
        )
        composite_audio_task = progress.add_task(
            "Rendering audio...", total=0, start=False, visible=False
        )
        composite_task = progress.add_task(
            "Compositing...", total=0, start=False, visible=False
        )

        def on_characters_cast(cast: dict):
            cast_table = Table("User ID", "Character ID", title="Cast")
            for username, character in cast.items():
                cast_table.add_row(username, character)
            print(cast_table)

        def on_comment_processed(
            comment_index: int, num_comments: int, comment: Comment
        ):
            progress.update(
                process_comments_task,
                completed=comment_index + 1,
                total=num_comments,
                refresh=True,
                visible=True,
            )

        def on_page_completed(
            page_index,
            num_pages: int,
            page: DialoguePage,
            time_to_render: float,
            time_onscreen: float,
        ):
            print(
                f'"{page.get_raw_text():30.30s}"\t\tRender {time_to_render:3.2f} sec\t\tVisible {time_onscreen:3.2f} sec\t\t{time_to_render / time_onscreen:3.2f} SPS'
            )
            progress.start_task(complete_pages_task)
            progress.update(
                complete_pages_task,
                completed=page_index + 1,
                total=num_pages,
                refresh=True,
                visible=True,
            )

        def on_all_pages_completed():
            pass

        def on_audio_composite_progress(audio_index: int, num_audios: int, audio: dict):
            progress.start_task(composite_audio_task)
            progress.update(
                composite_audio_task,
                completed=audio_index + 1,
                total=num_audios,
                refresh=True,
                visible=True,
            )

        def on_ffmpeg_started():
            progress.start_task(composite_task)
            progress.update(
                composite_task, completed=0, total=1, refresh=True, visible=True
            )

        def on_ffmpeg_finished():
            progress.update(composite_task, completed=1, refresh=True)

        callbacks = {
            "on_characters_cast": on_characters_cast,
            "on_comment_processed": on_comment_processed,
            "on_page_completed": on_page_completed,
            "on_all_pages_completed": on_all_pages_completed,
            "on_audio_composite_progress": on_audio_composite_progress,
            "on_ffmpeg_started": on_ffmpeg_started,
            "on_ffmpeg_finished": on_ffmpeg_finished,
        }

        builder = DialogueBoxBuilder(callbacks=callbacks)
        builder.render(
            comment_list,
            music_code=music_code,
            assigned_characters=assigned_characters,
            adult_mode=adult_mode,
            avoid_spoiler_sprites=avoid_spoiler_sprites,
        )
