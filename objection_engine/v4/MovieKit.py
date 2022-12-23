from PIL import Image, ImageDraw, ImageFont, ImageOps, ImageFile
import ffmpeg
from .math_helpers import lerp
from typing import Callable, Union
from time import time, sleep
from os import mkdir, remove
from shutil import rmtree
from pydub import AudioSegment

# NOTE: This fixes a weird issue
# (https://github.com/Meorge/objection_engine/issues/1)
# HOWEVER according to StackOverflow it might also cause some images to
# be black. So, if you're trying to load images and that happens, maybe that's
# why???
ImageFile.LOAD_TRUNCATED_IMAGES = True


class Scene:
    w: int = 0
    h: int = 0
    __root: "SceneObject" = None

    def __init__(self, w: int = 0, h: int = 0, root: "SceneObject" = None):
        self.w = w
        self.h = h
        self.__done = False
        self.set_root(root)

    def set_root(self, root: "SceneObject"):
        if self.__root is not None:
            self.__root.__parent = None
        self.__root = root
        if self.__root is not None:
            self.__root.make_root(self)

    def render(self, path: str):
        img = Image.new("RGBA", (self.w, self.h))
        ctx = ImageDraw.ImageDraw(img)

        all_objects: list[SceneObject] = sorted(
            self.__root.get_self_and_children_as_flat_list(), key=lambda obj: obj.z
        )

        for object in all_objects:
            if object.get_absolute_visibility():
                object.render(img, ctx)

        img.save(path)

    def update(self, delta: float):
        for object in self.__root.get_self_and_children_as_flat_list():
            object.update(delta)

    def set_animation_done(self):
        self.__done = True

    def is_animation_done(self):
        return self.__done

    def receive_message(self, data):
        ...


class SceneObject:
    x: int = 0
    y: int = 0
    z: int = 0
    name: str = ""
    visible: bool = True
    __children: list["SceneObject"] = []
    __parent: Union["SceneObject", Scene] = None

    def __init__(
        self,
        parent: "SceneObject" = None,
        name: str = "",
        pos: tuple[int, int, int] = (0, 0, 0),
    ):
        self.x, self.y, self.z = pos
        self.name = name
        self.__children = []

        if isinstance(parent, Scene):
            parent.set_root(self)

        elif isinstance(parent, SceneObject) and parent is not None:
            parent.add_child(self)

    def __repr__(self) -> str:
        return type(self).__name__ + f' "{self.name}" ({self.x}, {self.y}, {self.z})'

    def render(self, img: Image.Image, ctx: ImageDraw.ImageDraw):
        pass

    def update(self, delta):
        pass

    def get_x(self) -> int:
        return self.x

    def get_y(self) -> int:
        return self.y

    def set_x(self, x: int):
        self.x = int(x)

    def set_y(self, y: int):
        self.y = int(y)

    def show(self):
        self.visible = True

    def hide(self):
        self.visible = False

    def make_root(self, scene: Scene):
        self.__parent = scene

    def add_child(self, new_child: "SceneObject"):
        self.__children.append(new_child)
        if new_child.__parent is not None:
            new_child.__parent.__children.remove(new_child)
        new_child.__parent = self

    def get_scene(self) -> Scene:
        p = self
        while True:
            p = p.__parent
            if isinstance(p, Scene):
                return p
            elif p is None:
                return None

    def get_absolute_position(self) -> tuple[int, int, int]:
        p = self
        x_out = 0
        y_out = 0
        z_out = 0
        while p is not None and not isinstance(p, Scene):
            x_out += p.x
            y_out += p.y
            z_out += p.z
            p = p.__parent
        return (x_out, y_out, z_out)

    def get_absolute_visibility(self) -> bool:
        p = self
        while p is not None and not isinstance(p, Scene):
            if not p.visible:
                return False
            p = p.__parent
        return True

    def print_hierarchy(self):
        self.__internal_print_hierarchy(0)

    def __internal_print_hierarchy(self, i: int = 0):
        print(("\t" * i) + str(self))
        for child in self.__children:
            child.__internal_print_hierarchy(i + 1)

    def get_self_and_children_as_flat_list(self) -> list["SceneObject"]:
        nodes: list["SceneObject"] = []

        def f(c):
            for ch in c.__children:
                nodes.append(ch)
                f(ch)

        f(self)
        return nodes

    def emit_message(self, data):
        if isinstance(self.__parent, SceneObject):
            self.__parent.emit_message(data)
        elif isinstance(self.__parent, Scene):
            self.__parent.receive_message(data)
        else:
            print(
                f"Error in emit_audio - parent of {self} is type {type(self.__parent)}"
            )


