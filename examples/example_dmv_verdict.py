from objection_engine.ace_attorney_scene import AceAttorneyDirector
from objection_engine.composers.compose_verdict import compose_verdict
from objection_engine.parse_tags import (
    DialoguePage,
    DialogueAction,
    DialogueTextChunk,
    DialogueTextLineBreak,
)
from time import time

SWITCH_SPRITE_TIME = 0.18

VERDICT_SHAKE_COMMAND = "shake 4 0.1"
VERDICT_WAIT_COMMAND = "wait 0.2"

pages = [
    DialoguePage([DialogueAction("music start pwr/cross-moderato", 0)]),
    DialoguePage(
        [
            DialogueAction(
                "sprite center assets/characters/dahlia/dahlia-normal-idle.gif", 0
            ),
            DialogueAction("cut center", 0),
            DialogueAction('nametag "Customer"', 0),
            DialogueAction("evidence right examples/fish.png", 0),
            DialogueAction("wait 0.5", 0),
            DialogueAction("showbox", 0),
            DialogueAction("startblip female", 0),
            DialogueAction(
                "sprite center assets/characters/dahlia/dahlia-normal-talk.gif", 0
            ),
            DialogueTextChunk("I LOVE TO FISH", ["green"]),
            DialogueAction(
                "sprite center assets/characters/dahlia/dahlia-normal-idle.gif", 0
            ),
            DialogueAction("stopblip", 0),
            DialogueAction("showarrow", 0),
            DialogueAction("wait 4", 0),
            DialogueAction("hidearrow", 0),
            DialogueAction("sound pichoop", 0),
            DialogueAction("wait 0.3", 0),
        ]
    ),
    DialoguePage(
        [
            DialogueAction("hidebox", 0),
            DialogueAction("evidence clear", 0),
            DialogueAction("flash 0.1", 0),
            DialogueAction("bubble objection phoenix", 0),
            DialogueAction(f"wait 0.1", 0),
            DialogueAction("music stop", 0),
            DialogueAction(f"wait 1.2", 0),
            DialogueAction("hidebox", 0),
            DialogueAction("wait 0.25", 0),
            DialogueAction(f"pan left", 0),
            DialogueAction(
                f"sprite left assets/characters/phoenix/phoenix-handsondesk-idle.gif",
                0,
            ),
            DialogueAction(f"wait {SWITCH_SPRITE_TIME}", 0),
            DialogueAction("show left", 0),
            DialogueAction("show right", 0),
            DialogueAction("hide center", 0),
            DialogueAction(f"wait {1 - SWITCH_SPRITE_TIME}", 0),
            DialogueAction("show center", 0),
            DialogueAction(f"wait 0.1", 0),
            DialogueAction(
                f"sprite left assets/characters/phoenix/phoenix-deskslam.gif",
                0,
            ),
            DialogueAction("wait 0.15", 0),
            DialogueAction("sound deskslam", 0),
            DialogueAction("wait 0.7", 0),
            DialogueAction(
                f"sprite left assets/characters/phoenix/phoenix-handsondesk-idle.gif",
                0,
            ),
            DialogueAction("wait 0.5", 0),
        ]
    ),
    DialoguePage(
        [
            DialogueAction('nametag "CA DMV"', 0),
            DialogueAction(
                f"sprite leftzoom assets/characters/phoenix/phoenix-zoom-idle.gif",
                0,
            ),
            DialogueAction(f"music start pwr/press", 0),
            # DialogueAction("flash 0.1", 0),
            DialogueAction("cut leftzoom", 0),
            DialogueAction("wait 0.15", 0),
            DialogueAction("showbox", 0),
            DialogueAction("startblip male", 0),
            DialogueAction(
                f"sprite leftzoom assets/characters/phoenix/phoenix-zoom-talk.gif",
                0,
            ),
            DialogueTextChunk("SEXUAL CONNOTATIONS", []),
            DialogueAction("flash 0.15", 0),
            DialogueAction("shake 5 0.3", 0),
            DialogueAction("sound objection", 0),
            DialogueAction("stopblip", 0),
            DialogueAction(
                f"sprite leftzoom assets/characters/phoenix/phoenix-zoom-idle.gif",
                0,
            ),
            DialogueAction("showarrow", 0),
            DialogueAction("wait 4", 0),
            DialogueAction("hidebox", 0),
            DialogueAction("sound pichoop", 0),
        ]
    ),
    DialoguePage(
        [
            DialogueAction("hidebox", 0),
            DialogueAction(
                "sprite judge assets/characters/judge/judge-thinking.gif", 0
            ),
            DialogueAction("cut judge", 0),
            DialogueAction("wait 2", 0),
        ]
        + compose_verdict("Denied", slam_group="letter", color="black")
        + [
            DialogueAction("wait 5", 0),
        ]
    ),
]

director = AceAttorneyDirector()
director.set_current_pages(pages)
director.render_movie(output_filename=f"dmv-verdict-{int(time())}.mp4")
