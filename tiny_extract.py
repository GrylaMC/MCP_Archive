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
        - This gets remove in mcp20a
 - b1.1_02: 
    - Seems to not have class definitions for beta...
 - b1.2.1_01:
    - Actually has some beta class mappings


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
import csv
import os
import sys
from os.path import abspath, dirname, exists, join

SCRIPTS_DIR = join(dirname(dirname(abspath(__file__))), "utils", "scripts")
if not exists(SCRIPTS_DIR):
    raise RuntimeError("Refusing to run without use of official workspace")

sys.path.append(SCRIPTS_DIR)

from mc import download_mojang_file
from jawa.classloader import ClassLoader
import tempfile

OUT_DIR = join(dirname(abspath(__file__)), "tiny_v1s")


class TinyV1Writer:
    def __init__(self, namespaces):
        """
        namespaces: list of namespace names (e.g. ["official", "intermediary",
        "named"])
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
    Build {className: {fieldOrMethodName(+func): descriptor}} from the
    obfuscated jar. Keys are JVM internal names (slashes, e.g. kd, ko$1,
    net/minecraft/SomeClass).
    """
    desc_map = {}
    loader = ClassLoader(jar_path)

    for class_name in loader.classes:
        jclass = loader[class_name]
        inner_map = {}
        for entry in jclass.fields:
            inner_map[entry.name.value] = entry.descriptor.value
        for entry in jclass.methods:
            inner_map[entry.name.value + "+func"] = entry.descriptor.value
        desc_map[class_name] = inner_map

    return desc_map


def build_descriptor_map_moj(mc_ver: str, mc_dir : str):
    """
    Downloads the obfuscated Minecraft client jar for a given version and
    builds the descriptor map.
    """
    jar_path = join(mc_dir, mc_ver + ".jar")

    if not exists(jar_path):
        download_mojang_file(mc_ver, "client", jar_path)
    desc_map = build_descriptor_map_jar(jar_path)
    return desc_map


def revengpack_format(
    mc_ver: str, mc_dir : str, config_path: str, out_path: str, do_warnings: bool = True
):
    desc_map = build_descriptor_map_moj(mc_ver, mc_dir)
    os.makedirs(dirname(out_path), exist_ok=True)

    out = TinyV1Writer(["official", "named"])

    with open(join(config_path, "minecraft.rgs"), "r", encoding="utf-8") as f:
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

            if owner not in desc_map:
                if do_warnings:
                    print(f"WARNING: {owner} not found in provided jar")
                continue

            owner_descs = desc_map[owner]
            if off_name not in owner_descs:
                if do_warnings:
                    print(f"WARNING: field {named} cannot be resolved in {owner}/")
                continue

            out.add_field(owner, owner_descs[off_name], off_name, named)

        elif line.startswith("### GENERATED MAPPINGS:"):
            break

    out.write(out_path)


def alpha_csv_format(
    mc_ver: str,
    mc_dir : str,
    config_path: str,
    out_path: str,
    classes_version: int = 1,
    do_warnings: bool = True,
):
    """
    :param classes_version: alpha format csv classes.csv files can contain
                            multiple versions. This param selects the version
                            to use
    """
    desc_map = build_descriptor_map_moj(mc_ver, mc_dir)
    os.makedirs(dirname(out_path), exist_ok=True)

    out = TinyV1Writer(["official", "intermediary", "named"])

    with open(join(config_path, "classes.csv"), "r", encoding="utf-8") as f:
        clsreader = iter(csv.reader(f, delimiter=",", quotechar='"'))

        # Skip headers
        for _ in range(4):
            next(clsreader)

        for entry in clsreader:
            if entry[classes_version] == "*":
                continue
            out.add_class(entry[classes_version], entry[classes_version], entry[0])

    # Build intermediary maps first
    method_map = {}
    field_map = {}
    with open(join(config_path, "minecraft.rgs"), "r", encoding="utf-8") as f:
        for l in f.readlines():
            l = l.strip()
            if l.startswith(".method_map"):
                _, off_name, desc, inter = l.split(" ")
                method_map[inter] = [off_name, desc]
            if l.startswith(".field_map"):
                _, off_name, inter = l.split(" ")
                field_map[inter] = off_name

    with open(join(config_path, "fields.csv"), "r", encoding="utf-8") as f:
        fieldreader = iter(csv.reader(f, delimiter=",", quotechar='"'))

        # Skip headers
        for _ in range(3):
            next(fieldreader)

        for entry in fieldreader:
            if len(entry) < 7:
                continue

            inter_name = entry[2]
            if inter_name == "*":
                continue

            named_name = entry[6]

            if inter_name not in field_map:
                if do_warnings:
                    print(
                        f"WARNING: {named_name} aka {inter_name} cannot be mapped "
                        f"back to function."
                    )
                continue

            off_path = field_map[inter_name]
            off_cls = "/".join(off_path.split("/")[:-1])
            off_name = off_path.split("/")[-1]

            if off_cls not in desc_map:
                if do_warnings:
                    print(f"WARNING: {off_cls} not found in provided jar")
                continue

            owner_descs = desc_map[off_cls]
            if off_name not in owner_descs:
                if do_warnings:
                    print(
                        f"WARNING: field {off_name} cannot be resolved in {off_cls}: "
                        f"{list(owner_descs.keys())}"
                    )
                continue

            out.add_field(
                off_cls, owner_descs[off_name], off_name, inter_name, named_name
            )

    with open(join(config_path, "methods.csv"), "r", encoding="utf-8") as f:
        methodreader = iter(csv.reader(f, delimiter=",", quotechar='"'))

        # Skip headers
        for _ in range(4):
            next(methodreader)

        for entry in methodreader:
            entry = [e.strip() for e in entry]

            if len(entry) < 5:
                continue
            if entry[1] == "*" or len(entry[1]) == 0:
                continue

            inter_name = entry[1]
            named_name = entry[4]

            assert named_name != "*", "Mapping issue"

            if inter_name not in method_map:
                if do_warnings:
                    print(
                        f"WARNING: {named_name} aka {inter_name} cannot be mapped "
                        f"back to method"
                    )
                continue

            off_path, o_desc = method_map[inter_name]
            off_cls = "/".join(off_path.split("/")[:-1])
            off_name = off_path.split("/")[-1]

            out.add_method(off_cls, o_desc, off_name, inter_name, named_name)

    out.write(out_path)


