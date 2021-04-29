from enum import IntEnum

# Classes
class Action(IntEnum):
    TEXT = 1
    SHAKE_EFFECT = 2
    OBJECTION = 3
    TEXT_SHAKE_EFFECT = 4

class Character():
    PHOENIX = 'PHOENIX'
    EDGEWORTH = 'EDGEWORTH'
    GODOT = 'GODOT'
    FRANZISKA = 'FRANZISKA'
    JUDGE = 'JUDGE'
    LARRY = 'LARRY'
    MAYA = 'MAYA'
    KARMA = 'KARMA'
    PAYNE = 'PAYNE'
    MAGGEY = 'MAGGEY'
    PEARL = 'PEARL'
    LOTTA = 'LOTTA'
    GUMSHOE = 'GUMSHOE'
    GROSSBERG = 'GROSSBERG'


class Location(IntEnum):
    COURTROOM_LEFT = 1
    WITNESS_STAND = 2
    COURTROOM_RIGHT = 3
    CO_COUNCIL = 4
    JUDGE_STAND = 5
    COURT_HOUSE = 6
    def __str__(self):
        return str(self.name).capitalize()

# Maps
character_emotions = {
    Character.EDGEWORTH: {
        "happy": ["confident", "pointing", "smirk"],
        "neutral": ["document", "normal", "thinking"],
        "sad": ["handondesk"],
    },
    Character.PHOENIX: {
        "happy": ["confident", "pointing", "handsondesk"],
        "neutral": ["document", "normal", "thinking", "coffee"],
        "sad": ["emo", "sheepish", "sweating"],
    },
    Character.MAYA: {
        "happy": ["bench"],
        "neutral": ["bench-hum", "bench-profile"],
        "sad": ["bench-strict", "bench-ugh"],
    },
    Character.LARRY: {
        "happy": ["hello"],
        "neutral": ["normal"],
        "sad": ["extra", "mad", "nervous"],
    },
    Character.GODOT: {
        "happy": ["normal"],
        "neutral": ["normal"],
        "sad": ["steams", "pointing"],
    },
    Character.FRANZISKA: {
        "happy": ["ha"],
        "neutral": ["ready"],
        "sad": ["mad", "sweating", "withwhip"],
    },
    Character.JUDGE: {
        "happy": ["nodding"],
        "neutral": ["normal"],
        "sad": ["headshake", "warning"],
    },
    Character.KARMA: {
        "happy": ["smirk", "snap"],
        "neutral": ["normal"],
        "sad": ["badmood", "break", "sweat"],
    },
    Character.PAYNE: {
        "happy": ["confident"],
        "neutral": ["normal"],
        "sad": ["sweating"],
    },
    Character.MAGGEY: {
        "happy": ["pumped", "shining"],
        "neutral": ["normal"],
        "sad": ["sad"],
    },
    Character.PEARL: {
        "happy": ["sparkle", "surprised"],
        "neutral": ["normal", "shy", "thinking"],
        "sad": ["cries", "disappointed", "fight"],
    },
    Character.LOTTA: {
        "happy": ["confident", "smiling"],
        "neutral": ["normal", "shy", "thinking"],
        "sad": ["badmood", "disappointed", "mad"],
    },
    Character.GUMSHOE: {
        "happy": ["laughing", "confident", "pumped"],
        "neutral": ["normal", "shy", "side", "thinking"],
        "sad": ["disheartened", "mad"],
    },
    Character.GROSSBERG: {
        "happy": ["normal"],
        "neutral": ["normal"],
        "sad": ["sweating"],
    },
}

character_map = {
    Character.PHOENIX: "assets/Sprites-phoenix",
    Character.EDGEWORTH: "assets/Sprites-edgeworth",
    Character.GODOT: "assets/Sprites-Godot",
    Character.FRANZISKA: "assets/Sprites-franziska",
    Character.JUDGE: "assets/Sprites-judge",
    Character.LARRY: "assets/Sprites-larry",
    Character.MAYA: "assets/Sprites-maya",
    Character.KARMA: "assets/Sprites-karma",
    Character.PAYNE: "assets/Sprites-payne",
    Character.MAGGEY: "assets/Sprites-Maggey",
    Character.PEARL: "assets/Sprites-Pearl",
    Character.LOTTA: "assets/Sprites-lotta",
    Character.GUMSHOE: "assets/Sprites-gumshoe",
    Character.GROSSBERG: "assets/Sprites-grossberg",
}

character_location_map = {
    Character.PHOENIX: Location.COURTROOM_LEFT,
    Character.EDGEWORTH: Location.COURTROOM_RIGHT,
    Character.GODOT: Location.COURTROOM_RIGHT,
    Character.FRANZISKA: Location.COURTROOM_RIGHT,
    Character.JUDGE: Location.JUDGE_STAND,
    Character.LARRY: Location.WITNESS_STAND,
    Character.MAYA: Location.CO_COUNCIL,
    Character.KARMA: Location.COURTROOM_RIGHT,
    Character.PAYNE: Location.COURTROOM_RIGHT,
    Character.MAGGEY: Location.WITNESS_STAND,
    Character.PEARL: Location.WITNESS_STAND,
    Character.LOTTA: Location.WITNESS_STAND,
    Character.GUMSHOE: Location.WITNESS_STAND,
    Character.GROSSBERG: Location.WITNESS_STAND,
}


location_map = {
    Location.COURTROOM_LEFT: "assets/defenseempty.png",
    Location.WITNESS_STAND: "assets/witnessempty.png",
    Location.COURTROOM_RIGHT: "assets/prosecutorempty.png",
    Location.CO_COUNCIL: "assets/helperstand.png",
    Location.JUDGE_STAND: "assets/judgestand.png",
    Location.COURT_HOUSE: "assets/courtroomoverview.png",
}


# Single_constants
fps = 18
lag_frames = 25
