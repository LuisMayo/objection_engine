from math import ceil

from objection_engine.parse_tags import get_rich_boxes
from .beans.comment_bridge import CommentBridge
from PIL import Image, ImageDraw, ImageFont , ImageFile
from matplotlib.pyplot import imshow
import numpy as np
import cv2
from typing import List, Dict, Union
import random
import os
import json
import shutil
import random as r
from pydub import AudioSegment
import moviepy.editor as mpe
from enum import IntEnum
import ffmpeg
from collections import Counter
import random
from textwrap import wrap
import spacy
from .polarity_analysis import Analizer
analizer = Analizer()
from .beans.img import AnimImg
from .beans.text import AnimText, TextType
from .beans.scene import AnimScene
from .beans.video import AnimVideo
from .constants import Character, lag_frames, fps
from . import constants
import re

def create_nameplate(obj: dict):
    """
    Creates the layers for a nameplate that
    resizes to fit the user's name.
    """
    if "name" not in obj: return []
    character_name = AnimText(
        obj["name"],
        text_type=TextType.NAME,
        font_size = 8,
        x = 6,
        y = 129 - 11,
        force_no_rtl=True
    )

    name_width = character_name.get_text_size()[0]

    namebox_l = AnimImg(
        "assets/textbox/nametag_left.png",
        x = 1,
        y = 129 - 12
    )

    namebox_c = AnimImg(
        "assets/textbox/nametag_center.png",
        x = 3,
        y = 129-12,
        w = name_width + 6,
        h = 14
    )

    namebox_r = AnimImg(
        "assets/textbox/nametag_right.png",
        x = 3 + name_width + 6,
        y = 129 - 12
    )

    # If the text of the text box is RTL, then move
    # the nameplate to the right side of the screen
    if obj["text"].use_rtl():
        namebox_l.x = 256 - namebox_r.w - name_width - 6
        namebox_c.x = 256 - namebox_r.w - name_width - 3
        namebox_r.x = 256 - namebox_r.w
        character_name.x = namebox_l.x + 5

    if obj.get("action") == constants.Action.TEXT_SHAKE_EFFECT:
        namebox_l.shake_effect = True
        namebox_c.shake_effect = True
        namebox_r.shake_effect = True

    return [namebox_l, namebox_c, namebox_r, character_name]

