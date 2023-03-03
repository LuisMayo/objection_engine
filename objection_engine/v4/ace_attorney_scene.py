from email.utils import localtime
from math import exp
from string import punctuation
from collections import Counter
from random import choice
from timeit import default_timer as timer
from os.path import join
from os import environ
from turtle import pos

environ["TOKENIZERS_PARALLELISM"] = "false"  # to make HF Transformers happy

from transformers import pipeline

from objection_engine.v4.loading import ASSETS_FOLDER, CHARACTERS_FOLDER
from objection_engine.beans.font_constants import NAMETAG_FONT_ARRAY, TextType

from objection_engine.v4.loading import load_character_data, load_music_data
from objection_engine.beans.comment import Comment

from .MovieKit import (
    Scene,
    SceneObject,
    ImageObject,
    MoveSceneObjectAction,
    SimpleTextObject,
    Director,
)
from .math_helpers import ease_in_out_cubic, ease_in_out_sine, lerp, remap
from PIL import Image, ImageDraw, ImageFont
from .parse_tags import (
    BaseDialogueItem,
    DialoguePage,
    DialogueTextChunk,
    DialogueAction,
    DialogueTextLineBreak,
)
from .font_tools import get_best_font, get_text_width
from .font_constants import TEXT_COLORS, FONT_ARRAY
from typing import Callable, Optional
from os.path import exists, join
from shlex import split
from math import cos, sin, pi
from random import random
from polyglot.text import Text, Sentence

try:
    from rich import print
except:
    pass


### PARALLAX EFFECT
# Distance between the benches and witness stand.
FG_PARALLAX = 155

# Width of the foreground determined by the parallax amount.
# DO NOT MODIFY!
FG_WIDTH = 256 + FG_PARALLAX + 192 + FG_PARALLAX + 256

# Left anchored, so left X should always just be zero
# DO NOT MODIFY!
FG_LEFT_X = 0

# For right bench, the X should be offset by the width (so that the right-hand
# side is aligned to the right of the background)
# DO NOT MODIFY!
FG_RIGHT_X = 1296 - (FG_WIDTH)

# For center, start at the middle then move half the width of the foreground
# DO NOT MODIFY!
FG_CENTER_X = (1296 / 2) - (FG_WIDTH / 2)

### PAN PROBABILITY
PAN_PROBABILITY_STEEPNESS = 10.0


def pan_probability(x: float) -> float:
    return 1.0 / (
        1 + exp(-PAN_PROBABILITY_STEEPNESS * x + PAN_PROBABILITY_STEEPNESS / 2.0)
    )


SENTIMENT_MODEL_PATH = "cardiffnlp/twitter-xlm-roberta-base-sentiment"

# Maximum allowed width of a line of text
MAX_WIDTH = 220

# Thanks so much to Smash Highlights on Discord for generating this LUT!
# I gave it a good few tries, but the results kept being weird...
# This one looks like it fits footage from the game perfectly, though!
PAN_LUT = [
    (0.0, 0),
    (0.06666666666666667, 0.01546750087),
    (0.13333333333333333, 0.03049086626),
    (0.2, 0.04597767736),
    (0.26666666666666666, 0.1001428958),
    (0.3333333333333333, 0.1920789403),
    (0.4, 0.2840149847),
    (0.4666666666666667, 0.3841578805),
    (0.5333333333333333, 0.4843007763),
    (0.6, 0.5839802263),
    (0.6666666666666666, 0.6841231221),
    (0.7333333333333333, 0.7842467076),
    (0.8, 0.8766461978),
    (0.8666666666666667, 0.9686015525),
    (0.9333333333333333, 0.9840690534),
    (1.0, 1),
]


def courtroom_pan_lut_ease(t: float) -> float:
    v = 0
    if t < 0:
        return 0
    elif t >= 1:
        return 1
    else:
        for i in range(0, len(PAN_LUT) - 1):
            if PAN_LUT[i][0] <= t <= PAN_LUT[i + 1][0]:
                a, b = PAN_LUT[i][1], PAN_LUT[i + 1][1]
                v = remap(PAN_LUT[i][0], PAN_LUT[i + 1][0], a, b, t)
    return v


class NameBox(SceneObject):
    def __init__(self, parent: SceneObject, pos: tuple[int, int, int]):
        super().__init__(parent, "Name Box", pos)
        self.namebox_l = ImageObject(
            parent=self,
            name="Name Box Left",
            pos=(0, 0, 11),
            filepath=join(ASSETS_FOLDER, "textbox", "nametag_left.png"),
        )
        self.namebox_c = ImageObject(
            parent=self,
            name="Name Box Center",
            pos=(1, 0, 11),
            filepath=join(ASSETS_FOLDER, "textbox", "nametag_center.png"),
        )
        self.namebox_r = ImageObject(
            parent=self,
            name="Name Box Right",
            pos=(2, 0, 11),
            filepath=join(ASSETS_FOLDER, "textbox", "nametag_right.png"),
        )
        self.namebox_text = SimpleTextObject(
            parent=self, name="Name Box Text", pos=(4, 0, 12)
        )
        self.set_text("")
        self.use_rtl = False

    def set_text(self, text: str):
        self.text = text
        self.namebox_text.text = self.text
        font_stuff = get_best_font(text, NAMETAG_FONT_ARRAY)
        self.font = ImageFont.truetype(font_stuff["path"], size=font_stuff.get("size", 12))

        text_offset = font_stuff.get("offset", {}).get(TextType.NAME, (0, 0))
        self.namebox_text.x = 4 + text_offset[0]
        self.namebox_text.y = text_offset[1]
        self.use_rtl = font_stuff.get("rtl", False)
        self.namebox_text.font = self.font

    def update(self, delta):
        length = int(self.font.getlength(self.text))
        self.namebox_c.width = length + 4
        self.namebox_r.x = 1 + length + 4

        # For RTL, move the box to the right side
        # 2 for left side of textbox
        # Width of the namebox
        # 2 for right side of namebox
        if self.use_rtl:
            self.x = 256 - (2 + self.namebox_c.width + 2)
        else:
            self.x = 0


