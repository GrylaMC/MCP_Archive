from __future__ import print_function
import sys, os


os.chdir("mcp")

print("asd")
sys.path.insert(0, os.path.join("runtime"))
from commands import * 


commands = Commands(None)
print(commands.jarclient)
commands.jarclient = os.path.abspath("mc.jar")
print(commands.jarclient)

commands.logger.info ('> Creating SRGS for client')
commands.createsrgs(0)
commands.logger.info ('> Applying Retroguard to client')
commands.applyrg(0)
commands.logger.info ('> Applying Exceptor to client')
commands.applyexceptor(0)

