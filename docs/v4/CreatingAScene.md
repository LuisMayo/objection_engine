# Creating a Scene
*Objection 4* has a few different ways to build scenes before rendering them.
Some methods are simpler but leave more up to random chance, whereas other
methods are more intense but allow finer control over the finished video.

## The Easy Way (compatible with *Objection 3* code)
Most of the time, you can use the `render_comment_list()` method from 
`objection_engine.v4.make_movie` to quickly and easily generate scenes.

Here is the script `examples/v4/example_easy.py`, and a video it produces.
(Note that because the engine uses randomness to choose things like sprites or
music tracks, your output may not match the linked video exactly.)
```python
from objection_engine.v4.make_movie import render_comment_list
from objection_engine.beans.comment import Comment

comments = [
    Comment(
        user_name="Phoenix",
        text_content="Hello. My name is Phoenix. I am a defense attorney.",
    ),
    Comment(user_name="Phoenix", text_content="Here is another line of dialogue."),
    Comment(
        user_name="Edgeworth",
        text_content="I am Edgeworth, because I have the second-most lines.",
    ),
]

render_comment_list(comments)
```

## The Hard Way (building everything yourself)
This script, `examples/v4/example_hard.py`, produces equivalent output to
`example_easy.py`, but controls all of the scene actions manually. As a result,
this example *should* always result in an identical video.

Unlike when using `render_comment_list()`, it will not display progress bars.

