from time import time
from objection_engine.ace_attorney_scene import AceAttorneyDirector
from objection_engine.parse_tags import (
    DialoguePage,
    DialogueAction,
    DialogueTextChunk,
)

pages = [
    DialoguePage([DialogueAction("music start pwr/cross-moderato", 0)]),
    DialoguePage(
        [
            DialogueAction(
                "sprite judge assets/characters/judge/judge-normal-idle.gif", 0
            ),
            DialogueAction("cut judge", 0),
            DialogueAction("nametag 'Judge'", 0),
            DialogueAction("showbox", 0),
            DialogueAction("startblip male", 0),
            DialogueAction(
                "sprite judge assets/characters/judge/judge-normal-talk.gif", 0
            ),
            DialogueTextChunk("I'm going to slam my gavel.", []),
            DialogueAction(
                "sprite judge assets/characters/judge/judge-normal-idle.gif", 0
            ),
            DialogueAction("stopblip", 0),
            DialogueAction("showarrow", 0),
            DialogueAction("wait 2", 0),
            DialogueAction("hidearrow", 0),
            DialogueAction("sound pichoop", 0),
            DialogueAction("wait 0.3", 0),
        ]
    ),
    DialoguePage(
        [
            DialogueAction("hidebox", 0),
            DialogueAction("cut gavel", 0),
            DialogueAction("gavel 0", 0),
            DialogueAction("wait 0.3", 0),
            DialogueAction("gavel 1", 0),
            DialogueAction("wait 0.04", 0),
            DialogueAction("gavel 2", 0),
            DialogueAction("wait 0.04", 0),
            DialogueAction("gavel 3", 0),
            DialogueAction("sound gavel", 0),
            DialogueAction("shake 3 0.2", 0),
            DialogueAction("wait 0.766", 0),
        ]
    ),
    DialoguePage(
        [
            DialogueAction("hidebox", 0),
            DialogueAction("cut judge", 0),
            DialogueAction("nametag 'Judge'", 0),
            DialogueAction("showbox", 0),
            DialogueAction("startblip male", 0),
            DialogueAction(
                "sprite judge assets/characters/judge/judge-normal-talk.gif", 0
            ),
            DialogueTextChunk("Now I'll do it three times.", []),
            DialogueAction(
                "sprite judge assets/characters/judge/judge-normal-idle.gif", 0
            ),
            DialogueAction("stopblip", 0),
            DialogueAction("showarrow", 0),
            DialogueAction("wait 2", 0),
            DialogueAction("hidearrow", 0),
            DialogueAction("sound pichoop", 0),
            DialogueAction("wait 0.3", 0),
        ]
    ),
    DialoguePage(
        [
            DialogueAction("hidebox", 0),
            DialogueAction("cut gavel", 0),
            DialogueAction("gavel 0", 0),
            DialogueAction("wait 0.300", 0),
            DialogueAction("gavel 1", 0),
            DialogueAction("wait 0.04", 0),
            DialogueAction("gavel 3", 0),
            DialogueAction("sound gavel", 0),
            DialogueAction("shake 3 0.2", 0),
            DialogueAction("wait 0.17", 0),
            DialogueAction("gavel 2", 0),
            DialogueAction("wait 0.04", 0),
            DialogueAction("gavel 1", 0),
            DialogueAction("wait 0.17", 0),
            DialogueAction("gavel 3", 0),
            DialogueAction("sound gavel", 0),
            DialogueAction("shake 3 0.2", 0),
            DialogueAction("wait 0.17", 0),
            DialogueAction("gavel 2", 0),
            DialogueAction("wait 0.04", 0),
            DialogueAction("gavel 1", 0),
            DialogueAction("wait 0.17", 0),
            DialogueAction("gavel 2", 0),
            DialogueAction("wait 0.04", 0),
            DialogueAction("gavel 3", 0),
            DialogueAction("sound gavel", 0),
            DialogueAction("shake 3 0.2", 0),
            DialogueAction("wait 0.766", 0),
        ]
    ),
]

director = AceAttorneyDirector()
director.set_current_pages(pages)
director.render_movie(output_filename=f"example-gavel-{int(time())}.mp4")
