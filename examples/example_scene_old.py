from objection_engine.ace_attorney_scene import (
    AceAttorneyDirector,
    get_boxes_with_pauses,
)

from objection_engine.parse_tags import (
    DialoguePage,
    DialogueAction
)

pages: list[DialoguePage] = []

pages.append(DialoguePage([DialogueAction("music start cross-moderato", 0)]))
pages.extend(
    get_boxes_with_pauses(
        user_name="Phoenix",
        character="phoenix",
        text="Hello it is I, Phoenix Wright. I am saying some lines of text.",
    )
)
pages.extend(
    get_boxes_with_pauses(
        user_name="Edgeworth",
        character="edgeworth",
        text="And I am the antagonist, Edgeworth. I am also saying some lines of text. Here is a third line, because I am very serious.",
    )
)
pages.extend(
    get_boxes_with_pauses(
        user_name="Gumshoe",
        character="gumshoe",
        text="Hey, pal! I'm on the witness stand! Ain't that cool? Woah ho ho look at me!",
    )
)
pages.extend(
    get_boxes_with_pauses(
        user_name="Judge",
        character="judge",
        text="And I'm over here, on another screen! Isn't that just the neatest thing?",
    )
)

pages.extend(
    get_boxes_with_pauses(
        user_name="Lotta",
        character="lotta",
        text="Don't forget about me, m'kay? I'm still here too.",
    )
)

director = AceAttorneyDirector()
director.set_current_pages(pages)
director.render_movie(-15)
