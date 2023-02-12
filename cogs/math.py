import inspect
import os

try:
    import giacpy
except ImportError:
    pass

from discord import Interaction, app_commands
from discord.ext import commands

home = os.path.split(os.path.abspath(inspect.getsourcefile(lambda: 0)))[0]


class MathCog(commands.GroupCog, group_name="math"):
    def __init__(self, client):
        self.client = client


    @app_commands.command()
    @app_commands.describe(number="A number greater than -1")
    async def pythagoras(self, interaction: Interaction, number: app_commands.Range[int, -1]):
        """ Prints a prime Pythagoras triple """
        print(f"> {interaction.user} used the command 'pythagoras'.")
        await interaction.response.defer()
        await interaction.followup.send(pythagoras_run(number))


    @app_commands.command()
    @app_commands.choices(complex=[
        app_commands.Choice(name="true", value=1),
        app_commands.Choice(name="false", value=0)],
    technical_view=[
        app_commands.Choice(name="true", value=1),
        app_commands.Choice(name="false", value=0)
    ])
    @app_commands.describe(
        equation="An equation. Please insert multiplication symbol '*' when dealing with functions",
        complex="Decides whether the solutions contain complex numbers. Defaults to false",
        technical_view="Get raw input from the solver. Defaults to false"
    )

    async def solve(self, interaction: Interaction, equation: str, complex: int = 0, technical_view: int = 0):
        """ Solve simple equations """
        print(f"> {interaction.user} used the command 'solve'.")
        await interaction.response.defer()
        if complex == 1:
            sol = giacpy.cfsolve(equation)
            # Change it back to csolve() when it doesn't bug anymore
        else:
            sol = giacpy.solve(equation)
        res = []
        if technical_view == 0:
            for i in sol:
                if "rootof" in str(i):
                    res.append(giacpy.evalf(i))
                else:
                    res.append(i)
        else:
            res = list(sol)
        await interaction.followup.send("""Input: ```{}```
Output: ``` {}```
""".format(equation, '\n'.join(map(str, res))))

    @app_commands.command()
    @app_commands.describe(
        function="A function. Please insert multiplication symbol '*' when dealing with functions",
        var="The variable of the function to derive. Defaults to x. Type a function with variable x to omit this option",
        order="The order of the derivative. Defaults to 1",
        at="The value to calculate the derivative at. Defaults to nothing, and the bot will output the function instead"
    )

    async def derive(self, interaction: Interaction, function: str, var: str = 'x', order: app_commands.Range[int, 1] = 1, at: str = None):
        """ Get derivative of simple functions """
        print(f"> {interaction.user} used the command 'derive'.")
        await interaction.response.defer()
        res = giacpy.normal(giacpy.diff(function, f"{var}${order}"))
        if at is not None:
            res_t = giacpy.subst(res, var, at)
            if str(res_t) == "undef":
                res_t = "(undefined)"
            await interaction.followup.send("""Input: ```{}, variable {}, order {}, at {}```
Output: ``` {}```""".format(function, var, order, at, res_t))
        else:
            await interaction.followup.send("""Input: ```{}, variable {}, order {}```
Output: ``` {}```""".format(function, var, order, str(res).replace('**', '^')))


async def setup(client):
    try:
        import giacpy
    except ImportError:
        print("""> WARNING: Module giacpy is missing! To install giacpy, execute:
> apt-get install python3-pip libgiac-dev
> pip install giacpy
> Please note that giacpy currently DOES NOT support Python 3.11!
> Cog "math" will be disabled until you install giacpy.""")
    else:
        await client.add_cog(MathCog(client))

# code for pythagoras

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


def pythagoras_run(number):
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
