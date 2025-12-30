from os.path import basename, dirname, exists, join, abspath, splitext
import os, sys, subprocess, tempfile, shutil
from typing import Generator

from libs.jar_marker import taint_jar, generate_tiny

SCRIPTS_DIR = join(dirname(dirname(abspath(__file__))), "utils", "scripts")
if not exists(SCRIPTS_DIR):
    raise RuntimeError("Refusing to run without use of official workspace")

sys.path.append(SCRIPTS_DIR)

from mcjar import get_piston_file, REMAPPER


def get_mcp_temp(zip_file: str):
    with tempfile.TemporaryDirectory(delete=False) as f:
        if subprocess.call(["unzip", "-q", zip_file, "-d", f]) > 1:
            raise RuntimeError("Cannot unzip")
        return f


# Only used in a1.1.2, just is behind a single retroguard file
def style_retroguard_old(mcp_zip, mc_versions: list[tuple[str, str]]):
    mcp_dir = None
    for mc_ver, out_tiny in mc_versions:
        if exists(out_tiny):
            continue

        if mcp_dir is None:
            mcp_dir = get_mcp_temp(mcp_zip)
            print(f"=========== {basename(mcp_zip)}: Style Retroguard ===========")

        print(f"[*] Running for {mc_ver}")
        os.makedirs(dirname(out_tiny), exist_ok=True)

        tainted_jar: str = tempfile.mktemp(".jar")
        tainted_mapped_jar: str = tempfile.mktemp(".jar")
        taint_jar(get_piston_file(mc_ver, "client"), tainted_jar)

        proc = subprocess.Popen(
            [
                "java",
                "-cp",
                join(mcp_dir, "tools", "retroguard.jar"),
                "RetroGuard",
                tainted_jar,
                tainted_mapped_jar,
                join(mcp_dir, "conf", "minecraft.rgs"),
            ],
            stdout=subprocess.DEVNULL,
        )
        if proc.wait() != 0:
            raise RuntimeError("Retroguard error")
        generate_tiny(tainted_mapped_jar, out_tiny)
        os.remove(tainted_jar)

        if exists("retroguard.log"):
            os.remove("retroguard.log")

        os.remove(tainted_mapped_jar)


import csv


def load_alpha_field_csv(path: str) -> dict[str, str]:
    out = {}
    with open(path, newline="") as csvfile:
        r = csv.reader(csvfile)
        next(r)
        next(r)
        next(r)
        for row in r:
            if not len(row):
                continue
            if not len(row[2]):
                continue
            if row[2] == "*":
                continue
            out[row[2]] = row[6]
    return out


def load_alpha_method_csv(path: str) -> dict[str, str]:
    out = {}
    with open(path, newline="") as csvfile:
        r = csv.reader(csvfile)

        next(r)
        next(r)
        next(r)
        next(r)

        for row in r:
            if 4 > len(row):
                continue
            if not row[1]:
                continue
            if "*" == row[1]:
                continue
            out[row[1]] = row[4]
    return out


def tiny_renamer(mcp_fields, mcp_methods, tiny_file, ignore_conflicts : bool = False):
    new_lines = []

    field_dedup = set()
    field_dups = set()

    method_dedups = set()
    method_dups = set()

    print("[*] Renaming fields from intermediary")

    with open(tiny_file, "r") as fin:
        for line in fin.readlines():
            if line.startswith("FIELD"):
                segs = line.split("\t")
                
                if (true_name := mcp_fields.get(segs[4].rstrip())) is not None:
                    if ignore_conflicts:
                        dedup_key = f"{segs[1]}@{true_name}" 
                        if dedup_key in field_dedup:
                            field_dups.add(dedup_key)
                        else:
                            field_dedup.add(dedup_key)

                    segs[4] = true_name + "\n"
                new_lines.append("\t".join(segs))
            elif line.startswith("METHOD"):
                segs = line.split("\t")
                if (true_name := mcp_methods.get(segs[4].rstrip())) is not None:
                    if ignore_conflicts:
                        dedup_key = f"{segs[1]}@{segs[2]}:{true_name}"
                        if dedup_key in method_dedups:
                            method_dups.add(dedup_key)
                        else:
                            method_dedups.add(dedup_key)


                    segs[4] = true_name + "\n"

                new_lines.append("\t".join(segs))
            else:
                new_lines.append(line)

    if ignore_conflicts and (len(field_dups) or len(method_dups)):
        print("[*] Duplicate fields and/or methods detected, repairing!")
        new_new_lines = []
        for line in new_lines:
            if line.startswith("FIELD"):
                segs = line.split("\t")
                dedup_key = f"{segs[1]}@{segs[4]}" 

                # Use the official name to try to have the day
                if dedup_key in field_dups:
                    segs[4] += f"_{segs[3]}"
                new_new_lines.append("\t".join(segs))
            elif line.startswith("METHOD"):
                segs = line.split("\t")
                dedup_key = f"{segs[1]}@{segs[2]}:{segs[4].rstrip()}"
                if dedup_key in method_dups:
                    segs[4] = segs[4].rstrip() + f"_{segs[3]}\n"

                new_new_lines.append("\t".join(segs))
            else:
                new_new_lines.append(line)
        new_lines = new_new_lines

    with open(tiny_file, "w") as fout:
        fout.writelines(new_lines)
    print("[*] Finished renaming operations")
 
 





