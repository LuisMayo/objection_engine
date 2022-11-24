from objection_engine.v4.ace_attorney_scene import AceAttorneyDirector, get_sprite_tag

from objection_engine.v4.tag_macros import (
    SPR_PHX_NORMAL_T,
    SPR_PHX_NORMAL_I,
    SPR_PHX_SWEAT_T,
    SPR_PHX_SWEAT_I,
    SPR_EDW_NORMAL_T,
    SPR_EDW_NORMAL_I,
    SLAM_PHX,
    SLAM_EDW,
    OBJ_PHX,
    OBJ_EDW,
    HDI_PHX,
    END_BOX,
    S_DRAMAPOUND,
    S_SMACK,
)

from objection_engine.v4.parse_tags import DialoguePage, DialogueAction, get_rich_boxes

test_dialogue_1 = (
    f'<music start cross-moderato/><nametag "Phoenix right"/><showbox/>'
    + f"{SPR_PHX_NORMAL_T}I am going to <red>slam the desk</red>!"
    + f"{SPR_PHX_NORMAL_I}<wait 0.25/>{OBJ_PHX}"
    + f"{SLAM_PHX}{SPR_PHX_NORMAL_T} I just did it!{SPR_PHX_NORMAL_I}{HDI_PHX}"
    + f" {SPR_PHX_NORMAL_T}Did you see that?{SPR_PHX_NORMAL_I}{S_DRAMAPOUND}<wait 0.5/>"
    + f" {SPR_PHX_NORMAL_T}<green>Was I cool?</green>{SPR_PHX_NORMAL_I}{END_BOX}<hidebox/>"
)

test_dialogue_2 = (
    f'<nametag "Phoenix right"/><showbox/>{SPR_PHX_SWEAT_T}...Hello?'
    + f"{SPR_PHX_SWEAT_I}<wait 0.25/>{SPR_PHX_SWEAT_T} ...Is anyone there?"
    + f" {SPR_PHX_SWEAT_I}{END_BOX}<hidebox/>"
)

test_dialogue_3 = (
    f"<music stop/>{OBJ_EDW}<pan right/><wait 1/>"
    + f'<nametag "Mr edge worth"/><showbox/>'
    + f"{SPR_EDW_NORMAL_T}Yes, I saw it.{SPR_EDW_NORMAL_I}<wait 0.1/> "
    + f"{SPR_EDW_NORMAL_T}But it was not very impressive.<music start pursuit/>{SPR_EDW_NORMAL_I}<wait 1/> "
    + f"{SPR_EDW_NORMAL_T}Look,{S_SMACK} I can do the same thing.{SLAM_EDW} "
    + f"{SPR_EDW_NORMAL_T}See?{SPR_EDW_NORMAL_I}"
    + f"{END_BOX}"
)

def write_page(user_name: str, character: str, text: str):
    # Get character gender and use appropriate blips
    character_data = {
        "phoenix": {
            "pos": "left",
            "gender": "male"
        },
        "edgeworth": {
            "pos": "right",
            "gender": "male"
        },
        "judge": {
            "pos": "judge",
            "gender": "male"
        },
        "lotta": {
            "pos": "center",
            "gender": "female",
        },
        "gumshoe": {
            "pos": "center",
            "gender": "male"
        },
        "larry": {
            "pos": "center",
            "gender": "male"
        }
    }[character]

    pos = character_data["pos"]
    gender = character_data["gender"]

    set_position = f"<cut {pos}/>"

    start_blips = f"<startblip {gender}/>"
    stop_blips = "<stopblip/>"

    talk_sprite = get_sprite_tag(pos, character, "normal-talk") + start_blips
    idle_sprite = get_sprite_tag(pos, character, "normal-idle") + stop_blips
    return (
        f"<wait 0.03/>{talk_sprite}{set_position}"
        + f"<nametag \"{user_name}\"/><showbox/>"
        + f"{text}{idle_sprite}{END_BOX}"
    )

def get_boxes_with_pauses(user_name: str, character: str, text: str):
    boxes = get_rich_boxes(write_page(user_name, character, text))
    return boxes

pages: list[DialoguePage] = []

pages.append(DialoguePage([DialogueAction("music start cross-moderato", 0)]))
pages.extend(get_boxes_with_pauses(
    user_name="Phoenix",
    character="phoenix",
    text="Hello it is I, Phoenix Wright. I am saying some lines of text."
))
pages.extend(get_boxes_with_pauses(
    user_name="Edgeworth",
    character="edgeworth",
    text="And I am the antagonist, Edgeworth. I am also saying some lines of text. Here is a third line, because I am very serious."
))
pages.extend(get_boxes_with_pauses(
    user_name="Gumshoe",
    character="gumshoe",
    text="Hey, pal! I'm on the witness stand! Ain't that cool? Woah ho ho look at me!"
))
pages.extend(get_boxes_with_pauses(
    user_name="Judge",
    character="judge",
    text="And I'm over here, on another screen! Isn't that just the neatest thing?"
))

pages.extend(get_boxes_with_pauses(
    user_name="Lotta",
    character="lotta",
    text="Don't forget about me, m'kay? I'm still here too."
))

director = AceAttorneyDirector()
director.set_current_pages(pages)
director.render_movie(-15)
