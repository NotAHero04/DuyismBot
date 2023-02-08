import re
import sys

logfile = open(sys.argv[1])

patterns = [
	"iPhone.*|iPod.*|iPad.*|Architecture:.*",
	"Launcher version:.*",
	"Launching Minecraft .*|Minecraft version: .*",
	"Loading Minecraft .* with .* Loader .*",
	"Forge Mod Loader version .* for Minecraft .* loading|Forge mod loading, version .*, for MC .* with MCP .*",
	"Mod Loader has successfully loaded .* mods|Forge Mod Loader has identified .* mods to load",
	"dynamic-codesigning: .*",
	"JIT has been enabled"
]


def run(pattern):
	for i, line in enumerate(logfile):
		search = re.search(pattern, line)
		if search is not None:
			return search


