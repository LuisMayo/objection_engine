def lerp(a: float, b: float, t: float) -> float:
    return (1.0 - t) * a + b * t

def inv_lerp(a: float, b: float, v: float) -> float:
    return (v - a) / (b - a)

def remap(a_in: float, b_in: float, a_out: float, b_out: float, v: float, func: callable = None):
    t = inv_lerp(a_in, b_in, v)
    if func is not None:
        t = func(t)
    return lerp(a_out, b_out, t)

def ease_in_out_quint(x: int):
    return (16 * x ** 5) if x < 0.5 else 1 - ((-2 * x + 2) ** 5) / 2

def ease_in_out_cubic(x: int):
    return 4 * x * x * x if x < 0.5 else 1 - ((-2 * x + 2) ** 3) / 2