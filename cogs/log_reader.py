import inspect
import os
import discord
import re
import hashlib
import tempfile
import sys

from discord import Interaction, app_commands
from discord.ext import commands

home = os.path.split(os.path.abspath(inspect.getsourcefile(lambda: 0)))[0]

class Reader(commands.Cog):
 def __init__(self, client):
  self.client = client

 @commands.Cog.listener()
 async def on_message(self, message):
  attachments = message.attachments
  if len(attachments) != 0:
    for attachment in attachments:
     if re.match("latestlog.*\.txt", attachment.filename) is not None:
      print(f"> {message.author} sent a log.")
      file = await attachment.read()
      file_str = file.decode('UTF-8')
      hash = hashlib.sha1(file).hexdigest()
      path = "/tmp/duyismbot." + hash
      try:
       if not os.path.isfile(path):
        with open(path, 'w') as f:
         f.write(file_str)
        print(f"> Log saved to {path}")
       else:
        print("> Not saving log, it has been saved before")
      except HTTPException:
       print("> Couldn't save the log")
      result = logreader(path)
      rep = """*Result:*
Launcher version: {}
Device: {}
Minecraft version: {}""".format(result[0][0], ", ".join([i for i in result[0][1:4] if i is not None]), result[0][4])
      if result[0][5] is None:
       rep += "\nJava path: {}, ".format(result[0][6])
      else:
       rep += "\nJava version: {}, path: {}, ".format(*result[0][5:7])
      rep += "args: {}\nRenderer: {}".format(*result[0][7:9])
      if result[0][9] is not None:
       rep += "\nMod loader: {}, version {} for Minecraft {}".format(*result[0][9])
      if result[0][10] is not None:
       rep += "\nOptiFine: {} (shaders: {})".format(*result[0][10:12])
      rep += "\n\n*Warnings:*\n{}\n\n*Problems:*\n{}".format(*['\n'.join(i) for i in result[1:3]])
      await message.reply(content=rep)

async def setup(client):
 await client.add_cog(Reader(client))

# @profile
def logreader(path: str):
 res = []
 # events = []
 problems = []
 warnings = []
 # Open file
 try:
  with open(path, 'r') as f:
   file = f.read()
 except FileNotFoundError:
  return "File couldn't be read"
 # Launcher version (0)
 version = re.search("Launcher version: (.*)", file)
 if version is not None:
  res.append(version.group(1))
 else:
  res.append(None)
 # Device platform (1, 2, 3)
 arch = re.search("Architecture: (.*)", file)
 if arch is not None:
  res += [None, "Android", arch.group(1)]
 else:
  ios_platform = re.search("(iP.*) with (iOS .*) \((.*)\)", file)
  if ios_platform is not None:
   res += list(ios_platform.group(1, 2)) + ["arm64"]
  else:
   res += [None, "Android", None]
 # Minecraft version (4)
 if res[2] == "Android":
  mc = re.search("Selected Minecraft version: (.*)", file)
 else:
  mc = re.search("Launching Minecraft (.*)", file)
 if mc is not None:
  mc_ver = mc.group(1)
  res.append(mc_ver)
 else:
  res.append(None)
 # Java version and arguments (5, 6, 7)
 java_type = None
 if res[2] == "Android":
  java = re.search("JAVA_HOME=(.*)", file)
  java_args = re.search("Custom Java arguments: \"(.*)\"", file)
  if java is not None:
   java_path = java.group(1)
   java_ver = re.search("Internal(-(17))?", java_path)
   if java_ver is None:
    # Alternative way:
    java_ver = re.search("(jre|jdk)(.*)-.*-.*-release.tar.xz", file)
    if java_ver is not None:
     java_type = java_ver.group(1)
 else:
  java = re.search("JAVA_HOME is set to (.*)", file)
  # TODO: Any way to detect Java args on iOS log?
  java_args = None
  if java is not None:
   java_path = java.group(1)
   java_ver = re.search("java(-([0-9]+))-openjdk", java_path)
 if java_ver is not None:
  if java_ver.group(1) is None:
  # Android: Internal = 8
   res.append("8")
  else:
   res.append(java_ver.group(2))
 else:
  res.append(None)
 res.append(java_path)
 if java_args is not None:
  res.append(java_args.group(1))
 else:
  res.append(None)
 # Renderer (8)
 if res[2] == "Android":
  renderer = re.search("POJAV_RENDERER=(.*)", file)
 else:
  renderer = re.search("RENDERER is set to (.*)", file)
 if renderer is not None:
  renderer_name = renderer.group(1)
  res.append(renderer_name)
 # Mod loaders (9)
 ## Fabric / Quilt
 ml = re.search("Loading Minecraft (.*) with (.*) Loader (.*)", file)
 if ml is not None:
  res.append(ml.group(2, 3, 1))
 else:
 ## Forge (*-1.12.2)
  ml = re.search("Forge Mod Loader version (.*) for Minecraft (.*) loading", file)
  if ml is not None:
   res.append(("Forge (legacy)", *ml.group(1, 2)))
  else:
   ## Forge ModLauncher (1.13-*)
   ml = re.search("Forge mod loading, version (.*), for MC (.*) with MCP", file)
   if ml is not None:
    res.append(("Forge", *ml.group(1, 2)))
   else:
   ## TODO: More mod loader support in the future
    res.append(None)
 # OptiFine (10)
 of = re.search("OptiFine[-_].*\.jar", file)
 if of is not None:
  res.append(of.group(0).replace(".jar", ''))
  # Shaders (11)
  shader = re.search("Loaded shaderpack: (.*)", file)
  if shader is not None:
   res.append(shader.group(1))
  else:
   res.append(None)
 else:
  res += [None, None]
 if res[0] is not None:
