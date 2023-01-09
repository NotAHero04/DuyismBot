import re
import sys
from concurrent.futures import ThreadPoolExecutor

logfile = open(sys.argv[1])


def parallel_task(pattern):
    for i, line in enumerate(logfile):
        search = re.search(pattern, line)
        if search is not None:
            return search


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
with ThreadPoolExecutor() as executor:
    results = list(executor.map(parallel_task, patterns))
    
