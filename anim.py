from beans.comment_bridge import CommentBridge
from PIL import Image, ImageDraw, ImageFont
from matplotlib.pyplot import imshow
import numpy as np
import cv2
from typing import List, Dict
import random
import os
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
from polarity_analysis import Analizer
analizer = Analizer()
from beans.img import AnimImg
from beans.text import AnimText
from beans.scene import AnimScene
from beans.video import AnimVideo
from constants import Character, lag_frames, fps
import constants
import re

nlp = spacy.load("xx_ent_wiki_sm")
nlp.add_pipe(nlp.create_pipe('sentencizer'))


def split_str_into_newlines(text: str, max_line_count: int = 34):
    words = text.split(" ")
    new_text = ""
    for word in words:
        last_sentence = new_text.split("\n")[-1] + word + " "
        if len(last_sentence) >= max_line_count:
            new_text += "\n" + word + " "
        else:
            new_text += word + " "
    return new_text


# @profile
def do_video(config: List[Dict], output_filename):
    scenes = []
    sound_effects = []
    part = 0
    for scene in config:
        # We pick up the images to be rendered
        bg = AnimImg(constants.location_map[scene["location"]])
        arrow = AnimImg("assets/arrow.png", x=235, y=170, w=15, h=15, key_x=5)
        textbox = AnimImg("assets/textbox4.png", w=bg.w)
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
        text = None
        #         print('scene', scene)
        for obj in scene["scene"]:
            # First we check for evidences
            if "evidence" in obj and obj['evidence'] is not None:
                if scene["location"] == constants.Location.COURTROOM_RIGHT:
                    evidence = AnimImg(obj["evidence"], x=26, y=19, w=85, maxh=75)
                else:
                    evidence = AnimImg(obj["evidence"], x=145, y=19, w=85, maxh=75)
            else:
                evidence = None
            if "character" in obj:
                _dir = constants.character_map[obj["character"]]
                current_character_name = obj["character"]
                #                 print('character change', current_character_name)
                #                 if current_character_name == "Larry":
                #                     current_character_name = "The Player"
                character_name = AnimText(
                    current_character_name,
                    font_path="assets/igiari/Igiari.ttf",
                    font_size=12,
                    x=4,
                    y=113,
                )
                default = "normal" if "emotion" not in obj else obj["emotion"]
                default_path = (
                    f"{_dir}/{current_character_name.lower()}-{default}(a).gif"
                )
                if not os.path.isfile(default_path):
                    default_path = (
                        f"{_dir}/{current_character_name.lower()}-{default}.gif"
                    )
                if not os.path.isfile(
                        default_path
                        ):
                        default_path = (
                            f"{_dir}/{current_character_name.lower()}-normal(a).gif"
                        )
                assert os.path.isfile(
                    default_path
                ), f"{default_path} does not exist"
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
                if not os.path.isfile(
                        default_path
                        ):
                        default_path = (
                            f"{_dir}/{current_character_name.lower()}-normal(a).gif"
                        )
                assert os.path.isfile(
                    default_path
                ), f"{default_path} does not exist"
                default_character = AnimImg(default_path, half_speed=True)
                if "(a)" in default_path:
                    talking_character = AnimImg(
                        default_path.replace("(a)", "(b)"), half_speed=True
                    )
                else:
                    talking_character = AnimImg(default_path, half_speed=True)
            if "action" in obj and (
                obj["action"] == constants.Action.TEXT
                or obj["action"] == constants.Action.TEXT_SHAKE_EFFECT
            ):
                character = talking_character
                _text = split_str_into_newlines(obj["text"])
                _colour = None if "colour" not in obj else obj["colour"]
                text = AnimText(
                    _text,
                    font_path="assets/igiari/Igiari.ttf",
                    font_size=15,
                    x=5,
                    y=130,
                    typewriter_effect=True,
                    colour=_colour,
                )
                num_frames = len(_text) + lag_frames
                _character_name = character_name
                if "name" in obj:
                    _character_name = AnimText(
                        obj["name"],
                        font_path="assets/igiari/Igiari.ttf",
                        font_size=12,
                        x=4,
                        y=113,
                    )
                if obj["action"] == constants.Action.TEXT_SHAKE_EFFECT:
                    bg.shake_effect = True
                    character.shake_effect = True
                    if bench is not None:
                        bench.shake_effect = True
                    textbox.shake_effect = True
                scene_objs = list(
                    filter(
                        lambda x: x is not None,
                        [bg, character, bench, textbox, _character_name, text, evidence],
                    )
                )
                scenes.append(
                    AnimScene(scene_objs, len(_text) - 1, start_frame=current_frame)
                )
                sound_effects.append({"_type": "bip", "length": len(_text) - 1})
                if obj["action"] == constants.Action.TEXT_SHAKE_EFFECT:
                    bg.shake_effect = False
                    character.shake_effect = False
                    if bench is not None:
                        bench.shake_effect = False
                    textbox.shake_effect = False
                text.typewriter_effect = False
                character = default_character
                scene_objs = list(
                    filter(
                        lambda x: x is not None,
                        [bg, character, bench, textbox, _character_name, text, arrow, evidence],
                    )
                )
                scenes.append(
                    AnimScene(scene_objs, lag_frames, start_frame=len(_text) - 1)
                )
                current_frame += num_frames
                sound_effects.append({"_type": "silence", "length": lag_frames})
            elif "action" in obj and obj["action"] == constants.Action.SHAKE_EFFECT:
                bg.shake_effect = True
                character.shake_effect = True
                if bench is not None:
                    bench.shake_effect = True
                textbox.shake_effect = True
                character = default_character
                #                 print(character, textbox, character_name, text)
                if text is not None:
                    scene_objs = list(
                        filter(
                            lambda x: x is not None,
                            [
                                bg,
                                character,
                                bench,
                                textbox,
                                character_name,
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
            elif "action" in obj and obj["action"] == constants.Action.OBJECTION:
                #                 bg.shake_effect = True
                #                 character.shake_effect = True
                #                 if bench is not None:
                #                     bench.shake_effect = True
                objection.shake_effect = True
                character = default_character
                scene_objs = list(
                    filter(lambda x: x is not None, [bg, character, bench, objection])
                )
                scenes.append(AnimScene(scene_objs, 11, start_frame=current_frame))
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
            else:
                # list(filter(lambda x: x is not None, scene_objs))
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
                video = AnimVideo(scenes, fps=fps)
                video.render(output_filename + '/' +str(part) + '.mp4')
                part+=1
                scenes = []

    if (len(scenes) > 0):
        video = AnimVideo(scenes, fps=fps)
        video.render(output_filename + '/' +str(part) + '.mp4')
    return sound_effects

def do_audio(sound_effects: List[Dict], output_filename):
    audio_se = AudioSegment.empty()
    bip = AudioSegment.from_wav(
        "assets/sfx general/sfx-blipmale.wav"
    ) + AudioSegment.silent(duration=50)
    blink = AudioSegment.from_wav("assets/sfx general/sfx-blink.wav")
    blink -= 10
    badum = AudioSegment.from_wav("assets/sfx general/sfx-fwashing.wav")
    long_bip = bip * 100
    long_bip -= 10
    spf = 1 / fps * 1000
    pheonix_objection = AudioSegment.from_mp3("assets/Phoenix - objection.mp3")
    edgeworth_objection = AudioSegment.from_mp3(
        "assets/Edgeworth - (English) objection.mp3"
    )
    default_objection = AudioSegment.from_mp3("assets/Payne - Objection.mp3")
    for obj in sound_effects:
        if obj["_type"] == "silence":
            audio_se += AudioSegment.silent(duration=int(obj["length"] * spf))
        elif obj["_type"] == "bip":
            audio_se += blink + long_bip[: max(int(obj["length"] * spf - len(blink)), 0)]
        elif obj["_type"] == "objection":
            if obj["character"] == "phoenix":
                audio_se += pheonix_objection[: int(obj["length"] * spf)]
            elif obj["character"] == "edgeworth":
                audio_se += edgeworth_objection[: int(obj["length"] * spf)]
            else:
                audio_se += default_objection[: int(obj["length"] * spf)]
        elif obj["_type"] == "shock":
            audio_se += badum[: int(obj["length"] * spf)]
    #     audio_se -= 10
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
    #     print(music_tracks)
    music_se = AudioSegment.empty()
    for track in music_tracks:
        music_se += AudioSegment.from_mp3(track["src"])[
            : int((track["length"] / fps) * 1000)
        ]
    #     music_se = AudioSegment.from_mp3(sound_effects[0]["src"])[:len(audio_se)]
    #     music_se -= 5
    final_se = music_se.overlay(audio_se)
    final_se.export(output_filename, format="mp3")

def ace_attorney_anim(config: List[Dict], output_filename: str = "output.mp4"):
    root_filename = output_filename[:-4]
    audio_filename = output_filename + '.audio.mp3'
    text_filename = root_filename + '.txt'
    if os.path.exists(root_filename):
        shutil.rmtree(root_filename)
    os.mkdir(root_filename)
    sound_effects = do_video(config, root_filename)
    do_audio(sound_effects, audio_filename)
    videos = []
    with open(text_filename, 'w') as txt:
        for file in os.listdir(root_filename):
            videos.append(file)
        videos.sort(key=lambda item : int(item[:-4]))
        for video in videos:
            txt.write('file ' + root_filename + '/' +video + '\n')
    textInput = ffmpeg.input(text_filename, format='concat')
    audio = ffmpeg.input(audio_filename)
    if os.path.exists(output_filename):
        os.remove(output_filename)
    out = ffmpeg.output(
        textInput,
        audio,
        output_filename,
        vcodec="copy",
        acodec="aac",
        strict="experimental"
    )
    out.run()
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
            #         rnd_characters = rnd_prosecutors if len(set(rnd_prosecutors) - set(characters.keys())) > 0 else rnd_witness
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
        polarity = analizer.get_sentiment(comment.body)
        tokens = nlp(comment.body)
        sentences = [sent.string.strip() for sent in tokens.sents]
        joined_sentences = []
        i = 0
        while i < len(sentences):
            sentence = sentences[i]
            if len(sentence) > 85:
                text_chunks = [chunk for chunk in wrap(sentence, 85)]
                joined_sentences = [*joined_sentences, *text_chunks]
                i += 1
            else:
                if i + 1 < len(sentences) and len(f"{sentence} {sentences[i+1]}") <= 85: # Maybe we can join two different sentences
                    joined_sentences.append(sentence + " " + sentences[i+1])
                    i += 2
                else:
                    joined_sentences.append(sentence)
                    i += 1
        character_block = []
        character = comment.character
        main_emotion = random.choice(constants.character_emotions[character]["neutral"])
        if polarity == '-' or comment.score < 0:
            main_emotion = random.choice(constants.character_emotions[character]["sad"])
        elif polarity == '+':
            main_emotion = random.choice(constants.character_emotions[character]["happy"])
        # For each sentence we temporaly store it in character_block
        for idx, chunk in enumerate(joined_sentences):
            character_block.append(
                {
                    "character": character,
                    "name": comment.author.name,
                    "text": chunk,
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
    if name_music == 'PWR':
        last_audio = "03 - Turnabout Courtroom - Trial"
    elif name_music == 'JFA':
        last_audio = "Phoenix Wright Ace Attorney_ Justice for All OST - Trial"
    else:
        last_audio = "Phoenix Wright_ Trials and Tribulations OST - Trial"
    change_audio = True
    for character_block in scene:
        scene_objs = []
        if character_block[0]["objection"] == True:
            scene_objs.append(
                {
                    "character": character_block[0]["character"],
                    "action": constants.Action.OBJECTION,
                }
            )
            if name_music == 'PWR':
                if last_audio != "08 - Pressing Pursuit _ Cornered":
                    last_audio = "08 - Pressing Pursuit _ Cornered"
                    change_audio = True
            elif name_music == 'JFA':
                if last_audio != "Phoenix Wright Ace Attorney_ Justice for All OST - Pressing Pursuit _ Cross-Examine":
                    last_audio = "Phoenix Wright Ace Attorney_ Justice for All OST - Pressing Pursuit _ Cross-Examine"
                    change_audio = True
            else:
                if last_audio != "Phoenix Wright_ Trials and Tribulations OST - Pressing Pursuit _ Caught":
                    last_audio = "Phoenix Wright_ Trials and Tribulations OST - Pressing Pursuit _ Caught"
                    change_audio = True
            
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