def do_video(config: List[Dict], output_filename, resolution_scale):
    """
    Renders the video, and returns a list of sound effects that can be used to
    render the sound for the video.
    """
    scenes = []
    sound_effects = []
    part = 0
    for scene in config:
        # We pick up the images to be rendered
        bg = AnimImg(constants.location_map[scene["location"]])
        arrow = AnimImg("assets/arrow.gif", x=235, y=170, w=15, h=15)
        textbox = AnimImg("assets/textbox/mainbox.png", x=1, y=129, w=bg.w-2)
        objection = AnimImg("assets/objection.gif")
        bench = None

        # constants.Location needs a more in-depth chose
        if scene["location"] == constants.Location.COURTROOM_LEFT:
            bench = AnimImg("assets/logo-left.png")
        elif scene["location"] == constants.Location.COURTROOM_RIGHT:
            bench = AnimImg("assets/logo-right.png")
        elif scene["location"] == constants.Location.WITNESS_STAND:
            bench = AnimImg("assets/witness_stand.png", w=bg.w)
            bench.y = bg.h - bench.h

        if "audio" in scene:
            sound_effects.append({"_type": "bg", "src": f'assets/{scene["audio"]}.mp3'})

        current_frame = 0
        current_character_name = None
        current_character_gender = "male"
        text = None
        for obj in scene["scene"]:
            if "text" in obj and obj["text"].use_rtl():
                arrow.x = 7
                arrow.flip_x = True
            else:
                arrow.x = 235
                arrow.flip_x = False
            # First we check for evidences
            if "evidence" in obj and obj['evidence'] is not None:
                if scene["location"] == constants.Location.COURTROOM_RIGHT:
                    evidence = AnimImg(obj["evidence"], x=26, y=19, w=85, maxh=75)
                else:
                    evidence = AnimImg(obj["evidence"], x=145, y=19, w=85, maxh=75)
            else:
                evidence = None
            
            # Next, find the current character's sprite
            if "character" in obj:
                _dir = constants.character_map[obj["character"]]
                current_character_name = obj["character"]
                current_character_gender = constants.character_gender_map[obj["character"]]
                default = "normal" if "emotion" not in obj else obj["emotion"]
                default_path = (
                    f"{_dir}/{current_character_name.lower()}-{default}(a).gif"
                )
                if not os.path.isfile(default_path):
                    default_path = (
                        f"{_dir}/{current_character_name.lower()}-{default}.gif"
                    )
                if not os.path.isfile(default_path):
                    default_path = (
                        f"{_dir}/{current_character_name.lower()}-normal(a).gif"
                    )
                assert os.path.isfile(default_path), f"{default_path} does not exist"

                default_character = AnimImg(default_path, half_speed=True)
                if "(a)" in default_path:
                    talking_character = AnimImg(
                        default_path.replace("(a)", "(b)"), half_speed=True
                    )
                else:
                    talking_character = AnimImg(default_path, half_speed=True)

            if "emotion" in obj:
                default = obj["emotion"]
                default_path = (
                    f"{_dir}/{current_character_name.lower()}-{default}(a).gif"
                )
                if not os.path.isfile(default_path):
                    default_path = (
                        f"{_dir}/{current_character_name.lower()}-{default}.gif"
                    )
                if not os.path.isfile(default_path):
                    default_path = (
                        f"{_dir}/{current_character_name.lower()}-normal(a).gif"
                    )
                assert os.path.isfile(default_path), f"{default_path} does not exist"

                default_character = AnimImg(default_path, half_speed=True)
                if "(a)" in default_path:
                    talking_character = AnimImg(
                        default_path.replace("(a)", "(b)"), half_speed=True
                    )
                else:
                    talking_character = AnimImg(default_path, half_speed=True)

            # Handle case of character onscreen speaking with text
            if "action" in obj and (
                obj["action"] == constants.Action.TEXT
                or obj["action"] == constants.Action.TEXT_SHAKE_EFFECT
            ):
                character = talking_character
                splitter_font_path = AnimText(obj["text"]).font_path
                _text = obj["text"]
                _colour = None if "colour" not in obj else obj["colour"]
                text = AnimText(
                    _text,
                    font_size=15,
                    x=11,
                    y=134,
                    typewriter_effect=True,
                    colour=_colour,
                )
                num_frames = len(_text) + lag_frames

                # Apply shake effect to the scene if desired
                if obj["action"] == constants.Action.TEXT_SHAKE_EFFECT:
                    bg.shake_effect = True
                    character.shake_effect = True
                    if bench is not None:
                        bench.shake_effect = True
                    textbox.shake_effect = True

                scene_objs = list(
                    filter(
                        lambda x: x is not None,
                        [
                            bg,
                            character,
                            bench,
                            textbox
                        ]
                        + create_nameplate(obj) +
                        [
                            text,
                            evidence
                        ]
                    )
                )
                scenes.append(
                    AnimScene(scene_objs, len(_text) - 1, start_frame=current_frame)
                )
                sound_effects.append({"_type": "bip", "length": len(_text) - 1, "gender": current_character_gender})

                # Reset shake effect
                if obj["action"] == constants.Action.TEXT_SHAKE_EFFECT:
                    bg.shake_effect = False
                    character.shake_effect = False
                    if bench is not None:
                        bench.shake_effect = False
                    textbox.shake_effect = False

                # Append period of time after typewriter effect finishes, where the "next dialogue"
                # arrow is visible
                text.typewriter_effect = False
                character = default_character
                scene_objs = list(
                    filter(
                        lambda x: x is not None,
                        [bg, character, bench, textbox] + create_nameplate(obj) + [text, arrow, evidence],
                    )
                )
                scenes.append(
                    AnimScene(scene_objs, lag_frames, start_frame=len(_text) - 1)
                )
                current_frame += num_frames
                sound_effects.append({"_type": "silence", "length": lag_frames})
            
            # Handle case of shake effect without text
            elif "action" in obj and obj["action"] == constants.Action.SHAKE_EFFECT:
                bg.shake_effect = True
                character.shake_effect = True
                if bench is not None:
                    bench.shake_effect = True
                textbox.shake_effect = True
                character = default_character
                if text is not None:
                    scene_objs = list(
                        filter(
                            lambda x: x is not None,
                            [
                                bg,
                                character,
                                bench,
                                textbox
                            ]
                            + create_nameplate(obj) +
                            [
                                text,
                                arrow,
                                evidence,
                            ],
                        )
                    )
                else:
                    scene_objs = [bg, character, bench]

                scenes.append(
                    AnimScene(scene_objs, lag_frames, start_frame=current_frame)
                )
                sound_effects.append({"_type": "shock", "length": lag_frames})
                current_frame += lag_frames
                bg.shake_effect = False
                character.shake_effect = False
                if bench is not None:
                    bench.shake_effect = False
                textbox.shake_effect = False

            # Handle case of Objection bubble
            elif "action" in obj and obj["action"] == constants.Action.OBJECTION:
                # Add the "Objection!" bubble on top of the current background and character
                objection.shake_effect = True
                character = default_character
                scene_objs = list(
                    filter(lambda x: x is not None, [bg, character, bench, objection])
                )
                scenes.append(AnimScene(scene_objs, 11, start_frame=current_frame))

                # For a short period of time after the bubble disappears, continue to display
                # the background and character(?)
                bg.shake_effect = False
                if bench is not None:
                    bench.shake_effect = False
                character.shake_effect = False
                scene_objs = list(
                    filter(lambda x: x is not None, [bg, character, bench])
                )
                scenes.append(AnimScene(scene_objs, 11, start_frame=current_frame))
                sound_effects.append(
                    {
                        "_type": "objection",
                        "character": current_character_name.lower(),
                        "length": 22,
                    }
                )
                current_frame += 11

            # Handle case of presenting evidence without any dialogue(?)
            else:
                character = default_character
                scene_objs = list(
                    filter(lambda x: x is not None, [bg, character, bench, evidence])
                )
                _length = lag_frames
                if "length" in obj:
                    _length = obj["length"]
                if "repeat" in obj:
                    character.repeat = obj["repeat"]
                scenes.append(AnimScene(scene_objs, _length, start_frame=current_frame))
                character.repeat = True
                sound_effects.append({"_type": "silence", "length": _length})
                current_frame += _length

            if (len(scenes) > 50):
                video = AnimVideo(scenes, fps=fps, resolution_scale=resolution_scale)
                video.render(output_filename + '/' +str(part) + '.mp4')
                part+=1
                scenes = []

    if (len(scenes) > 0):
        video = AnimVideo(scenes, fps=fps, resolution_scale=resolution_scale)
        video.render(output_filename + '/' +str(part) + '.mp4')
    return sound_effects