class ImageObject(SceneObject):
    filepath: str = ""
    t: float = 0.0

    width: int = None
    height: int = None

    image_data: Union[Image.Image, list[tuple[Image.Image, float]]] = []

    current_frame: Image = None
    callbacks: dict = {}

    def __init__(
        self,
        parent: "SceneObject" = None,
        name: str = "",
        pos: tuple[int, int, int] = (0, 0, 0),
        width: int = None,
        height: int = None,
        flip_x: bool = False,
        flip_y: bool = False,
        filepath: str = None,
    ):
        super().__init__(parent, name, pos)
        self.width = width
        self.height = height
        self.flip_x = flip_x
        self.flip_y = flip_y
        self.current_frame = None
        self.set_filepath(filepath)

    def update(self, delta):
        t_before = self.t
        self.t += delta
        for time, callback in self.callbacks.items():
            if t_before < time and self.t >= time and callback is not None:
                callback()

    def set_filepath(self, filepath: str, callbacks: dict = None):
        self.callbacks = callbacks if callbacks is not None else {}
        self.t = 0.0
        self.filepath = filepath
        if self.filepath is None:
            self.image_data = None
            return
        with Image.open(self.filepath) as my_img:
            try:
                is_animated = my_img.is_animated
            except AttributeError:
                is_animated = False

            if is_animated:
                self.image_data = []
                time_so_far = 0.0
                for frame_no in range(my_img.n_frames):
                    my_img.seek(frame_no)
                    time_so_far += my_img.info["duration"] / 1000
                    self.image_data.append((my_img.convert("RGBA"), time_so_far))
                self.image_duration = time_so_far
            else:
                self.image_data = my_img.convert("RGBA")
                self.image_duration = None

    def get_current_frame(self) -> Image.Image:
        t = self.t % self.image_duration
        for image, max_time in self.image_data:
            if max_time > t:
                return image
        return None

    def render(self, img: Image.Image, ctx: ImageDraw.ImageDraw):
        if self.image_data is None:
            return
        x, y, _ = self.get_absolute_position()
        box = (x, y)

        # Resize image to expected bounds
        if isinstance(self.image_data, Image.Image):
            w = self.image_data.width if self.width is None else self.width
            h = self.image_data.height if self.height is None else self.height
            resized = self.image_data.resize((w, h))
        elif isinstance(self.image_data, list):
            current_frame = self.get_current_frame()
            w = current_frame.width if self.width is None else self.width
            h = current_frame.height if self.height is None else self.height
            resized = current_frame.resize((w, h))

        # If this image is entirely off-screen we don't need to render it!
        left = x
        right = x + w
        top = y
        bottom = y + h

        scene_left = 0
        scene_right = self.get_scene().w
        scene_top = 0
        scene_bottom = self.get_scene().h

        if (
            (right < scene_left)
            or (left > scene_right)
            or (bottom < scene_top)
            or (top > scene_bottom)
        ):
            return

        # Flip images if necessary
        if self.flip_x:
            resized = ImageOps.mirror(resized)
        if self.flip_y:
            resized = ImageOps.flip(resized)

        img.alpha_composite(resized, box)
        # img.paste(resized, box, mask=resized)


class SimpleTextObject(SceneObject):
    def __init__(
        self,
        parent: "SceneObject" = None,
        name: str = "",
        pos: tuple[int, int, int] = (0, 0, 0),
        text: str = "",
        font: ImageFont.FreeTypeFont = None,
    ):
        super().__init__(parent, name, pos)
        self.text = text
        self.font = font

    def get_width(self):
        if self.font is not None:
            return self.font.getlength(self.text)

    def render(self, img: Image.Image, ctx: ImageDraw.ImageDraw):
        x, y, _ = self.get_absolute_position()

        args = {"xy": (x, y), "text": self.text, "fill": (255, 255, 255)}

        if self.font is not None:
            args["font"] = self.font
        ctx.text(**args)


class Sequencer:
    actions: list["SequenceAction"] = []

    def run_action(self, action: "SequenceAction"):
        self.actions.append(action)
        action.sequencer = self

    def update(self, delta):
        self.actions = [action for action in self.actions if not action.completed]
        for action in self.actions:
            action.update(delta)


class SequenceAction:
    sequencer: Sequencer
    completed: bool = False

    def start(self):
        ...

    def update(self, delta):
        ...