class DialogueBox(SceneObject):
    time: float = 0

    chars_visible: int = 0
    current_char_time: float = 0.0
    max_current_char_time: float = 1 / 30

    current_wait_time: float = 0.0
    max_wait_time: float = 0.0

    def __init__(self, parent: SceneObject, director: "AceAttorneyDirector"):
        super().__init__(parent=parent, name="Dialogue Box", pos=(0, 128, 12))
        self.director = director
        self.bg = ImageObject(
            parent=self,
            name="Dialogue Box Background",
            pos=(0, 0, 10),
            filepath=join(ASSETS_FOLDER, "textbox", "mainbox.png"),
        )
        self.namebox = NameBox(parent=self, pos=(1, -11, 0))
        self.arrow = ImageObject(
            parent=self,
            name="Dialogue Box Arrow",
            pos=(256 - 15 - 5, 64 - 15 - 5, 11),
            filepath=join(ASSETS_FOLDER, "textbox", "arrow.gif"),
        )
        self.arrow.visible = False

        self.page: DialoguePage = None

        self._font_data = {}
        self.font: ImageFont.ImageFont = None
        self.use_rtl = False
        self.font_size = 16

        self.chars_visible = 0
        self.current_char_time = 0

        self.on_complete: Callable[[], None] = None

    @property
    def font_data(self) -> dict:
        return self._font_data

    @font_data.setter
    def font_data(self, value: dict):
        self._font_data = value
        self.font = ImageFont.truetype(self._font_data["path"], 16)
        self.use_rtl = self._font_data.get("rtl", False)

        if self.use_rtl:
            self.arrow.x = 7
            self.arrow.flip_x = True
        else:
            self.arrow.x = 236
            self.arrow.flip_x = False

    def render(self, img: Image.Image, ctx: ImageDraw.ImageDraw):
        if self.page is None:
            return

        x, y = self.x, self.y
        line_no = 0
        x_offset = 234 if self.use_rtl else 0
        for command in self.page.commands:
            if isinstance(command, DialogueTextLineBreak):
                line_no += 1
                x_offset = 234 if self.use_rtl else 0
            elif isinstance(command, DialogueTextChunk):
                text_str = command.text[: command.position]
                drawing_args = {
                    "xy": (
                        10 + x + x_offset,
                        5 + y + (self.font_size) * line_no,
                    ),
                    "text": text_str,
                    "fill": (255, 0, 255),
                    "anchor": ("r" if self.use_rtl else "l") + "a",
                }

                if len(command.tags) == 0:
                    drawing_args["fill"] = (255, 255, 255)
                else:
                    drawing_args["fill"] = TEXT_COLORS.get(
                        command.tags[-1], (255, 255, 255)
                    )

                if self.font is not None:
                    drawing_args["font"] = self.font

                ctx.text(**drawing_args)

                try:
                    # TODO: I think the Pillow docs say this isn't actually
                    # how you should get the true text length due to kerning,
                    # but I'm too tired right now to do it the "right" way
                    # and so far it doesn't seem to have broken significantly.
                    add_to_x_offset = ctx.textlength(text_str, font=self.font)
                except UnicodeEncodeError:
                    add_to_x_offset = self.font.getsize(text_str)[0]

                x_offset += (add_to_x_offset * -1) if self.use_rtl else add_to_x_offset


class ExclamationObject(ImageObject):
    def __init__(self, parent: SceneObject, director: "AceAttorneyDirector"):
        super().__init__(parent=parent, name="Exclamation Image", pos=(0, 0, 20))
        self.director = director

    def get_exclamation_path(self, type: str, speaker: str):
        base_name = join(ASSETS_FOLDER, CHARACTERS_FOLDER, speaker, type)
        if exists(f"{base_name}.mp3"):
            return f"{base_name}.mp3"
        elif exists(f"{base_name}.wav"):
            return f"{base_name}.wav"
        return join(ASSETS_FOLDER, "sound", "objection-generic.wav")

    def play_objection(self, speaker: str):
        self.play_exclamation("objection", speaker)

    def play_holdit(self, speaker: str):
        self.play_exclamation("holdit", speaker)

    def play_takethat(self, speaker: str):
        self.play_exclamation("takethat", speaker)

    def play_exclamation(self, type: str, speaker: str):
        self.set_filepath(
            f"assets_v4/exclamations/{type}.gif", {0.7: lambda: self.set_filepath(None)}
        )

        audio_path = self.get_exclamation_path(type, speaker)

        self.director.audio_commands.append(
            {"type": "audio", "path": audio_path, "offset": self.director.time}
        )


class EvidenceObject(ImageObject):
    EVIDENCE_POS_R = 173  # X coord of evidence box on the right
    EVIDENCE_POS_L = 13  # X coord of evidence box on the left

    def __init__(self, parent: SceneObject, director: "AceAttorneyDirector"):
        super().__init__(parent=parent, name="Evidence Image", pos=(0, 0, 18))
        self.director = director
        self.evidence_bg = ImageObject(
            parent=self,
            name="Evidence BG",
            pos=(self.EVIDENCE_POS_R, 13, 18),
            filepath=join(ASSETS_FOLDER, "evidence", "evidence-bg.png"),
        )
        self.evidence_bg.visible = False

        self.evidence_container = ImageObject(
            parent=self.evidence_bg,
            name="Evidence BG",
            pos=(3, 3, 19),
            width=64,
            height=64,
        )

    def make_media_visible(self, side: str, media_path: str):
        if side == "right":
            self.evidence_bg.x = self.EVIDENCE_POS_R
        elif side == "left":
            self.evidence_bg.x = self.EVIDENCE_POS_L

        self.evidence_bg.visible = True
        self.evidence_container.set_filepath(media_path)
        self.set_filepath(None)

    def hide_evidence(self):
        self.evidence_bg.visible = False

    def display_evidence(self, side: str, media_path: str):
        self.evidence_bg.visible = False
        self.set_filepath(
            join(ASSETS_FOLDER, "evidence", f"evidence-in-{side}.gif"),
            {0.3: lambda: self.make_media_visible(side, media_path)},
        )

        self.director.audio_commands.append(
            {
                "type": "audio",
                "path": join(ASSETS_FOLDER, "sound", "sfx-evidenceshoop.wav"),
                "offset": self.director.time,
            }
        )