# Warnings
  if res[5] is None:
   warnings.append("A custom runtime is used.")
  if res[2] == "Android" and not "v3_openjdk" in res[0]:
   if not "LOCAL" in res[0]:
    warnings.append("Not mainline launcher version.")
   else:
    warnings.append("Locally built launcher.")
  if res[11] is not None and "internal" in res[11]:
   warnings.append("OptiFine's internal shader is being used.")
  if java_type == "jdk":
   warnings.append("A JDK is detected in runtime path.")
  mixin_redirect_conflict = re.search("Skipping (.*)\.mixins\.json.* with priority .*, already redirected by (.*)\.mixins\.json.* with priority .*", file)
  if mixin_redirect_conflict is not None:
   warnings.append("Potential undocumented mod conflict: \"{}\" and \"{}\" (mixin redirection collision)".format(*mixin_redirect_conflict.group(1, 2)))
 # Problems
  unrecognized_vm_args = re.search("Unrecognized( VM)? option(:)? (.*)", file)
  if unrecognized_vm_args is not None:
   problems.append("Some VM options are unrecognized: {}".format(unrecognized_vm_args.group(3)))
  reserve_heap_space = re.search("Could not reserve enough space for (.*)KB object heap", file)
  if reserve_heap_space is not None:
   problems.append("The current allocation ({}MB) is too high for the system.".format(int(reserve_heap_space.group(1))/1024))
  if "java.lang.OutOfMemoryError: Java heap space" in file:
   problems.append("The current allocation is not enough for Minecraft.")
  if "angle" in res[8] and "glCheckFramebufferStatus returned unknown status" in file:
   problems.append("ANGLE is incompatible with Minecraft version {}".format(res[4]))
  if (res[3] == "arm" or res[3] == "x86") and "virgl" in res[8]:
   problems.append("VirGL is not supported on platform {}".format(res[3]))
  if "java.lang.ClassCastException: class jdk.internal.loader.ClassLoaders$AppClassLoader cannot be cast to class java.net.URLClassLoader" in file:
   problems.append("Legacy LaunchWrapper (used in MC version {}) is not compatible with Java version {}".format(res[4], res[5] or "being used"))
  if res[9] is not None and res[9][0] == "Fabric":
   if "java.lang.RuntimeException: error remapping game jars" in file:
    problems.append("Remapping Fabric game files failed")
   if "net.fabricmc.loader.impl.FormattedException: Mod resolution encountered an incompatible mod set!" in file:
    problems.append("The modpack is incompatible")
  if "[OptiFine] OpenGL error: 1280 (Invalid enum), at: Copy VBO" in file:
   problems.append("Render regions is enabled in OptiFine 1.17+ while using GL4ES")
  if "Native memory allocation (malloc) failed to allocate" in file:
   problems.append("JVM crashed due to insufficient memory on the system")
 return (res, warnings, problems)

# if __name__ == '__main__':
#  main()