def do_audio(sound_effects: List[Dict], output_filename):
    """
    Renders the sound for the video given the data outputted by do_video().
    """
    # Track containing sound effects
    audio_se = AudioSegment.empty()

    # Character speech sound effect
    male_bip = AudioSegment.from_wav("assets/sfx general/sfx-blipmale.wav") + AudioSegment.silent(duration=50)
    long_male_bip = male_bip * 100
    long_male_bip -= 10

    female_bip = AudioSegment.from_wav("assets/sfx general/sfx-blipfemale.wav") + AudioSegment.silent(duration=50)
    long_female_bip = female_bip * 100
    long_female_bip -= 10

    # "Next dialogue" sound effect
    blink = AudioSegment.from_wav("assets/sfx general/sfx-pichoop.wav")
    blink -= 10

    # Shock sound effect
    badum = AudioSegment.from_wav("assets/sfx general/sfx-fwashing.wav")

    # "Objection!" sound effects for characters with voiced objections
    pheonix_objection = AudioSegment.from_mp3("assets/Phoenix - objection.mp3")
    edgeworth_objection = AudioSegment.from_mp3("assets/Edgeworth - (English) objection.mp3")
    payne_objection = AudioSegment.from_mp3("assets/Payne - Objection.mp3")
    default_objection = AudioSegment.from_mp3("assets/sfx general/sfx-objection.wav")

    spf = 1 / fps * 1000
    for obj in sound_effects:
        if obj["_type"] == "silence":
            audio_se += AudioSegment.silent(duration=int(obj["length"] * spf))
        elif obj["_type"] == "bip":
            if obj["gender"] == "female":
                audio_se += blink + long_female_bip[: max(int(obj["length"] * spf - len(blink)), 0)]
            else:
                audio_se += blink + long_male_bip[: max(int(obj["length"] * spf - len(blink)), 0)]
        elif obj["_type"] == "objection":
            if obj["character"] == "phoenix":
                audio_se += pheonix_objection[: int(obj["length"] * spf)]
            elif obj["character"] == "edgeworth":
                audio_se += edgeworth_objection[: int(obj["length"] * spf)]
            elif obj["character"] == "payne":
                audio_se += payne_objection[: int(obj["length"] * spf)]
            else:
                audio_se += default_objection[: int(obj["length"] * spf)]
        elif obj["_type"] == "shock":
            audio_se += badum[: int(obj["length"] * spf)]

    # Assemble the background music information
    music_tracks = []
    len_counter = 0
    for obj in sound_effects:
        if obj["_type"] == "bg":
            if len(music_tracks) > 0:
                music_tracks[-1]["length"] = len_counter
                len_counter = 0
            music_tracks.append({"src": obj["src"]})
        else:
            len_counter += obj["length"]
    if len(music_tracks) > 0:
        music_tracks[-1]["length"] = len_counter

    # Track containing the background music
    music_se = AudioSegment.empty()
    for track in music_tracks:
        loaded_audio = AudioSegment.from_mp3(track["src"])
        # Total mp3 length in seconds
        music_file_len = len(loaded_audio) / 1000
        # Needed length, in seconds
        needed_len = track["length"] / fps
        if needed_len > music_file_len:
            loaded_audio *= ceil(needed_len / music_file_len)
        music_se += loaded_audio[:int(needed_len * 1000)]

    final_se = music_se.overlay(audio_se)
    final_se.export(output_filename, format="adts")