class ShakerObject(SceneObject):
    magnitude: float = 0.0
    remaining: float = 0.0

    def start_shaking(self, magnitude, duration):
        self.magnitude = magnitude
        self.remaining = duration

    def update(self, delta):
        self.remaining -= delta
        if self.remaining > 0:
            angle = random() * 2 * pi
            x_offset = int(cos(angle) * self.magnitude)
            y_offset = int(sin(angle) * self.magnitude)
            self.set_x(x_offset)
            self.set_y(y_offset)
        else:
            self.remaining = 0
            self.magnitude = 0
            self.set_x(0)
            self.set_y(0)


class ColorOverlayObject(SceneObject):
    color: tuple[int, int, int] = (0, 0, 0)
    remaining: float = 0.0

    def start_color(self, color, duration):
        self.color = color
        self.remaining = duration

    def update(self, delta):
        self.remaining -= delta
        if self.remaining < 0:
            self.remaining = 0

    def render(self, img: Image.Image, ctx: ImageDraw.ImageDraw):
        if self.remaining > 0:
            ctx.rectangle(xy=(0, 0, img.width, img.height), fill=self.color)


class ActionLinesObject(ImageObject):
    def __init__(
        self,
        parent: "SceneObject" = None,
        name: str = "",
        pos: tuple[int, int, int] = ...,
        width: int = None,
        height: int = None,
        filepath: str = None,
    ):
        super().__init__(parent=parent, name=name, pos=pos, width=width, height=height, filepath=filepath)
        self.move_left = True

    def update(self, delta):
        super().update(delta)
        distance_to_move = 16

        if self.move_left:
            self.x -= distance_to_move
            while self.x < -256:
                self.x += 256
        else:
            self.x += distance_to_move
            while self.x > -256:
                self.x -= 256


