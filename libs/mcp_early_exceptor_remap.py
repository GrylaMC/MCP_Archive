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
