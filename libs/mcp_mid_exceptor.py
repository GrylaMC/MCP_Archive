from os.path import abspath, exists, join 
import sys, os


sys.path.insert(0, os.path.join("runtime"))
from commands import *


commands = Commands(None, verify=True)

if exists(join("temp", "out.jar")):
    os.remove(join("temp", "out.jar"))

commands.jarclient = abspath(sys.argv[1])

side=CLIENT
commands.logger.info('> Creating Retroguard config files')
commands.creatergcfg(reobf=False, keep_lvt=True, keep_generics=True)
commands.logger.info('> Creating SRGs')
commands.createsrgs(side, use_srg=commands.has_srg)
commands.logger.info('> Applying Retroguard')
commands.applyrg(side)
commands.logger.info('> Applying MCInjector')
commands.applyexceptor(side)


os.rename(join("temp", "minecraft_exc.jar"), join("temp", "out.jar"))