class AceAttorneyDirector(Director):
    def __init__(self, callbacks: dict = None, fps: float = 30):
        super().__init__(None, fps)
        self.callbacks = {} if callbacks is None else callbacks

        self.root = SceneObject(name="Root")

        self.white_flash = ColorOverlayObject(
            parent=self.root, name="White Flash Overlay", pos=(0, 0, 30)
        )
        self.white_flash.color = (255, 255, 255)

        self.world_root = SceneObject(
            parent=self.root, name="World Root", pos=(0, 0, 0)
        )

        self.world_shaker = ShakerObject(
            parent=self.world_root, name="World Shaker", pos=(0, 0, 0)
        )

        self.judge_shot = ImageObject(
            parent=self.world_shaker,
            name="Judge Background",
            pos=(0, 256, 0),
            filepath=join(ASSETS_FOLDER, "bg", "bg_judge.png"),
        )

        self.judge = ImageObject(
            parent=self.judge_shot,
            name="Judge",
            pos=(0, 0, 1),
            width=256,
            height=192,
        )

        self.phoenix_action_lines_shot = SceneObject(
            parent=self.world_shaker,
            name="Phoenix Action Lines Container",
            pos=(0, 512, 0),
        )

        self.phoenix_action_lines_animator = ActionLinesObject(
            parent=self.phoenix_action_lines_shot,
            name="Phoenix Action Lines",
            pos=(0, 0, 0),
            filepath=join(ASSETS_FOLDER, "bg", "bg_action.png"),
        )

        self.phoenix_action_lines_character = ImageObject(
            parent=self.phoenix_action_lines_shot,
            name="Phoenix Action Lines Character",
            pos=(0, 0, 1),
            width=256,
            height=192,
        )

        self.edgeworth_action_lines_shot = SceneObject(
            parent=self.world_shaker,
            name="Edgeworth Action Lines Container",
            pos=(0, 768, 0),
        )

        self.edgeworth_action_lines_animator = ActionLinesObject(
            parent=self.edgeworth_action_lines_shot,
            name="Edgeworth Action Lines",
            pos=(0, 0, 0),
            filepath=join(ASSETS_FOLDER, "bg", "bg_action.png"),
        )
        self.edgeworth_action_lines_animator.move_left = False

        self.edgeworth_action_lines_character = ImageObject(
            parent=self.edgeworth_action_lines_shot,
            name="Edgeworth Action Lines Character",
            pos=(0, 0, 1),
            width=256,
            height=192,
        )

        self.wide_courtroom = ImageObject(
            parent=self.world_shaker,
            name="Background",
            pos=(0, 0, 0),
            filepath=join(ASSETS_FOLDER, "bg", "bg_main.png"),
        )

        self.foreground = SceneObject(
            parent=self.world_shaker,
            name="Foreground Elements",
        )

        self.left_bench = ImageObject(
            parent=self.foreground,
            name="Left Bench",
            pos=(0, 0, 2),
            filepath=join(ASSETS_FOLDER, "fg", "pr_bench.png"),
        )

        self.witness_stand = ImageObject(
            parent=self.foreground,
            name="Witness Stand",
            pos=(256 + FG_PARALLAX, 0, 2),
            width=192,
            height=192,
            filepath=join(ASSETS_FOLDER, "fg", "witness_stand.png"),
        )

        self.right_bench = ImageObject(
            parent=self.foreground,
            name="Right Bench",
            pos=(256 + FG_PARALLAX + 192 + FG_PARALLAX, 0, 2),
            flip_x=True,
            filepath=join(ASSETS_FOLDER, "fg", "pr_bench.png"),
        )

        self.phoenix = ImageObject(
            parent=self.left_bench,
            name="Left Character",
            pos=(0, 0, 1),
            width=256,
            height=192,
        )

        self.edgeworth = ImageObject(
            parent=self.right_bench,
            name="Right Character",
            pos=(0, 0, 1),
            width=256,
            height=192,
        )

        self.witness = ImageObject(
            parent=self.witness_stand,
            name="Witness",
            pos=(-31, 0, 1),
            width=256,
            height=192,
        )

        self.textbox_shaker = ShakerObject(
            parent=self.root, name="Text Box Shaker", pos=(0, 0, 0)
        )

        self.exclamation = ExclamationObject(parent=self.root, director=self)

        self.textbox = DialogueBox(parent=self.textbox_shaker, director=self)

        self.evidence = EvidenceObject(parent=self.textbox_shaker, director=self)

        self.scene = Scene(width=256, height=192, root=self.root)

        if "on_director_initialized" in self.callbacks:
            self.callbacks["on_director_initialized"]()

    def set_current_pages(self, pages: list[DialoguePage]):
        self.pages = pages
        self.page_index = 0
        self.page_start_time = timer()
        self.time_on_this_page = 0
        self.local_time = 0
        self.cur_time_for_char = 0.0

        self.current_page = self.pages[self.page_index]
        self.textbox.page = self.current_page
        self.textbox.font_data = get_best_font(
            self.current_page.get_raw_text(), FONT_ARRAY
        )

    cur_time_for_char: float = 0.0
    max_time_for_char: float = 0.03

    def update(self, delta: float):
        # Within that page, get the current object
        self.time_on_this_page += delta

        while True:
            current_dialogue_obj = self.current_page.get_current_item()
            if isinstance(current_dialogue_obj, DialogueTextChunk):
                self.cur_time_for_char += delta
                while self.cur_time_for_char > self.max_time_for_char:
                    # Increment the progress through the current dialogue object
                    # by one. This will make it render more characters in render()
                    current_dialogue_obj.position += 1
                    self.cur_time_for_char -= self.max_time_for_char
                    if current_dialogue_obj.position >= len(current_dialogue_obj.text):
                        current_dialogue_obj.completed = True
                break

            elif isinstance(current_dialogue_obj, DialogueAction):
                # Handle actions
                # Most actions can be taken care of instantly and then marked complete
                # Wait actions need the timer to fill up before they can be marked complete
                action_split = split(current_dialogue_obj.name)

                c = action_split[0]
                if c == "startblip":
                    voice_type = action_split[1]
                    self.start_voice_blips(voice_type)
                    current_dialogue_obj.completed = True

                elif c == "stopblip":
                    self.end_voice_blips()
                    current_dialogue_obj.completed = True

                elif c == "sprite":
                    position = action_split[1]
                    path = action_split[2]
                    if position == "left":
                        self.phoenix.set_filepath(path)
                    elif position == "right":
                        self.edgeworth.set_filepath(path)
                    elif position == "center":
                        self.witness.set_filepath(path)
                    elif position == "judge":
                        self.judge.set_filepath(path)
                    elif position == "leftzoom":
                        self.phoenix_action_lines_character.set_filepath(path)
                    elif position == "rightzoom":
                        self.edgeworth_action_lines_character.set_filepath(path)
                    else:
                        print(
                            f'Error in sprite command "{action_split}": unknown position "{position}"'
                        )
                    current_dialogue_obj.completed = True

                elif c == "wait":
                    duration_str = action_split[1]
                    self.cur_time_for_char += delta
                    if self.cur_time_for_char >= float(duration_str):
                        current_dialogue_obj.completed = True
                        self.cur_time_for_char = 0.0
                    else:
                        break

                elif c == "bubble":
                    exclamation_type = action_split[1]
                    character = action_split[2]
                    self.exclamation.play_exclamation(exclamation_type, character)
                    current_dialogue_obj.completed = True

                elif c == "deskslam":
                    character = action_split[1]
                    if character == "phoenix":
                        self.play_phoenix_desk_slam()
                    elif character == "edgeworth":
                        self.play_edgeworth_desk_slam()
                    current_dialogue_obj.completed = True

                elif c == "showarrow":
                    self.textbox.arrow.visible = True
                    current_dialogue_obj.completed = True

                elif c == "hidearrow":
                    self.textbox.arrow.visible = False
                    current_dialogue_obj.completed = True

                elif c == "showbox":
                    self.textbox.show()
                    current_dialogue_obj.completed = True

                elif c == "hidebox":
                    self.textbox.hide()
                    current_dialogue_obj.completed = True

                elif c == "nametag":
                    name = action_split[1]
                    self.textbox.namebox.set_text(name)
                    current_dialogue_obj.completed = True

                elif c == "evidence":
                    side = action_split[1]  # left or right or clear
                    if side == "clear":
                        self.evidence.hide_evidence()
                    else:
                        media_path = action_split[2]
                        self.evidence.display_evidence(side, media_path)
                    current_dialogue_obj.completed = True

                elif c == "sound":
                    sound_path = action_split[1]
                    self.audio_commands.append(
                        {
                            "type": "audio",
                            "path": join(
                                ASSETS_FOLDER, "sound", f"sfx-{sound_path}.wav"
                            ),
                            "offset": self.time,
                        }
                    )
                    current_dialogue_obj.completed = True

                elif c == "shake":
                    magnitude_str = action_split[1]
                    duration_str = action_split[2]

                    magnitude = float(magnitude_str)
                    duration = float(duration_str)
                    self.world_shaker.start_shaking(magnitude, duration)
                    self.textbox_shaker.start_shaking(magnitude, duration)
                    current_dialogue_obj.completed = True

                elif c == "flash":
                    duration_str = action_split[1]

                    duration = float(duration_str)
                    self.white_flash.start_color((255, 255, 255), duration)
                    current_dialogue_obj.completed = True

                elif c == "music":
                    music_command = action_split[1]

                    if music_command == "start":
                        track_name = action_split[2]
                        self.start_music_track(track_name)
                        current_dialogue_obj.completed = True
                    elif music_command == "stop":
                        self.end_music_track()
                        current_dialogue_obj.completed = True

                elif c == "cut":
                    position = action_split[1]
                    if position == "left":
                        self.cut_to_left()
                    elif position == "right":
                        self.cut_to_right()
                    elif position == "center":
                        self.cut_to_center()
                    elif position == "judge":
                        self.cut_to_judge()
                    elif position == "leftzoom":
                        self.cut_to_phoenix_action()
                    elif position == "rightzoom":
                        self.cut_to_edgeworth_action()
                    current_dialogue_obj.completed = True

                elif c == "pan":
                    position = action_split[1]
                    if position == "left":
                        self.pan_to_left()
                    elif position == "right":
                        self.pan_to_right()
                    elif position == "center":
                        self.pan_to_center()
                    current_dialogue_obj.completed = True

                elif c == "show":
                    position = action_split[1]
                    if position == "left":
                        self.left_bench.visible = True
                    elif position == "right":
                        self.right_bench.visible = True
                    elif position == "center":
                        self.witness_stand.visible = True
                    current_dialogue_obj.completed = True

                elif c == "hide":
                    position = action_split[1]
                    if position == "left":
                        self.left_bench.visible = False
                    elif position == "right":
                        self.right_bench.visible = False
                    elif position == "center":
                        self.witness_stand.visible = False
                    current_dialogue_obj.completed = True

                elif c == "nop":
                    current_dialogue_obj.completed = True

                else:
                    print(
                        f'ERROR - Unknown action encountered: "{current_dialogue_obj.name}"'
                    )
                    current_dialogue_obj.completed = True

            elif isinstance(current_dialogue_obj, DialogueTextLineBreak):
                # Does anything need to be done here? I think this can be handled
                # entirely in render()
                current_dialogue_obj.completed = True

            elif current_dialogue_obj is None:
                # Done with the current page - let's try to get the next page!
                page_end_time = timer()
                page_duration = page_end_time - self.page_start_time
                if "on_page_completed" in self.callbacks:
                    self.callbacks["on_page_completed"](
                        self.page_index,
                        len(self.pages),
                        self.current_page,
                        page_duration,
                        self.time_on_this_page,
                    )

                self.page_index += 1

                # If the current page index is greater than the number of pages, then we've
                # used all the pages - in other words, we're done.
                if self.page_index >= len(self.pages):
                    self.end_music_track()
                    self.end_voice_blips()
                    self.is_done = True

                    if "on_all_pages_completed" in self.callbacks:
                        self.callbacks["on_all_pages_completed"]()

                    return

                # Update to the next page
                self.current_page = self.pages[self.page_index]
                self.textbox.page = self.current_page
                self.textbox.font_data = get_best_font(
                    self.current_page.get_raw_text(), FONT_ARRAY
                )
                self.page_start_time = timer()
                self.time_on_this_page = 0

    def pan_to_right(self):
        self.sequencer.run_action(
            MoveSceneObjectAction(
                target_value=(-1296 + 256, 0),
                duration=0.5,
                scene_object=self.world_root,
                ease_function=courtroom_pan_lut_ease,
            )
        )

        self.sequencer.run_action(
            MoveSceneObjectAction(
                target_value=(FG_RIGHT_X, 0),
                duration=0.5,
                scene_object=self.foreground,
                ease_function=courtroom_pan_lut_ease,
            )
        )

    def pan_to_left(self):
        self.sequencer.run_action(
            MoveSceneObjectAction(
                target_value=(0, 0),
                duration=0.5,
                scene_object=self.world_root,
                ease_function=courtroom_pan_lut_ease,
            )
        )

        self.sequencer.run_action(
            MoveSceneObjectAction(
                target_value=(FG_LEFT_X, 0),
                duration=0.5,
                scene_object=self.foreground,
                ease_function=courtroom_pan_lut_ease,
            )
        )

    def pan_to_center(self):
        self.sequencer.run_action(
            MoveSceneObjectAction(
                target_value=(-(1296 / 2) + (256 / 2), 0),
                duration=0.5,
                scene_object=self.world_root,
                ease_function=courtroom_pan_lut_ease,
            )
        )

        self.sequencer.run_action(
            MoveSceneObjectAction(
                target_value=(FG_CENTER_X, 0),
                duration=0.5,
                scene_object=self.foreground,
                ease_function=courtroom_pan_lut_ease,
            )
        )

    def cut_to_left(self):
        self.world_root.set_x(0)
        self.world_root.set_y(0)
        self.foreground.set_x(FG_LEFT_X)

    def cut_to_right(self):
        self.world_root.set_x(-1296 + 256)
        self.world_root.set_y(0)
        self.foreground.set_x(FG_RIGHT_X)

    def cut_to_center(self):
        self.world_root.set_x(-(1296 / 2) + (256 / 2))
        self.world_root.set_y(0)
        self.foreground.set_x(FG_CENTER_X)

    def cut_to_judge(self):
        self.world_root.set_x(0)
        self.world_root.set_y(-256)

    def cut_to_phoenix_action(self):
        self.world_root.set_x(0)
        self.world_root.set_y(-512)

    def cut_to_edgeworth_action(self):
        self.world_root.set_x(0)
        self.world_root.set_y(-768)

    current_music_track: Optional[dict] = None
    current_voice_blips: Optional[dict] = None

    def start_music_track(self, name: str):
        self.end_music_track()
        self.current_music_track = {
            "type": "audio",
            "path": join(ASSETS_FOLDER, "music", f"{name}.mp3"),
            "offset": self.time,
            "loop_type": "loop_until_truncated",
        }
        self.audio_commands.append(self.current_music_track)

    def end_music_track(self):
        if self.current_music_track is not None:
            self.current_music_track["end"] = self.time
            self.current_music_track = None

    def start_voice_blips(self, gender: str):
        self.end_voice_blips()
        self.current_voice_blips = {
            "type": "audio",
            "path": join(ASSETS_FOLDER, "sound", f"sfx-blip{gender}.wav"),
            "offset": self.time,
            "loop_delay": 0.06,
            "loop_type": "loop_complete_only",
        }
        self.audio_commands.append(self.current_voice_blips)

    def end_voice_blips(self):
        if self.current_voice_blips is not None:
            self.current_voice_blips["end"] = self.time
            self.current_voice_blips = None

    def next_dialogue_sound(self):
        self.audio_commands.append(
            {
                "type": "audio",
                "path": join(ASSETS_FOLDER, "sound", "sfx-pichoop.wav"),
                "offset": self.time,
            }
        )

    def play_phoenix_desk_slam(self):
        fp_before = self.phoenix.filepath
        cb_before = self.phoenix.callbacks
        self.phoenix.set_filepath(
            get_sprite_location("phoenix", "deskslam"),
            {0.8: lambda: self.phoenix.set_filepath(fp_before, cb_before)},
        )
        self.audio_commands.append(
            {
                "type": "audio",
                "path": join(ASSETS_FOLDER, "sound", "sfx-deskslam.wav"),
                "offset": self.time + 0.15,
            }
        )

    def play_edgeworth_desk_slam(self):
        fp_before = self.edgeworth.filepath
        cb_before = self.edgeworth.callbacks
        self.edgeworth.set_filepath(
            get_sprite_location("edgeworth", "deskslam"),
            {0.8: lambda: self.edgeworth.set_filepath(fp_before, cb_before)},
        )
        self.audio_commands.append(
            {
                "type": "audio",
                "path": join(ASSETS_FOLDER, "sound", "sfx-deskslam.wav"),
                "offset": self.time + 0.25,
            }
        )


