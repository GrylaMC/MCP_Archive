from os.path import abspath, exists, join 
import sys, os
import shutil


sys.path.insert(0, os.path.join("runtime"))
from commands import *


# This object CANNOT be used, but tells us important variables
incomplete_commands = Commands(None, shortstart=True)


version_client = incomplete_commands.versionClient
version_dir = join(incomplete_commands.dirjars, "versions", version_client)

if not exists(version_dir):
    os.makedirs(version_dir)


shutil.copy(
    sys.argv[1],
    join(version_dir, "%s.jar" % version_client)
)

shutil.copy(
    sys.argv[2],
    join(version_dir, "%s.json" % version_client)
)

if exists(join("temp", "out.jar")):
    os.remove(join("temp", "out.jar"))

commands = Commands(None)

side=CLIENT
commands.logger.info('> Creating SRGs')
commands.createsrgs(side, use_srg=commands.has_srg)

commands.logger.info('> Applying SpecialSource')
commands.applyss(side)
commands.logger.info('> Applying MCInjector')
commands.applyexceptor(side)

os.rename(join("temp", "minecraft_exc.jar"), join("temp", "out.jar"))
