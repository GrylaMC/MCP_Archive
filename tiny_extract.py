"""
A tool for converting MCP mappings into the more standered fabric tiny (V1) format.

Some things to note:
 * The jar many mappings are based off is that which was distributed at the time. _NOT_ the version avalible todat.
 * Older versions of MCP lack field descripts, meaning those must be re-extracted from the Minecraft jar. 
    * Which causes issues when they do not match
 * There are several eras of the MCP format
 * In many of those eras, an early form of intermidiary mapping is attempted. 



Formatting details throughout history:
 - a1.1.2: Only revengpack16 has the config
    - rgs format
    - Uses "generate" mappings (aka intermediary)
        - In addition to regular mappings?
    - NO .csvs !!!!!
 - a1.2.1_1: First csv format
    - Starts the alpha csv format
        - Notably the alpha for
    - Contains classes.csv, removed in later versions
    - Contains minecraft.rgs, but is only intermediary
    - Also has minecraft_rav.rgs, which seem to map backwards



Copyright (C) 2025 - PsychedelicPalimpsest


This program is free software: you can redistribute it and/or modify
it under the terms of the GNU Affero General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU Affero General Public License for more details.

You should have received a copy of the GNU Affero General Public License
along with this program.  If not, see <https://www.gnu.org/licenses/>.

"""

import sys, os, csv
from os.path import *


SCRIPTS_DIR = join(dirname(dirname(abspath(__file__))), "utils", "scripts" )
if not exists(SCRIPTS_DIR):
    raise RuntimeError("Refusing to run without use of official workspace")

sys.path.append(SCRIPTS_DIR)

from mc import download_mojang_file
from jawa.classloader import ClassLoader



CONFIGS_DIR = join(dirname(abspath(__file__)), "configs")
OUT_DIR = join(dirname(abspath(__file__)), "tiny_v1s")

class TinyV1Writer:
    def __init__(self, namespaces):
        """
        namespaces: list of namespace names (e.g. ["official", "intermediary", "named"])
        """
        self.namespaces = namespaces
        self.lines = [f"v1\t" + "\t".join(namespaces)]

    def add_class(self, *names):
        """Add a class mapping across namespaces"""
        self.lines.append("CLASS\t" + "\t".join(names))

    def add_field(self, owner, desc, *names):
        """Add a field mapping"""
        self.lines.append("FIELD\t" + "\t".join([owner, desc] + list(names)))

    def add_method(self, owner, desc, *names):
        """Add a method mapping"""
        self.lines.append("METHOD\t" + "\t".join([owner, desc] + list(names)))

    def write(self, path):
        with open(path, "w", encoding="utf-8") as f:
            f.write("\n".join(self.lines) + "\n")

def build_descriptor_map_jar(jar_path: str):
    """
    Build {className: {fieldName: descriptor}} from the obfuscated jar.
    Keys are JVM internal names (slashes, e.g. kd, ko$1, net/minecraft/SomeClass).
    """
    desc_map = {}
    loader = ClassLoader(jar_path)

    for class_name in loader.classes:  # keys like 'kd', 'ko$1', 'net/minecraft/util/EnumChatFormatting'
        jclass = loader[class_name]
        inner_map = {}
        for entry in jclass.fields:
            inner_map[entry.name.value] = entry.descriptor.value
        for entry in jclass.methods:
            inner_map[entry.name.value + "+func"] = entry.descriptor.value
        desc_map[class_name] = inner_map

    return desc_map


def build_descriptor_map_moj(mc_ver: str):
    """
    Downloads the obfuscated Minecraft client jar for a given version
    and builds the descriptor map.
    """
    jar_path = "tmp.jar"
    download_mojang_file(mc_ver, "client", jar_path)
    map = build_descriptor_map_jar(jar_path)
    os.remove("tmp.jar")
    return map 



def revengpack_format(mc_ver : str, config_path : str, out_path : str, do_warnings = True):
    map = build_descriptor_map_moj(mc_ver)
    os.makedirs(dirname(out_path), exist_ok=True)
    
    out = TinyV1Writer(["official", "named"])
    

    with open(join(config_path, "minecraft.rgs"), "r") as f:
        lines = f.readlines()

    
    for line in lines:
        line = line.strip()

        if line.startswith(".class_map"):
            _, off, named = line.split(" ")
            out.add_class(off, named)
        elif line.startswith(".method_map"):
            _, off, desc, named = line.split(" ")
            owner = "/".join(off.split("/")[:-1])
            off_name = off.split("/")[-1]

            out.add_method(owner, desc, off_name, named)
        elif line.startswith(".field_map"):
            _, off, named = line.split(" ")
            owner = "/".join(off.split("/")[:-1])
            off_name = off.split("/")[-1]

            if not owner in map:
                if do_warnings:
                    print(f"WARNING: {owner} not found in provided jar")
                continue
            descs = map[owner]

            if not off_name in descs:
                if do_warnings:
                    print(f"WARNING: field {named} cannot be resolved in {owner}/")
                continue

            out.add_field(
                owner,
                descs[off_name],
                off_name,
                named
            )

        elif line.startswith("### GENERATED MAPPINGS:"):
            break

    out.write(out_path)