def get_sprite_location(character: str, emotion: str):
    return join(
        ASSETS_FOLDER, CHARACTERS_FOLDER, character, f"{character}-{emotion}.gif"
    )


def get_sprite_tag(location: str, character: str, emotion: str):
    return f"<sprite {location} {get_sprite_location(character, emotion)}/>"


class DialogueBoxBuilder:
    def __init__(self, callbacks: dict = None, verify_sprites: bool = False) -> None:
        self.character_data = load_character_data(verify_sprites=verify_sprites)
        self.music_data = load_music_data()
        self.current_character_name: str = None
        self.current_character_animation: str = None
        self.previous_character_name: str = None

        #
        self.pan_probability_in: float = 1.0

        self.has_gone_to_tense_music: bool = False
        self.callbacks = {} if callbacks is None else callbacks

        # Hugging Face sentiment analyzer
        self.get_sentiment = pipeline(
            "sentiment-analysis",
            model=SENTIMENT_MODEL_PATH,
            tokenizer=SENTIMENT_MODEL_PATH,
        )

    def reload_character_data(self, verify_sprites: bool = False):
        self.character_data = load_character_data(verify_sprites=verify_sprites)

    def initialize_box(
        self,
        user_name: str,
        do_objection: bool = False,
        go_to_tense_music: bool = False,
        text: str = None,
    ) -> DialoguePage:
        this_char_data = self.character_data["characters"][self.current_character_name]
        location = this_char_data["location"]
        gender = this_char_data["gender"]

        actions: list[BaseDialogueItem] = []

        if do_objection:
            actions.extend(
                [
                    DialogueAction("hidebox", 0),
                    DialogueAction(
                        f"bubble objection {self.current_character_name}", 0
                    ),
                    DialogueAction(f"wait 0.1", 0),
                    DialogueAction("music stop", 0) if go_to_tense_music else None,
                    DialogueAction(f"wait 1.2", 0),
                    DialogueAction(f"music start {self.tense_track}", 0)
                    if go_to_tense_music
                    else None,
                ]
            )

        if go_to_tense_music:
            self.has_gone_to_tense_music = True

        actions.extend(
            [
                DialogueAction("wait 0.03", 0),
            ]
        )

        previous_location = (
            self.character_data["characters"]
            .get(self.previous_character_name, {})
            .get("location", None)
        )
        pannable_locations = ["left", "center", "right"]
        can_pan = (
            (location in pannable_locations)
            and (previous_location in pannable_locations)
            and (location != previous_location)
        )
        PAN_TIME = 0.5
        SWITCH_SPRITE_TIME = 0.18
        move_cam_actions = []
        if can_pan and random() < pan_probability(self.pan_probability_in):
            self.pan_probability_in -= 0.5
            panning_across_whole_courtroom = (
                location == "left" and previous_location == "right"
            ) or (location == "right" and previous_location == "left")

            if panning_across_whole_courtroom:
                move_cam_actions.extend(
                    [
                        DialogueAction("hidebox", 0),
                        DialogueAction("wait 0.25", 0),
                        DialogueAction("hide center", 0),
                        DialogueAction(f"pan {location}", 0),
                        DialogueAction(
                            f"sprite {location} {get_sprite_location(self.current_character_name, f'{self.current_character_animation}-idle')}",
                            0,
                        ),
                        DialogueAction(f"wait 0.14", 0),
                        DialogueAction("hide left", 0),
                        DialogueAction("hide right", 0),
                        DialogueAction(f"wait 0.26", 0),
                        DialogueAction("show left", 0),
                        DialogueAction("show right", 0),
                        DialogueAction("wait 0.1", 0),
                        DialogueAction(f"wait 0.1", 0),
                        DialogueAction("show center", 0),
                    ]
                )

            # Panning to the witness
            elif location == "center":
                move_cam_actions.extend(
                    [
                        DialogueAction("hidebox", 0),
                        DialogueAction("wait 0.25", 0),
                        DialogueAction(f"pan {location}", 0),
                        DialogueAction(
                            f"sprite {location} {get_sprite_location(self.current_character_name, f'{self.current_character_animation}-idle')}",
                            0,
                        ),
                        DialogueAction(f"wait {SWITCH_SPRITE_TIME}", 0),
                        DialogueAction("hide left", 0),
                        DialogueAction("hide right", 0),
                        DialogueAction("show center", 0),
                        DialogueAction(f"wait {PAN_TIME - SWITCH_SPRITE_TIME}", 0),
                        DialogueAction("show left", 0),
                        DialogueAction("show right", 0),
                        DialogueAction(f"wait 0.1", 0),
                    ]
                )

            # Panning to the defense or prosecution from the witness
            else:
                move_cam_actions.extend(
                    [
                        DialogueAction("hidebox", 0),
                        DialogueAction("wait 0.25", 0),
                        DialogueAction(f"pan {location}", 0),
                        DialogueAction(
                            f"sprite {location} {get_sprite_location(self.current_character_name, f'{self.current_character_animation}-idle')}",
                            0,
                        ),
                        DialogueAction(f"wait {SWITCH_SPRITE_TIME}", 0),
                        DialogueAction("show left", 0),
                        DialogueAction("show right", 0),
                        DialogueAction("hide center", 0),
                        DialogueAction(f"wait {1 - SWITCH_SPRITE_TIME}", 0),
                        DialogueAction("show center", 0),
                        DialogueAction(f"wait 0.1", 0),
                    ]
                )

        else:
            if location == previous_location:
                self.pan_probability_in += 0.2
            else:
                self.pan_probability_in += 0.1

            # Prevents one person talking a bunch at the beginning
            # from making it pan constantly later on
            self.pan_probability_in = min(self.pan_probability_in, 1.0)

            move_cam_actions.extend(
                [
                    DialogueAction(
                        f"sprite {location} {get_sprite_location(self.current_character_name, f'{self.current_character_animation}-idle')}",
                        0,
                    ),
                    DialogueAction(f"cut {location}", 0),
                ]
            )

        actions.extend(move_cam_actions)
        actions.extend(
            [
                DialogueAction(f'nametag "{user_name}"', 0),
                DialogueAction("showbox", 0),
            ]
        )

        self.previous_character_name = self.current_character_name

        return DialoguePage(actions)

    def finish_box(self, page: DialoguePage):
        this_char_data = self.character_data["characters"][self.current_character_name]
        pos = this_char_data["location"]

        page.commands.extend(
            [
                DialogueAction(
                    f"sprite {pos} {get_sprite_location(self.current_character_name, f'{self.current_character_animation}-idle')}",
                    0,
                ),
                DialogueAction(f"stopblip", 0),
                DialogueAction("showarrow", 0),
                DialogueAction("wait 2", 0),
                DialogueAction("hidearrow", 0),
                DialogueAction("sound pichoop", 0),
                DialogueAction("wait 0.3", 0),
            ]
        )

    def get_characters_for_users(
        self,
        common: Counter,
        assigned_characters: dict = None,
        adult_mode: bool = False,
    ):
        users_to_characters = (
            {} if assigned_characters is None else assigned_characters.copy()
        )
        most_common = [t[0] for t in common.most_common()]

        high_priority_character_names = self.character_data["high_priority"]
        character_names = [
            name
            for name in self.character_data["characters"]
            if not adult_mode
            or (adult_mode and name not in self.character_data["omit_for_adult_mode"])
        ]
        rnd_character_names = [
            name
            for name in character_names
            if name not in high_priority_character_names
        ]

        # Assign high priority characters first
        i: int = 0
        for name in high_priority_character_names:
            try:
                if (
                    name not in users_to_characters.values()
                    and most_common[i] not in users_to_characters
                ):
                    users_to_characters[most_common[i]] = name
            except IndexError:
                pass
            i += 1

        # Everyone else is chosen at random
        rnd_characters = [
            c for c in rnd_character_names if c not in users_to_characters.values()
        ]
        for user_id in most_common:
            # Skip users who were manually assigned characters
            if user_id in users_to_characters:
                continue

            # Reload choosable characters if we ran out
            if len(rnd_characters) == 0:
                rnd_characters = rnd_character_names.copy()

            # Assign a character randomly chosen from the list to this user,
            # and remove them from the pool
            rnd_character = choice(rnd_characters)
            rnd_characters.remove(rnd_character)
            users_to_characters[user_id] = rnd_character

        return users_to_characters

    def build_from_comments(
        self,
        comments: list[Comment],
        music_code: str = "pwr",
        assigned_characters: dict = None,
        adult_mode: bool = False,
        avoid_spoiler_sprites: bool = False,
    ):
        self.avoid_spoiler_sprites = avoid_spoiler_sprites

        # Do character check
        counter = Counter()
        for comment in comments:
            counter.update({comment.effective_user_id: 1})
        users_to_characters = self.get_characters_for_users(
            counter,
            assigned_characters=assigned_characters,
            adult_mode=adult_mode,
        )

        if "on_characters_cast" in self.callbacks:
            self.callbacks["on_characters_cast"](users_to_characters)

        # Get music
        if music_code in self.music_data:
            music_pack = self.music_data[music_code]
        else:
            raise KeyError(
                f'Music code "{music_code}" not found. Ensure that a folder for it exists in the "music" folder, and that it has a "config.toml" file.'
            )

        self.pages: list[DialoguePage] = []

        # Start relaxed music
        self.relaxed_track = join(music_code, choice(music_pack["relaxed"]))
        self.tense_track = join(music_code, choice(music_pack["tense"]))
        self.pages.append(
            DialoguePage([DialogueAction(f"music start {self.relaxed_track}", 0)])
        )

        self.has_done_objection = False

        # Add boxes for the dialogue
        for i, comment in enumerate(comments):
            self.pages.extend(
                self.get_boxes_with_pauses(
                    user_name=comment.user_name,
                    character=users_to_characters[comment.effective_user_id],
                    text=comment.text_content,
                    evidence_path=comment.evidence_path,
                )
            )

            if "on_comment_processed" in self.callbacks:
                self.callbacks["on_comment_processed"](i, len(comments), comment)

    def update_pose_for_sentence(self, sentence: Sentence, sprites: list[str]):
        sentiment: dict = self.get_sentiment(sentence.raw)[0]
        try:
            sprite_cat = sentiment.get("label", "neutral")
        except IndexError:
            sprite_cat = "neutral"

        self.current_character_animation = choice(
            [
                s
                for s in sprites[sprite_cat]
                if not self.avoid_spoiler_sprites
                or "spoiler" not in sprites
                or (self.avoid_spoiler_sprites and s not in sprites["spoiler"])
            ]
        )

    def get_boxes_with_pauses(
        self, user_name: str, character: str, text: str, evidence_path: str = None
    ):
        self.current_character_name = character
        this_char_data = self.character_data["characters"][character]
        location = this_char_data["location"]
        gender = this_char_data["gender"]
        sprites = this_char_data["sprites"]

        # Split text into sentences
        pg_text = Text(text)
        sentences: list[Sentence] = pg_text.sentences

        # Determine if this should have an objection
        text_polarity_data = self.get_sentiment(pg_text.raw)[0]
        polarity_type = text_polarity_data["label"]
        polarity_confidence = text_polarity_data["score"]

        do_objection = (
            (polarity_type == "negative" or (polarity_type == "positive" and random() > 0.7))
            and polarity_confidence > 0.5
            and not self.has_done_objection
        )
        go_to_tense_music = do_objection and not self.has_gone_to_tense_music
        # Stuff at beginning of text box
        all_pages: list[DialoguePage] = []

        self.update_pose_for_sentence(sentences[0], sprites)
        current_page = self.initialize_box(
            user_name, do_objection, go_to_tense_music, text=text
        )

        current_page.commands.append(DialogueAction("evidence clear", 0))
        if evidence_path is not None:
            current_page.commands.append(
                DialogueAction(
                    f"evidence {'left' if location == 'right' else 'right'} \"{evidence_path}\"",
                    0,
                )
            )

        # Add actual content of text box
        current_line_index = 0
        current_line_width = 0

        sentence_index = 0
        word_index = 0

        # Get the font for this text
        best_font = get_best_font(text, FONT_ARRAY)

        space_width = get_text_width(" ", font=best_font)

        sentences_in_this_box = 0
        for sentence_index, sentence in enumerate(sentences):
            # Get the sentence sentiment here

            # We don't want to
            if sentence_index > 0:
                self.update_pose_for_sentence(sentence, sprites)

            # Start animating the speaking and blips
            current_page.commands.extend(
                [
                    DialogueAction(f"startblip {gender}", 0),
                    DialogueAction(
                        f"sprite {location} {get_sprite_location(self.current_character_name, f'{self.current_character_animation}-talk')}",
                        0,
                    ),
                ]
            )

            # try:
            #     pos_tags = sentence.pos_tags
            # except ValueError:
            #     pos_tags = [(word, None) for word in sentence.words]

            pos_tags = [(word, None) for word in sentence.split()]

            for word_index, (word, pos) in enumerate(pos_tags):
                word_width = get_text_width(word, font=best_font)

                # Line break if this word is too wide to fit
                if current_line_width + word_width > MAX_WIDTH:
                    current_line_width = 0
                    if current_line_index < 2:
                        # Go to next line down
                        current_page.commands.append(DialogueTextLineBreak())
                        current_line_index += 1

                    else:
                        # This page is full, so create a new page
                        self.finish_box(current_page)
                        all_pages.append(current_page)
                        current_page = self.initialize_box(user_name, text=text)
                        current_page.commands.extend(
                            [
                                DialogueAction(f"startblip {gender}", 0),
                                DialogueAction(
                                    f"sprite {location} {get_sprite_location(self.current_character_name, f'{self.current_character_animation}-talk')}",
                                    0,
                                ),
                            ]
                        )
                        current_line_index = 0
                        sentences_in_this_box = 0

                # Should this be highlighted?
                # Add this word to current line
                tags: list[str] = []
                if pos == "PROPN" and random() > 0.5:
                    tags.append("red")
                current_page.commands.append(DialogueTextChunk(word, tags))
                current_line_width += word_width

                # If the current word is punctuation (not sentence end), then add a very short pause
                if word[-1] in ",-":
                    current_page.commands.extend(
                        [
                            DialogueAction(f"stopblip", 0),
                            DialogueAction(
                                f"sprite {location} {get_sprite_location(self.current_character_name, f'{self.current_character_animation}-idle')}",
                                0,
                            ),
                            DialogueAction("wait 0.3", 0),
                            DialogueAction(f"startblip {gender}", 0),
                            DialogueAction(
                                f"sprite {location} {get_sprite_location(self.current_character_name, f'{self.current_character_animation}-talk')}",
                                0,
                            ),
                        ]
                    )

                # If the next word is not the last word in the sentence, then
                # add a space after it
                if word_index != len(sentence.words) - 1:
                    current_page.commands.append(DialogueTextChunk(" ", []))
                    current_line_width += space_width

            sentences_in_this_box += 1
            if sentences_in_this_box < 2:
                # In between each sentence, pause and change the sprite
                current_page.commands.extend(
                    [
                        DialogueAction(f"stopblip", 0),
                        # DialogueTextChunk(" ", []),
                        DialogueAction(
                            f"sprite {location} {get_sprite_location(self.current_character_name, f'{self.current_character_animation}-idle')}",
                            0,
                        ),
                    ]
                )
                current_line_width += space_width

                # We only want to have a delay if this isn't the last sentence
                # in the box (otherwise there'll be a weird delay between the text
                # showing up and the "next page" arrow showing up.)
                if sentence_index != len(sentences) - 1:
                    current_page.commands.append(
                        DialogueAction("wait 0.6", 0),
                    )

            elif sentence_index != len(sentences) - 1:
                # There are two sentences in this box, so end this box and
                # start a new one
                self.finish_box(current_page)
                all_pages.append(current_page)
                current_page = self.initialize_box(user_name, text=text)
                current_line_index = 0
                current_line_width = 0
                sentences_in_this_box = 0

        self.finish_box(current_page)
        all_pages.append(current_page)

        return all_pages

    def render(
        self,
        comments: list[Comment],
        output_filename: str = None,
        music_code: str = "pwr",
        assigned_characters: dict = None,
        adult_mode: bool = False,
        avoid_spoiler_sprites: bool = False,
        volume: int = -15,
        resolution_scale: float = 1.0,
    ):
        self.build_from_comments(
            comments,
            music_code=music_code,
            assigned_characters=assigned_characters,
            adult_mode=adult_mode,
            avoid_spoiler_sprites=avoid_spoiler_sprites,
        )
        director = AceAttorneyDirector(callbacks=self.callbacks)
        director.set_current_pages(self.pages)
        director.render_movie(
            output_filename=output_filename,
            volume_adjustment=volume,
            resolution_scale=resolution_scale,
        )