def ace_attorney_anim(config: List[Dict], output_filename: str = "output.mp4", resolution_scale: int = 1):
    """
    Render the Ace Attorney sequence provided by `config` to the file named `output_filename`.
    """
    # Set up the filenames for the output files
    root_filename = output_filename[:-4]
    audio_filename = output_filename + '.audio.aac'
    text_filename = root_filename + '.txt'
    if os.path.exists(root_filename):
        shutil.rmtree(root_filename)
    os.mkdir(root_filename)

    # Render the video clips, and get the sound information.
    sound_effects = do_video(config, root_filename, resolution_scale)

    # Using the sound information, render the audio.
    do_audio(sound_effects, audio_filename)

    # Compile all of the rendered videos and audio into a single video file.
    videos = []
    with open(text_filename, 'w') as txt:
        for file in os.listdir(root_filename):
            videos.append(file)
        videos.sort(key=lambda item : int(item[:-4]))
        for video in videos:
            txt.write('file ' + root_filename + '/' +video + '\n')
    textInput = ffmpeg.input(text_filename, format='concat', safe=0)
    audio = ffmpeg.input(audio_filename)
    if os.path.exists(output_filename):
        os.remove(output_filename)
    out = ffmpeg.output(
        textInput,
        audio,
        output_filename,
        vcodec="copy" if os.getenv('OE_DIRECT_H264_ENCODING', 'false') == 'true' else "libx264",
        acodec="copy",
        strict="experimental"
    )
    try:
        out.run(capture_stdout=True, capture_stderr=True)
    except ffmpeg.Error as e:
        print('ffmpeg error! stdout:')
        print(e.stdout.decode('utf8'))
        print('stderr:')
        print(e.stderr.decode('utf8'))

    # Clean up the temporary files that were created.
    if os.path.exists(root_filename):
        shutil.rmtree(root_filename)
    if os.path.exists(text_filename):
        os.remove(text_filename)
    if os.path.exists(audio_filename):
        os.remove(audio_filename)

