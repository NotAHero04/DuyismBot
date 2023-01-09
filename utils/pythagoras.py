import sys


def to_base_3(a: int = 0):
    if a < 0:
        raise ValueError("Non-negative integer expected")
    else:
        ret = []
        while a > 2:
            x = a % 3
            a = a // 3
            ret.insert(0, x)
        ret.insert(0, a)
        return ret


def gen_list(mode="result", a=None):
    if a is None:
        a = [1, 1, 2, 3]
    if len(a) != 4:
        raise ValueError("4-item list expected")
    else:
        match mode:
            case "result":
                return [a[0] * a[3], 2 * a[1] * a[2], a[0] * a[2] + a[1] * a[3]]
            case "left":
                return [a[0], a[2], a[0] + a[2], a[0] + 2 * a[2]]
            case "middle":
                return [a[3], a[2], a[3] + a[2], a[3] + 2 * a[2]]
            case "right":
                return [a[3], a[1], a[3] + a[1], a[3] + 2 * a[1]]
            case _:
                raise ValueError("Operation not supported")


def run(number):
    v = [1, 1, 2, 3]
    try:
        n = int(number)
    except ValueError:
        print("The input is not an integer")
    if n >= 0:
        for i in to_base_3(n):
            match i:
                case 0:
                    v = gen_list("left", v)
                case 1:
                    v = gen_list("middle", v)
                case 2:
                    v = gen_list("right", v)
    elif n == -1:
        pass
    else:
        print("The number must be at least -1")
    r = gen_list("result", v)
    return str(r[0]) + " ^ 2 + " + str(r[1]) + " ^ 2 = " + str(r[2]) + " ^ 2"