def alpha_csv_format(mc_ver : str, config_path : str, out_path : str, classes_version : int = 1, do_warnings = True):
    """
    
    :param classes_version: alpha format csv classes.csv files can contain multiple versions. 
                            This param selects the version to use
    """

    map = build_descriptor_map_moj(mc_ver)
    os.makedirs(dirname(out_path), exist_ok=True)
    
    out = TinyV1Writer(["official", "named"])
    

    with open(join(config_path, "classes.csv"), "r") as f:
        clsreader = iter(csv.reader(f, delimiter=',',quotechar='"'))

        # Skip headers
        for _ in range(4):
            next(clsreader)

        for entry in clsreader:
            if entry[classes_version] == "*":
                continue
            out.add_class(entry[classes_version], entry[0])

    # We first need to figure out the
    # intermidiary mappings
    method_map = {}
    field_map = {}
    with open(join(config_path, "minecraft.rgs"), "r") as f:
        for l in f.readlines():
            if l.startswith(".method_map"):
                _, off_name, desc, inter = l.strip().split(" ")
                method_map[inter] = [off_name, desc]
            if l.startswith(".field_map"):
                _, off_name, inter = l.strip().split(" ")
                field_map[inter] = off_name


    with open(join(config_path, "fields.csv"), "r") as f:
        fieldreader = iter(csv.reader(f, delimiter=',',quotechar='"'))

        for _ in range(3):
            next(fieldreader)

        for entry in fieldreader:
            inter_name = entry[2]

            if inter_name == "*":
                continue
            
            if not inter_name in field_map:
                if do_warnings:
                    print(f"WARNING: {inter_name} cannot be mapped back to function.")
                continue

            off_path = field_map[inter_name]
            off_cls = "/".join(off_path.split("/")[:-1])
            off_name = off_path.split("/")[-1]
            

            named_name = entry[6]


            if not off_cls in map:
                if do_warnings:
                    print(f"WARNING: {off_cls} not found in provided jar")
                continue
    
            descs = map[off_cls]
            if not off_name in descs:
                print(f"WARNING: field {off_name} cannot be resolved in {off_cls}: {descs.keys()}")
                continue

            out.add_field(off_cls, descs[off_name], off_name, named_name)


        
    with open(join(config_path, "methods.csv"), "r") as f:
        methodreader = iter(csv.reader(f, delimiter=',',quotechar='"'))


        for _ in range(4):
            next(methodreader)

        for entry in methodreader:
            if len(entry) < 5:
                continue
            if entry[1] == "*" or len(entry[1]) == 0:
                continue
            
            inter_name = entry[1]
            
            named_name = entry[4]

            assert named_name != "*", "Mapping issue"


            if not inter_name in method_map:
                if do_warnings:
                    print(f"WARNING: {inter_name} cannot be mapped back to method")
                continue

            off_path, o_desc = method_map[inter_name]
            off_cls =  "/".join(off_path.split("/")[:-1])
            off_name = off_path.split("/")[-1] 

            out.add_method(
                off_cls,
                o_desc,

                off_name,
                named_name
            )


    out.write(out_path)



STYLE_REGENGPACK = [
    ("a1.1.2", "revengpack16")
]

STYLE_OLD_ALPHA = [
    ("a1.2.1_01", "mcp20"),
    ("a1.2.1_01", "mcp20a"),
]

def generate_all_tiny(do_warnings = False):
    for ver, sub in STYLE_REGENGPACK:
        config_dir = join("configs", ver)

        diR = join(config_dir, sub)
        out = join(OUT_DIR, ver, sub+".tiny")
        if exists(out):
            continue
        print(f"Generating {out}")
        revengpack_format(ver, diR, out, do_warnings=do_warnings)

    for ver, sub, *classes_versions  in STYLE_OLD_ALPHA:

        config_dir = join("configs", ver)
        diR = join(config_dir, sub)
        out = join(OUT_DIR, ver, sub+".tiny")
        if exists(out):
            continue
        print(f"Generating {out}")
        alpha_csv_format(ver, diR, out, **(
            {"classes_version": classes_versions[0]} if len(classes_versions) else {}
        ), do_warnings=do_warnings)
    

def main():
    generate_all_tiny()






if __name__ == "__main__":
    main()
