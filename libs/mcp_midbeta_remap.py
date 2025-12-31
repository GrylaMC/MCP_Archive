# This file is meant to be executed within the embeded MCP python interpreter
# and will simply instruct MCP to remap the jar. However, due to this being
# the beta version, it still requires field renaming after this!

# Outputs: temp/minecraft_rg.jar

from os.path import abspath, join
import sys, os


sys.path.insert(0, os.path.join("runtime"))
from commands import *


fake_commands = Commands(os.path.join("conf", "mcp.cfg"))


commands = Commands(os.path.join("conf", "mcp.cfg"))

commands.readconf()

commands.jarclient = abspath(sys.argv[1])
commands.creatergcfg()

commands.logger.info("> Creating SRGS for client")
commands.createsrgs(0)
commands.logger.info("> Applying Retroguard to client")
commands.applyrg(0)

os.rename(join("temp", "minecraft_rg.jar"), join("temp", "out.jar"))
