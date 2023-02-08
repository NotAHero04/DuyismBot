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
		if mode == "result":
			return [a[0] * a[3], 2 * a[1] * a[2], a[0] * a[2] + a[1] * a[3]]
		elif mode == "left":
			return [a[0], a[2], a[0] + a[2], a[0] + 2 * a[2]]
		elif mode == "middle":
			return [a[3], a[2], a[3] + a[2], a[3] + 2 * a[2]]
		elif mode == "right":
			return [a[3], a[1], a[3] + a[1], a[3] + 2 * a[1]]
		else:
			raise ValueError("Operation not supported")


def run(number):
	v = [1, 1, 2, 3]
	try:
		n = int(number)
	except ValueError:
		print("The input is not an integer")
	if n >= 0:
		for i in to_base_3(n):
			if i == 0:
				v = gen_list("left", v)
			elif i == 1:
				v = gen_list("middle", v)
			else:  # i == 2
				v = gen_list("right", v)
	elif n == -1:
		pass
	else:
		print("The number must be at least -1")
	r = gen_list("result", v)
	return str(r[0]) + " ^ 2 + " + str(r[1]) + " ^ 2 = " + str(r[2]) + " ^ 2"
