from os.path import exists, join
import os, sys, subprocess, tempfile

from libs.jar_marker import taint_jar, generate_tiny

sys.path.insert(0, "/home/mitch/Documents/gryla/utils/scripts")
from mcjar import get_piston_file


def get_mcp_temp(zip_file: str):
    with tempfile.TemporaryDirectory(delete=False) as f:
        if subprocess.call(["unzip", "-q", zip_file, "-d", f]) > 1:
            raise RuntimeError("Cannot unzip")
        return f


#  Only used in revengpack
def style_only_retroguard(mcp_dir, mc_versions: list[tuple[str, str]]):
    for mc_ver, out_tiny in mc_versions:
        tainted_jar = tempfile.mktemp(".jar")
        tainted_mapped_jar = tempfile.mktemp(".jar")
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
            ], stdout=subprocess.DEVNULL
        )
        if proc.wait() != 0:
            raise RuntimeError("Retroguard error")

        os.remove(tainted_jar)
        generate_tiny(tainted_mapped_jar, out_tiny)

        if exists("retroguard.log"):
            os.remove("retroguard.log")

        os.remove(tainted_mapped_jar)


if __name__ == "__main__":
    # x = get_mcp_temp("complete_packs/a1.1.2/revengpack16.zip")
    x = "/tmp/tmpjofm_g0m"
    style_only_retroguard(x, [("a1.1.2", "out.tiny")])
    pass