def get_characters(most_common: List):
    characters = {Character.PHOENIX: most_common[0]}
    if len(most_common) > 0:
        characters[Character.EDGEWORTH] = most_common[1]
        for character in most_common[2:]:
            rnd_characters = [
                Character.GODOT,
                Character.FRANZISKA,
                Character.JUDGE,
                Character.LARRY,
                Character.MAYA,
                Character.KARMA,
                Character.PAYNE,
                Character.MAGGEY,
                Character.PEARL,
                Character.LOTTA,
                Character.GUMSHOE,
                Character.GROSSBERG,
            ]
            rnd_character = random.choice(
                list(
                    filter(
                        lambda character: character not in characters, rnd_characters
                    )
                )
            )
            characters[rnd_character] = character
    return characters

def comments_to_scene(comments: List[CommentBridge], name_music = "PWR", **kwargs):
    scene = []
    for comment in comments:
        # Determine the sentiment of the comment (if it's positive, negative, or neutral)
        polarity = analizer.get_sentiment(comment.body)
        rich_boxes = get_rich_boxes(comment.body)

        character_block = []
        character = comment.character

        # Determine the character's emotion based on the sentiment check from earlier
        main_emotion = random.choice(constants.character_emotions[character]["neutral"])
        if polarity == '-' or comment.score < 0:
            main_emotion = random.choice(constants.character_emotions[character]["sad"])
        elif polarity == '+':
            main_emotion = random.choice(constants.character_emotions[character]["happy"])

        # For each sentence we temporarily store it in character_block
        for idx, box in enumerate(rich_boxes):
            character_block.append(
                {
                    "character": character,
                    "name": comment.author.name,
                    "text": box,
                    "objection": (
                        polarity == '-'
                        or comment.score < 0
                        or re.search("objection", comment.body, re.IGNORECASE)
                        or (polarity == '+' and random.random() > 0.81)
                    )
                    and idx == 0,
                    "emotion": main_emotion,
                    "evidence": comment.evidence if hasattr(comment, "evidence") else None
                }
            )
        scene.append(character_block)

    formatted_scenes = []

    # Get relaxed and tense music
    base_music_path = f"music/{name_music}"
    relaxed_path = f"{base_music_path}/trial"
    tense_path = f"{base_music_path}/press"
    try:
        with open(f"assets/{base_music_path}/config.json") as f:
            # Randomly choose one of the relaxed and one of the tense tracks to
            # use for this video
            config_data: dict = json.load(f)
            relaxed_path = f"{base_music_path}/{random.choice(config_data.get('relaxed', ['trial']))}"
            tense_path = f"{base_music_path}/{random.choice(config_data.get('tense', ['press']))}"
    except FileNotFoundError as e:
        # config.json doesn't exist, so just load the trial and press
        print(f"config.json not found for music folder \"{name_music}\", so defaulting to trial.mp3 and press.mp3")

    last_audio = relaxed_path
    change_audio = True
    tense_bgm_started = False
    for character_block in scene:
        scene_objs = []
        if character_block[0]["objection"] == True:
            scene_objs.append(
                {
                    "character": character_block[0]["character"],
                    "action": constants.Action.OBJECTION,
                }
            )
            new_audio = tense_path
            if not tense_bgm_started:
                last_audio = new_audio
                change_audio = True
                tense_bgm_started = True

        for obj in character_block:
            # We insert the data in the character block in the definitive scene object
            scene_objs.append(
                {
                    "character": obj["character"],
                    "action": constants.Action.TEXT,
                    "emotion": obj["emotion"],
                    "text": obj["text"],
                    "name": obj["name"],
                    "evidence": obj["evidence"]
                }
            )
        # One scene may have several sub-scenes. I.e: A scene may have an objection followed by text
        formatted_scene = {
            "location": constants.character_location_map[character_block[0]["character"]],
            "scene": scene_objs,
        }
        if change_audio:
            formatted_scene["audio"] = last_audio
            change_audio = False
        formatted_scenes.append(formatted_scene)
    ace_attorney_anim(formatted_scenes, **kwargs)
