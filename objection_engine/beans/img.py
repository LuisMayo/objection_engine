from PIL import Image
import random as r

def add_margin(pil_img, top, right, bottom, left):
    width, height = pil_img.size
    new_width = width + right + left
    new_height = height + top + bottom
    result = Image.new(pil_img.mode, (new_width, new_height), (0, 0, 0, 0))
    result.paste(pil_img, (left, top))
    return result

class AnimImg:
    def __init__(
        self,
        path: str,
        *,
        x: int = 0,
        y: int = 0,
        w: int = None,
        h: int = None,
        key_x: int = None,
        key_x_reverse: bool = True,
        shake_effect: bool = False,
        half_speed: bool = False,
        repeat: bool = True,
        maxw: int = None,
        maxh: int = None
    ):
        self.x = x
        self.y = y
        self.maxw = maxw
        self.maxh = maxh
        self.path = path
        img = Image.open(path, "r")
        if img.format == "GIF" and img.is_animated:
            self.frames = []
            for idx in range(img.n_frames):
                img.seek(idx)
                resized = self.resize(img, w=w, h=h)
                converted = resized.convert('RGBA',palette=Image.ADAPTIVE)
                self.frames.append(converted)
        elif key_x is not None:
            self.frames = []
            for x_pad in range(key_x):
                self.frames.append(
                    add_margin(
                        self.resize(img, w=w, h=h).convert("RGBA"), 0, 0, 0, x_pad
                    )
                )
            if key_x_reverse:
                for x_pad in reversed(range(key_x)):
                    self.frames.append(
                        add_margin(
                            self.resize(img, w=w, h=h).convert("RGBA"), 0, 0, 0, x_pad
                        )
                    )
        else:
            self.frames = [self.resize(img, w=w, h=h).convert("RGBA")]
        self.w = self.frames[0].size[0]
        self.h = self.frames[0].size[1]
        self.shake_effect = shake_effect
        self.half_speed = half_speed
        self.repeat = repeat

    def resize(self, frame, *, w: int = None, h: int = None):
        if w is not None and h is not None:
            return frame.resize((w, h))
        else:
            if w is not None:
                w_perc = w / float(frame.size[0])
                _h = int((float(frame.size[1]) * float(w_perc)))
                # We resize only up to a given height
                if self.maxh is not None and _h > self.maxh:
                    _h = self.maxh
                return frame.resize((w, _h), Image.ANTIALIAS)
            if h is not None:
                h_perc = h / float(frame.size[1])
                _w = int((float(frame.size[0]) * float(h_perc)))
                # We resize only up to a given width
                if self.maxw is not None and _w > self.maxw:
                    _w = self.maxw
                return frame.resize((_w, h), Image.ANTIALIAS)
        return frame

    def render(self, background: Image = None, frame: int = 0):
        if frame > len(self.frames) - 1:
            if self.repeat:
                frame = frame % len(self.frames)
            else:
                frame = len(self.frames) - 1
        if self.half_speed and self.repeat:
            frame = int(frame / 2)
        _img = self.frames[frame]
        if background is None:
            _w, _h = _img.size
            _background = Image.new("RGBA", (_w, _h), (255, 255, 255, 255))
        else:
            _background = background
        _img.convert("RGBA")
        bg_w, bg_h = _background.size
        offset = (self.x, self.y)
        # if there is a shake effect to be applied
        # adjust the paste offset with random ints
        if self.shake_effect:
            offset = (self.x + r.randint(-1, 1), self.y + r.randint(-1, 1))
        # paste _img onto _background with offset
        _background.paste(_img, offset, mask=_img)
        if background is None:
            return _background

    def __str__(self):
        return self.path
