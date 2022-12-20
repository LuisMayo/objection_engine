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