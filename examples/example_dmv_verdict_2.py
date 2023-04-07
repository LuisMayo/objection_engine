from objection_engine.ace_attorney_scene import AceAttorneyDirector
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
    DialoguePage(
        [
            DialogueAction("music start pwr/cross-moderato", 0)
        ]
    ),
    DialoguePage(
        [
            DialogueAction(
                f"sprite left assets/characters/phoenix/phoenix-thinking-idle.gif",
                0,
            ),
            DialogueAction(
                "sprite center assets/characters/tigre/tigre-normal-idle.gif", 0
            ),
            DialogueAction("cut center", 0),
            DialogueAction('nametag "Customer"', 0),
            DialogueAction("evidence right examples/ms_daang.png", 0),
            DialogueAction("wait 0.5", 0),
            DialogueAction("showbox", 0),
            DialogueAction("startblip male", 0),
            DialogueAction(
                "sprite center assets/characters/tigre/tigre-normal-talk.gif", 0
            ),
            DialogueTextChunk("MUSTANG", ["green"]),
            DialogueAction(
                "sprite center assets/characters/tigre/tigre-normal-idle.gif", 0
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
            DialogueAction(f"pan left", 0),
            DialogueAction(f"wait {SWITCH_SPRITE_TIME}", 0),
            DialogueAction("show left", 0),
            DialogueAction("show right", 0),
            DialogueAction("hide center", 0),
            DialogueAction(f"wait {1 - SWITCH_SPRITE_TIME}", 0),
            DialogueAction("show center", 0),
            DialogueAction(f"wait 0.1", 0),
        ]
    ),
    DialoguePage([
            DialogueAction('nametag "CA DMV"', 0),
            DialogueAction("wait 0.15", 0),
            DialogueAction("showbox", 0),
            DialogueAction("startblip male", 0),
            DialogueAction(
                f"sprite left assets/characters/phoenix/phoenix-thinking-talk.gif",
                0,
            ),
            DialogueTextChunk("DANG/DAMN?", []),
            DialogueAction("stopblip", 0),
            DialogueAction(
                f"sprite left assets/characters/phoenix/phoenix-thinking-idle.gif",
                0,
            ),
            DialogueAction("showarrow", 0),
            DialogueAction("wait 4", 0),
            DialogueAction("hidebox", 0),
            DialogueAction("sound pichoop", 0),
    ]),

    DialoguePage([
            DialogueAction("hidebox", 0),
            DialogueAction("sprite judge assets/characters/judge/judge-thinking.gif", 0),
            DialogueAction("cut judge", 0),


            DialogueAction("wait 2", 0),
            DialogueAction("verdict set \"Accepted\" white", 0),
            
            DialogueAction("verdict show 0", 0),
            DialogueAction(VERDICT_WAIT_COMMAND, 0),
            DialogueAction("sound guilty", 0),
            DialogueAction(VERDICT_SHAKE_COMMAND, 0),

            DialogueAction("verdict show 1", 0),
            DialogueAction(VERDICT_WAIT_COMMAND, 0),
            DialogueAction("sound guilty", 0),
            DialogueAction(VERDICT_SHAKE_COMMAND, 0),
            
            DialogueAction("verdict show 2", 0),
            DialogueAction(VERDICT_WAIT_COMMAND, 0),
            DialogueAction("sound guilty", 0),
            DialogueAction(VERDICT_SHAKE_COMMAND, 0),

            DialogueAction("verdict show 3", 0),
            DialogueAction(VERDICT_WAIT_COMMAND, 0),
            DialogueAction("sound guilty", 0),
            DialogueAction(VERDICT_SHAKE_COMMAND, 0),

            DialogueAction("verdict show 4", 0),
            DialogueAction(VERDICT_WAIT_COMMAND, 0),
            DialogueAction("sound guilty", 0),
            DialogueAction(VERDICT_SHAKE_COMMAND, 0),

            DialogueAction("verdict show 5", 0),
            DialogueAction(VERDICT_WAIT_COMMAND, 0),
            DialogueAction("sound guilty", 0),
            DialogueAction(VERDICT_SHAKE_COMMAND, 0),

            DialogueAction("verdict show 6", 0),
            DialogueAction(VERDICT_WAIT_COMMAND, 0),
            DialogueAction("sound guilty", 0),
            DialogueAction(VERDICT_SHAKE_COMMAND, 0),

            DialogueAction("verdict show 7", 0),
            DialogueAction(VERDICT_WAIT_COMMAND, 0),
            DialogueAction("sound guilty", 0),
            DialogueAction(VERDICT_SHAKE_COMMAND, 0),
            DialogueAction("wait 5", 0),
        ]
    )
]

director = AceAttorneyDirector()
director.set_current_pages(pages)
director.render_movie(output_filename=f"dmv-{int(time())}.mp4")