# Used in 1.2.1_01-TODO
# Lacks methods and fields, using a proto intermediary
def style_alpha(mcp_zip, mc_versions: list[tuple[str, str]], ignore_conflicts:bool=False):
    mcp_dir = None
    mcp_fields = {}
    mcp_methods = {}
    for mc_ver, out_tiny in mc_versions:
        if exists(out_tiny):
            continue

        if mcp_dir is None:
            mcp_dir = get_mcp_temp(mcp_zip)
            mcp_fields = load_alpha_field_csv(join(mcp_dir, "conf", "fields.csv"))
            mcp_methods = load_alpha_method_csv(join(mcp_dir, "conf", "methods.csv"))
            print(f"=========== {basename(mcp_zip)}: Style Alpha ===========")

        print(f"[*] Running for {mc_ver}")
        os.makedirs(dirname(out_tiny), exist_ok=True)

        tainted_jar: str = tempfile.mktemp(".jar")
        tainted_mapped_jar: str = tempfile.mktemp(".jar")
        taint_jar(get_piston_file(mc_ver, "client"), tainted_jar)

        proc = subprocess.Popen(
            [
                "java",
                "-cp",
                join(mcp_dir, "tools", "retroguard.jar"),
                "RetroGuard",
                tainted_jar,
                tainted_mapped_jar,
                join(mcp_dir, "conf", "minecraft.rgs"),
            ],
            stdout=subprocess.DEVNULL,
        )
        if proc.wait() != 0:
            raise RuntimeError("Retroguard error")
        generate_tiny(tainted_mapped_jar, out_tiny)

        tiny_renamer(mcp_fields, mcp_methods, out_tiny, ignore_conflicts=ignore_conflicts)

        os.remove(tainted_jar)

        if exists("retroguard.log"):
            os.remove("retroguard.log")

        os.remove(tainted_mapped_jar)


if __name__ == "__main__":

    stdname = lambda zip, versions, *args: (
        join("complete_packs", zip),
        [
            (
                version,
                join(
                    "tiny_v1s",
                    dirname(zip),
                    f"{version}-{splitext(basename(zip))[0]}.tiny",
                ),
                *args
            )
            for version in versions
        ],
    )

    style_retroguard_old(*stdname("a1.1.2/revengpack16.zip", ["a1.1.2"]))
    for zip, versions, *args in [
        ("a1.2.1_01/mcp20.zip", ["a1.2.1_01"]),
        ("a1.2.1_01/mcp20a.zip", ["a1.2.1_01"]),

        # Note: the a versions are debug releases
        ("a1.2.2/mcp21.zip", ["a1.2.2a", "a1.2.2b"], True),
        ("a1.2.2/mcp22.zip", ["a1.2.2a", "a1.2.2b"], True),
        ("a1.2.2/mcp22a.zip", ["a1.2.2a", "a1.2.2b"], True),

        ("a1.2.3_04/mcp23.zip", ["a1.2.3_02"]),

        ("a1.2.5/mcp24.zip", ["a1.2.5"]),

        ("a1.2.6/mcp25.zip", ["a1.2.6"])

    ]:
        style_alpha(*stdname(zip, versions), *args)