class MoveSceneObjectAction(SequenceAction):
    target_value: tuple[int, int] = (0, 0)
    duration: float = 0.0

    scene_object: SceneObject = None
    ease_function = lambda _, x: x

    on_complete = None

    time_passed: float = 0.0
    current_value: float = 0

    def __init__(
        self,
        target_value: tuple[int, int],
        duration: float,
        scene_object: SceneObject = None,
        ease_function: Callable[[float], float] = None,
        on_complete_function: Callable[[], None] = None,
    ):
        self.target_value = target_value
        self.duration = duration
        self.scene_object = scene_object
        if ease_function is not None:
            self.ease_function = ease_function
        self.on_complete = on_complete_function

    def update(self, delta):
        if self.time_passed == 0:
            self.initial_value = (self.scene_object.x, self.scene_object.y)

        self.time_passed += delta
        percent_complete = self.time_passed / self.duration

        percent_complete_eased = self.ease_function(percent_complete)
        new_x = lerp(
            self.initial_value[0], self.target_value[0], percent_complete_eased
        )
        new_y = lerp(
            self.initial_value[1], self.target_value[1], percent_complete_eased
        )
        self.scene_object.set_x(new_x)
        self.scene_object.set_y(new_y)

        if percent_complete_eased >= 1.0 and not self.completed:
            self.completed = True
            if self.on_complete is not None:
                self.on_complete()


class Director:
    def __init__(self, scene: Scene = None, fps: float = 30, callbacks: dict = None):
        self.sequencer = Sequencer()
        self.scene = scene
        self.fps = fps
        self.audio_commands: list[dict] = []
        self.time = 0.0
        self.callbacks = {} if callbacks is None else callbacks

    def update(self, delta: float):
        ...

    def render_audio(
        self, overall_duration, output_location, volume_adjustment: float = 0.0
    ):
        duration_ms = int(overall_duration * 1000)
        base_track = AudioSegment.silent(duration=duration_ms)

        for i, audio in enumerate(self.audio_commands):
            path = audio["path"]
            offset = int(audio.get("offset", 0.0) * 1000)
            loop_type = audio.get("loop_type", "no_loop")
            loop_delay = int(audio.get("loop_delay", 0) * 1000)
            end_time = audio.get("end", duration_ms)

            # Segment with silence afterwards
            new_segment = AudioSegment.from_file(path) + AudioSegment.silent(
                duration=loop_delay
            )

            # The segment should be this long
            duration_of_total_segment = int(end_time * 1000) - offset

            if loop_type == "no_loop":
                base_track = base_track.overlay(new_segment, offset)
            elif loop_type == "loop_complete_only":
                # Keep adding instances of this sound until we can't anymore
                looped_segment = AudioSegment.empty()
                while len(looped_segment) <= duration_of_total_segment:
                    looped_segment += new_segment

                base_track = base_track.overlay(looped_segment, offset)

            elif loop_type == "loop_until_truncated":
                looped_segment = AudioSegment.silent(duration=duration_of_total_segment)
                looped_segment = looped_segment.overlay(new_segment, loop=True)
                base_track = base_track.overlay(looped_segment, offset)

            if "on_audio_composite_progress" in self.callbacks:
                self.callbacks["on_audio_composite_progress"](
                    i, len(self.audio_commands), audio
                )

        base_track += volume_adjustment
        base_track.export(f"{output_location}.mp3", bitrate="312k")

    def render_movie(self, volume_adjustment: float = 0.0):
        self.time = 0.0
        self.is_done = False
        frame: int = 0
        temp_folder_name = f"output-{int(time())}"
        mkdir(temp_folder_name)
        while not self.is_done:
            self.update(1 / self.fps)
            self.sequencer.update(1 / self.fps)
            self.scene.update(1 / self.fps)
            self.scene.render(f"{temp_folder_name}/{frame:010d}.png")
            self.time += 1 / self.fps
            frame += 1

        self.render_audio(frame * (1 / self.fps), temp_folder_name, volume_adjustment)

        video_stream = ffmpeg.input(
            f"{temp_folder_name}/*.png", pattern_type="glob", framerate=self.fps
        )
        audio_stream = ffmpeg.input(f"{temp_folder_name}.mp3")

        stream = ffmpeg.concat(video_stream, audio_stream, v=1, a=1)
        stream = ffmpeg.output(
            stream,
            f"{temp_folder_name}.mp4",
            vcodec="h264",
            acodec="aac",
            pix_fmt="yuv420p",
        )
        stream = ffmpeg.overwrite_output(stream)

        if "on_ffmpeg_started" in self.callbacks:
            self.callbacks["on_ffmpeg_started"]()

        ffmpeg.run(stream, quiet=True)

        if "on_ffmpeg_finished" in self.callbacks:
            self.callbacks["on_ffmpeg_finished"]()

        # Delete frames folder and audio track
        remove(f"{temp_folder_name}.mp3")
        rmtree(temp_folder_name)
