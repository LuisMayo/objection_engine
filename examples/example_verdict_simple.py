from time import time
from objection_engine.ace_attorney_scene import AceAttorneyDirector
from objection_engine.parse_tags import DialoguePage, DialogueAction

pages = [
    DialoguePage(
        [
            DialogueAction("cut judge", 0),
            DialogueAction("hidebox", 0),
            DialogueAction(
                "sprite judge assets/characters/judge/judge-normal-idle.gif", 0
            ),
        ]
    ),
    DialoguePage(
        [
            # Initialize the verdict text.
            DialogueAction("verdict set 'Very Cool' white", 0),
            # Animate in the first word, "Very".
            DialogueAction("verdict show 0", 0),  # V
            DialogueAction("verdict show 1", 0),  # e
            DialogueAction("verdict show 2", 0),  # r
            DialogueAction("verdict show 3", 0),  # y
            DialogueAction("verdict show 4", 0),  # SPACE
            # Play the slam sound effect (called "guilty")
            # and shake the screen. This happens after a short delay
            # so that they line up with the letters' animations finishing.
            DialogueAction("wait 0.2", 0),
            DialogueAction("sound guilty", 0),
            DialogueAction("shake 4 0.1", 0),
            # Include a short delay between words "Very" and "Cool".
            DialogueAction("wait 0.5", 0),
            # Animate in the second word, "Cool".
            DialogueAction("verdict show 5", 0),  # C
            DialogueAction("verdict show 6", 0),  # o
            DialogueAction("verdict show 7", 0),  # o
            DialogueAction("verdict show 8", 0),  # l
            # Same effects as before but for the second word.
            DialogueAction("wait 0.2", 0),
            DialogueAction("sound guilty", 0),
            DialogueAction("shake 4 0.1", 0),
            # Let the words stay on screen for a few seconds.
            DialogueAction("wait 2.0", 0),
            # Clear the verdict text.
            DialogueAction("verdict clear", 0),
        ]
    ),
]

director = AceAttorneyDirector()
director.set_current_pages(pages)
director.render_movie(output_filename=f"example-verdict-simple-{int(time())}.mp4")