```python
from objection_engine.v4.ace_attorney_scene import AceAttorneyDirector
from objection_engine.v4.parse_tags import (
    DialoguePage,
    DialogueAction,
    DialogueTextChunk,
    DialogueTextLineBreak,
)

pages = [
    DialoguePage([DialogueAction("music start pwr/cross-moderato", 0)]),
    DialoguePage(
        [
            DialogueAction("wait 0.03", 0),
            DialogueAction(
                "sprite left assets_v4/characters/phoenix/phoenix-normal-idle.gif", 0
            ),
            DialogueAction("cut left", 0),
            DialogueAction('nametag "Phoenix"', 0),
            DialogueAction("showbox", 0),
            DialogueAction("evidence clear", 0),
            DialogueAction("startblip male", 0),
            DialogueAction(
                "sprite left assets_v4/characters/phoenix/phoenix-normal-talk.gif", 0
            ),
            DialogueTextChunk("Hello", []),
            DialogueTextChunk(".", []),
            DialogueAction("stopblip", 0),
            DialogueTextChunk(" ", []),
            DialogueAction(
                "sprite left assets_v4/characters/phoenix/phoenix-normal-idle.gif", 0
            ),
            DialogueAction("wait 0.6", 0),
            DialogueAction("startblip male", 0),
            DialogueAction(
                "sprite left assets_v4/characters/phoenix/phoenix-handsondesk-talk.gif",
                0,
            ),
            DialogueTextChunk("My", []),
            DialogueTextChunk(" ", []),
            DialogueTextChunk("name", []),
            DialogueTextChunk(" ", []),
            DialogueTextChunk("is", []),
            DialogueTextChunk(" ", []),
            DialogueTextChunk("Phoenix", []),
            DialogueTextChunk(".", []),
            DialogueAction(
                "sprite left assets_v4/characters/phoenix/phoenix-handsondesk-idle.gif",
                0,
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
            DialogueAction("wait 0.03", 0),
            DialogueAction(
                "sprite left assets_v4/characters/phoenix/phoenix-handsondesk-idle.gif",
                0,
            ),
            DialogueAction("cut left", 0),
            DialogueAction('nametag "Phoenix"', 0),
            DialogueAction("showbox", 0),
            DialogueAction("startblip male", 0),
            DialogueAction(
                "sprite left assets_v4/characters/phoenix/phoenix-handsondesk-talk.gif",
                0,
            ),
            DialogueTextChunk("I", []),
            DialogueTextChunk(" ", []),
            DialogueTextChunk("am", []),
            DialogueTextChunk(" ", []),
            DialogueTextChunk("a", []),
            DialogueTextChunk(" ", []),
            DialogueTextChunk("defense", []),
            DialogueTextChunk(" ", []),
            DialogueTextChunk("attorney", []),
            DialogueTextChunk(".", []),
            DialogueAction("stopblip", 0),
            DialogueTextChunk(" ", []),
            DialogueAction(
                "sprite left assets_v4/characters/phoenix/phoenix-handsondesk-idle.gif",
                0,
            ),
            DialogueAction(
                "sprite left assets_v4/characters/phoenix/phoenix-handsondesk-idle.gif",
                0,
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
            DialogueAction("wait 0.03", 0),
            DialogueAction(
                "sprite left assets_v4/characters/phoenix/phoenix-handsondesk-idle.gif",
                0,
            ),
            DialogueAction("cut left", 0),
            DialogueAction('nametag "Phoenix"', 0),
            DialogueAction("showbox", 0),
            DialogueAction("evidence clear", 0),
            DialogueAction("startblip male", 0),
            DialogueAction(
                "sprite left assets_v4/characters/phoenix/phoenix-handsondesk-talk.gif",
                0,
            ),
            DialogueTextChunk("Here", []),
            DialogueTextChunk(" ", []),
            DialogueTextChunk("is", []),
            DialogueTextChunk(" ", []),
            DialogueTextChunk("another", []),
            DialogueTextChunk(" ", []),
            DialogueTextChunk("line", []),
            DialogueTextChunk(" ", []),
            DialogueTextChunk("of", []),
            DialogueTextChunk(" ", []),
            DialogueTextChunk("dialogue", []),
            DialogueTextChunk(".", []),
            DialogueAction("stopblip", 0),
            DialogueTextChunk(" ", []),
            DialogueAction(
                "sprite left assets_v4/characters/phoenix/phoenix-handsondesk-idle.gif",
                0,
            ),
            DialogueAction(
                "sprite left assets_v4/characters/phoenix/phoenix-handsondesk-idle.gif",
                0,
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
            DialogueAction("wait 0.03", 0),
            DialogueAction("hidebox", 0),
            DialogueAction("wait 0.5", 0),
            DialogueAction("pan right", 0),
            DialogueAction(
                "sprite right assets_v4/characters/edgeworth/edgeworth-document-idle.gif",
                0,
            ),
            DialogueAction("wait 1.0", 0),
            DialogueAction('nametag "Edgeworth"', 0),
            DialogueAction("showbox", 0),
            DialogueAction("evidence clear", 0),
            DialogueAction("startblip male", 0),
            DialogueAction(
                "sprite right assets_v4/characters/edgeworth/edgeworth-document-talk.gif",
                0,
            ),
            DialogueTextChunk("I", []),
            DialogueTextChunk(" ", []),
            DialogueTextChunk("am", []),
            DialogueTextChunk(" ", []),
            DialogueTextChunk("Edgeworth", []),
            DialogueTextChunk(",", []),
            DialogueAction("stopblip", 0),
            DialogueAction(
                "sprite right assets_v4/characters/edgeworth/edgeworth-document-idle.gif",
                0,
            ),
            DialogueAction("wait 0.3", 0),
            DialogueAction("startblip male", 0),
            DialogueAction(
                "sprite right assets_v4/characters/edgeworth/edgeworth-document-talk.gif",
                0,
            ),
            DialogueTextChunk(" ", []),
            DialogueTextChunk("because", []),
            DialogueTextChunk(" ", []),
            DialogueTextChunk("I", []),
            DialogueTextChunk(" ", []),
            DialogueTextChunk("have", []),
            DialogueTextChunk(" ", []),
            DialogueTextLineBreak(),
            DialogueTextChunk("the", []),
            DialogueTextChunk(" ", []),
            DialogueTextChunk("second", []),
            DialogueTextChunk("-", []),
            DialogueAction("stopblip", 0),
            DialogueAction(
                "sprite right assets_v4/characters/edgeworth/edgeworth-document-idle.gif",
                0,
            ),
            DialogueAction("wait 0.3", 0),
            DialogueAction("startblip male", 0),
            DialogueAction(
                "sprite right assets_v4/characters/edgeworth/edgeworth-document-talk.gif",
                0,
            ),
            DialogueTextChunk(" ", []),
            DialogueTextChunk("most", []),
            DialogueTextChunk(" ", []),
            DialogueTextChunk("lines", []),
            DialogueTextChunk(".", []),
            DialogueAction("stopblip", 0),
            DialogueTextChunk(" ", []),
            DialogueAction(
                "sprite right assets_v4/characters/edgeworth/edgeworth-document-idle.gif",
                0,
            ),
            DialogueAction(
                "sprite right assets_v4/characters/edgeworth/edgeworth-document-idle.gif",
                0,
            ),
            DialogueAction("stopblip", 0),
            DialogueAction("showarrow", 0),
            DialogueAction("wait 2", 0),
            DialogueAction("hidearrow", 0),
            DialogueAction("sound pichoop", 0),
            DialogueAction("wait 0.3", 0),
        ]
    ),
]

director = AceAttorneyDirector()
director.set_current_pages(pages)
director.render_movie()
```