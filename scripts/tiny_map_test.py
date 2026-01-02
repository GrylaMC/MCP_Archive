import os, subprocess, sys
import tempfile
from os.path import abspath, dirname, exists, join

PARENT = dirname(dirname(abspath(__file__)))
os.chdir(PARENT)




SCRIPTS_DIR = join(dirname(PARENT), "utils", "scripts")
if not exists(SCRIPTS_DIR):
    raise RuntimeError("Refusing to run without use of official workspace")

sys.path.append(SCRIPTS_DIR)

from mcjar import get_piston_file, REMAPPER


def jar_map(jar_from, jar_to, mapping_file, from_name, to_name):
    resp = subprocess.Popen(["java", "-jar", REMAPPER,
                             jar_from, jar_to, mapping_file, from_name, to_name]) 

    return resp.wait()

def get_namespaces(mapping_file):
    with open(mapping_file, "r") as f:
        line = f.readline().strip()
        assert line.startswith("v1")


        _, *namespaces = line.split("\t")
        return namespaces








if __name__ == "__main__":
    with tempfile.TemporaryDirectory(delete=True) as tempdir:
        for diR in sorted(os.listdir("tiny_v1s")):
            if diR.startswith("a") or diR.startswith("b"):
                continue

            full_dir = os.path.join("tiny_v1s", diR)
            # for file in sorted(os.listdir(full_dir)):
            for file in sorted(os.listdir(full_dir)):
                full_file = os.path.join(full_dir, file)

                official, *other = get_namespaces(full_file)

                print()
                print(f"Attempting to map with {file}")

                # Fix for rengpack16
                mc_version = file.split("-mcp")[0] if "-mcp" in file else diR



                client_jar_path = get_piston_file(mc_version, "client") 
                
                for ns in other:
                    print(f"\t{ns}")
                    path = join(tempdir, file + f".{ns}.mapped.jar")
                    print(path)
                    ret = jar_map(client_jar_path, path, full_file, official, ns)
                    if ret != 0:
                        print(f"Failed to map {file} with {ns} in dir {diR}")


