"""
Copyright (C) 2026 - PsychedelicPalimpsest
Feel free to share this within the bounds of 
CC0 1.0 Universal
"""



import os, json

from os.path import join, splitext, dirname, abspath

os.chdir(dirname(dirname(abspath(__file__))))

versions = {}

for diR in sorted(os.listdir("tiny_v1s")):
    diR_name = diR
    diR = join("tiny_v1s", diR)

    for mapping in os.listdir(diR):
        mapping_path = join(diR, mapping)

        if "-mcp" in mapping:
            mc_ver, mcp_ver = mapping.split("-mcp")
        else:
            assert "-revengpack" in mapping
            mc_ver, mcp_ver = mapping.split("-revengpack")
        mcp_ver, _ = splitext(mcp_ver)

        if not mc_ver in versions:
            versions[mc_ver] = []
        versions[mc_ver].append((mapping, mcp_ver, diR_name))

versions = {
    k: [
        f"https://github.com/GrylaMC/MCP_Archive/raw/refs/heads/main/tiny_v1s/{x[2]}/{x[0]}"
        for x in sorted(v, key=lambda x: x[-1])
    ] for k, v in versions.items()
}

if __name__ == "__main__":
    print(json.dumps(versions, indent=2))
