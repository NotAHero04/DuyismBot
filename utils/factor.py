import math


def run(number):
    try:
        n = int(number)
    except ValueError:
        print("The input is not an integer")
    if n >= 1e10:
        print("The number is too high")
    elif n < 2:
        print("The number must be at least 2")
    else:
        s = 2
        num = n
        ret = [[], []]
        while s <= math.sqrt(num):
            if num % s == 0:
                ret[0].append(s)
                ret[1].append(0)
                while num % s == 0:
                    ret[1][len(ret[1]) - 1] += 1
                    num = num // s
            s += 1
        if num >= 2:
            ret[0].append(num)
            ret[1].append(1)
        value = ""
        for i in range(len(ret[0])):
            value += str(ret[0][i]) + ' '
            if ret[1][i] >= 2:
                value += '^' + str(ret[1][i]) + ' '
            if i != len(ret[0]) - 1:
                value += '*' + ' '
    return value
