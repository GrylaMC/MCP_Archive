"""
The inject python script for later MCP exceptor versions.
For more information see generate_tiny.py.

Input: 
    sys.argv[1] for the jar file to be mapped

Output: 
    Mapped jar file goes to MCP_DIR/temp/out.jar


Copyright (C) 2026 - PsychedelicPalimpsest
Feel free to share this within the bounds of 
CC0 1.0 Universal
"""

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
