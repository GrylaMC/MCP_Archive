"""
The inject python script for early MCP exceptor versions.
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


commands = Commands(os.path.join("conf", "mcp.cfg"))


commands.jarclient = abspath(sys.argv[1])

commands.logger.info ('> Creating Retroguard config files')
commands.creatergcfg()

commands.logger.info ('> Creating SRGS for client')
commands.createsrgs(0)
commands.logger.info ('> Applying Retroguard to client')
commands.applyrg(0)
commands.logger.info ('> Applying Exceptor to client')
commands.applyexceptor(0)

os.rename(join("temp", "minecraft_exc.jar"), join("temp", "out.jar"))