STYLE_REGENGPACK = [
    {"mcver": "a1.1.2", "ver": "a1.1.2", "sub": "revengpack16"},
]

STYLE_OLD_ALPHA = [
    {"ver": "a1.2.1_01", "sub": "mcp20",  "mcver": "a1.1.2", "out": "a1.1.2-mcp20",  "classes_version" : 1},
    {"ver": "a1.2.1_01", "sub": "mcp20a", "mcver": "a1.1.2", "out": "a1.1.2-mcp20a", "classes_version" : 1},

    {"ver": "a1.2.1_01", "sub": "mcp20",  "mcver": "a1.2.0", "out": "a1.2.0-mcp20",  "classes_version" : 2},
    {"ver": "a1.2.1_01", "sub": "mcp20a", "mcver": "a1.2.0", "out": "a1.2.0-mcp20a", "classes_version" : 2},


    # I have NO IDEA what 1.2.2 is being referred to in the config names
    # the wiki tells me that a lost version exists and a1.2.2a is a debug
    # build. So I am assuming using a1.2.2b is the best bet.

    {"ver": "a1.2.2", "sub": "mcp21",  "mcver": "a1.1.2", "out": "a1.1.2-mcp21",  "classes_version" : 1},
    {"ver": "a1.2.2", "sub": "mcp21",  "mcver": "a1.2.0", "out": "a1.2.0-mcp21",  "classes_version" : 2},


    {"ver": "a1.2.2", "sub": "mcp22",  "mcver": "a1.2.0", "out": "a1.2.0-mcp22",  "classes_version" : 1},
    {"ver": "a1.2.2", "sub": "mcp22",  "mcver": "a1.2.2b", "out": "a1.2.2b-mcp22",  "classes_version" : 2},

    {"ver": "a1.2.2", "sub": "mcp22a",  "mcver": "a1.2.0", "out": "a1.2.0-mcp22a",  "classes_version" : 1},
    {"ver": "a1.2.2", "sub": "mcp22a",  "mcver": "a1.2.2b", "out": "a1.2.2b-mcp22a",  "classes_version" : 2},

    {"ver": "a1.2.3_04", "sub": "mcp23", "mcver": "a1.2.2b", "out": "a1.2.2-mcp23", "classes_version": 1},
    {"ver": "a1.2.3_04", "sub": "mcp23", "mcver": "a1.2.3_02", "out": "a1.2.3_02-mcp23", "classes_version": 2},

    {"ver": "a1.2.5", "sub": "mcp24", "mcver": "a1.2.2b", "out": "a1.2.2-mcp24", "classes_version": 1},
    {"ver": "a1.2.5", "sub": "mcp24", "mcver": "a1.2.3_02", "out": "a1.2.3_02-mcp24", "classes_version": 2},

    {"ver": "a1.2.6", "sub": "mcp25", "mcver": "a1.2.5", "out": "a1.2.5-mcp25", "classes_version": 1},
    {"ver": "a1.2.6", "sub": "mcp25", "mcver": "a1.2.6", "out": "a1.2.6-mcp25", "classes_version": 2},
]

def generate_all_tiny(do_warnings):
    with tempfile.TemporaryDirectory() as temp_mc_dir:
        for cfg in STYLE_REGENGPACK:
            config_dir = join("configs", cfg["ver"])
            dir_ = join(config_dir, cfg["sub"])

            outf = f'{cfg["sub"] if not "out" in cfg else cfg["out"]}.tiny'
            out = join(OUT_DIR, cfg["ver"], outf)

            if exists(out):
                continue
            print(f"Generating {out}")
            revengpack_format(cfg["mcver"], temp_mc_dir, dir_, out, do_warnings=do_warnings)

        for cfg in STYLE_OLD_ALPHA:
            config_dir = join("configs", cfg["ver"])
            dir_ = join(config_dir, cfg["sub"])

            outf = f'{cfg["sub"] if not "out" in cfg else cfg["out"]}.tiny'
            out = join(OUT_DIR, cfg["ver"], outf)

            if exists(out):
                continue
            print(f"\tGenerating {out}")
            kwargs = {}
            if "classes_version" in cfg:
                kwargs["classes_version"] = cfg["classes_version"]
            alpha_csv_format(
                cfg["mcver"], temp_mc_dir, dir_, out, do_warnings=do_warnings, **kwargs
            )


def main():
    generate_all_tiny(False)


if __name__ == "__main__":
    main()
