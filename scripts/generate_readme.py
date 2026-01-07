"""
Copyright (C) 2026 - PsychedelicPalimpsest
Feel free to share this within the bounds of
CC0 1.0 Universal
"""

import json, re
import os 

from os.path import dirname, abspath, exists, isfile, join, splitext


PARENT_DIR = dirname(dirname(abspath(__file__)))
os.chdir(PARENT_DIR)


COMPLETE_PACKS_DIR = join(PARENT_DIR, "complete_packs")
FORGE_EXTRACTED = "extracted_forge_configs"

GEN_FORGEBOT = "generated_forge_mcpbot_configs"
GEN_ZFFUBOT = "generated_zffu_mcpbot_configs"


TINY_V1S = join(PARENT_DIR, "tiny_v1s")



def parse_mc_version(ver_str):
    """
    Parses a Minecraft version string into a comparable tuple.
    
    Structure: (Era, Major, Minor, Patch, Snapshot_Tag, Original_String)
    
    Eras:
    0: Alpha (a1.X)
    1: Beta (b1.X) - Note: b1.9-pre is numerically high Beta.
    2: Release (1.0+)
    """
    clean_ver = ver_str.replace("@omni@", "").strip()
    
    # Defaults
    era = 2 # Default to Release
    major = 0
    minor = 0
    patch = 0
    tag = 0 # 0 for snapshot/pre, 1 for clean release (clean release sorts LAST)
    
    # 1. Determine Era
    if clean_ver.startswith('a'):
        era = 0
    elif clean_ver.startswith('b'):
        era = 1
    
    # 2. Heuristic for Year/Week Snapshots (e.g., 12w17a, 13w02b)
    # These technically belong to Era 2 but usually start with digits > 1 (e.g. 12, 13).
    # Standard releases start with 1. (e.g. 1.7.10).
    # If we sorted purely numerically, 12w (12) > 1.7 (1).
    # We map them roughly to where they belong chronologically to interleave them.
    # 11w -> ~1.1
    # 12w -> ~1.2.5+
    # 13w -> ~1.4.5+
    snapshot_match = re.search(r'^(\d\d)w', clean_ver)
    if snapshot_match:
        year = int(snapshot_match.group(1))
        era = 2
        # Rough mapping of Year to Major Version for sorting purposes
        # This ensures 12w sorts after 1.2.5 but before 1.3/1.4 logic usually picks up
        # It's not perfect but works for sorting lists.
        major = 1
        if year == 11: minor = 1
        elif year == 12: minor = 2 
        elif year == 13: minor = 5 # 13w is usually 1.5 era
        elif year >= 14: minor = year - 7 # 14w->1.7, 15w->1.8, etc
        
        # Use the whole string as the tiebreaker for snapshots
        patch = 0 
        tag = 0 
        return (era, major, minor, patch, tag, clean_ver)

    # 3. Standard Semantic Version Parsing
    # Finds sequences of numbers: 1.7.10 -> [1, 7, 10]
    nums = [int(n) for n in re.findall(r'\d+', clean_ver)]
    
    if len(nums) > 0: major = nums[0]
    if len(nums) > 1: minor = nums[1]
    if len(nums) > 2: patch = nums[2]
    
    # 4. Handle Pre-releases / Candidates (lower priority than clean)
    # If 'pre', 'rc', or 'beta' (in the suffix) is found, it's older than the clean release.
    # tag 0 = dirty/pre, tag 1 = clean
    is_dirty = re.search(r'(pre|rc|beta|snapshot)', clean_ver, re.IGNORECASE)
    tag = 0 if is_dirty else 1
    
    # Special Fix: Beta 1.9-pre is logically higher than Beta 1.8
    # The normal number sort handles this (9 > 8).
    
    return (era, major, minor, patch, tag, clean_ver)

def sort_key(item):
    mcp_ver = item.get("mcp version", "")
    mc_ver = item.get("mc version", "")

    # --- PRIMARY KEY: MC VERSION ---
    # Sorts primarily by chronological Minecraft version (Alpha -> Beta -> Release 1.1 -> 1.16)
    mc_sort_tuple = parse_mc_version(mc_ver)

    # --- SECONDARY KEY: MCP VERSION ---
    # Used to order items that share the exact same MC version.
    # Prioritizes: Known MCP ID > UNKNOWN
    
    is_unknown = 1 if mcp_ver == "UNKNOWN" else 0
    
    mcp_num = 0
    match = re.search(r'(\d+)', mcp_ver)
    if match:
        mcp_num = int(match.group(1))

    # Return tuple:
    # 1. MC Version (The Era/Time)
    # 2. Is Unknown? (Puts UNKNOWNs after defined MCPs for the same version)
    # 3. MCP Number (Puts mcp908 before mcp910 if MC versions match exactly)
    return (mc_sort_tuple, is_unknown, mcp_num)


def complete_packs_data():
    data = []
    for version_dir in os.listdir(COMPLETE_PACKS_DIR):
        version_path = join(COMPLETE_PACKS_DIR, version_dir)

        for zip_file in os.listdir(version_path):
            mcp = splitext(zip_file)[0]

            data.append(
                (
                    version_dir,
                    zip_file,
                    mcp,
                )
            )

    return data


def extracted_forge_data():
    data = []

    for version_dir in os.listdir(FORGE_EXTRACTED):
        version_path = join(FORGE_EXTRACTED, version_dir)

        if isfile(version_path):
            continue

        for config in os.listdir(version_path):
            data.append((version_dir, config))
    return data




def tiny_v1s():
    data = []

    for diR in os.listdir(TINY_V1S):
        diR_path = join(TINY_V1S, diR)

        for tiny in os.listdir(diR_path):
            assert "-mcp" in tiny or "-revengpack" in tiny
            data.append((diR, tiny, *tiny.replace("-revengpack", "-mcp").split("-mcp")))
    return data


def generate_data():
    entries = []

    completes = complete_packs_data()
    complete_mcps = {mcp: (dir, ziP, mcp) for dir, ziP, mcp in completes}

    forge = extracted_forge_data()
    forge_mcps = {mcp: (version_dir, mcp) for version_dir, mcp in forge}


    tinys = tiny_v1s()

    def complete_pack_helper(tiny):
        mcp_version = splitext(tiny[3])[0]
        if "-revengpack" in tiny[1]:
            mcp_version = "revengpack" + mcp_version
        else:
            mcp_version = "mcp" + mcp_version
        if mcp_version in complete_mcps:
            pack = complete_mcps[mcp_version]

            assert exists(join(COMPLETE_PACKS_DIR, pack[0], pack[1]))

            entries.append(
                {
                    "type": "complete mcp",
                    "mcp version": mcp_version,
                    "mc version": tiny[2],
                    "link": f"https://cdn.githubraw.com/GrylaMC/MCP_Archive/main/complete_packs/{pack[0]}/{pack[1]}",
                    "tiny": f"https://cdn.githubraw.com/GrylaMC/MCP_Archive/main/tiny_v1s/{tiny[0]}/{tiny[1]}",
                }
            )

            return False

        return True

    tinys = filter(complete_pack_helper, tinys)

    def extracted_config_helper(tiny):
        mcp_version = "mcp" + splitext(tiny[3])[0]
        if mcp_version in forge_mcps:
            conf = forge_mcps[mcp_version]

            assert exists(join(FORGE_EXTRACTED, conf[0], conf[1]))

            entries.append(
                {
                    "type": "extracted forge config",
                    "mcp version": mcp_version,
                    "mc version": tiny[2],
                    "link": f"https://github.com/GrylaMC/MCP_Archive/tree/main/{FORGE_EXTRACTED}/{conf[0]}/{conf[1]}",
                    "tiny": f"https://cdn.githubraw.com/GrylaMC/MCP_Archive/main/tiny_v1s/{tiny[0]}/{tiny[1]}",
                }
            )

            return False

        return True


    tinys = filter(extracted_config_helper, tinys)

    def zffu_helper(tiny):
        if tiny[3] != "ZFFU.tiny":
            return True
        entries.append(
        {
            "type": "zffu config",
            "mcp version": "UNKNOWN",
            "mc version": tiny[2],
            "link": f"https://github.com/GrylaMC/newer_forge_mappings/tree/main/versions/{tiny[2]}/",
            "tiny": f"https://cdn.githubraw.com/GrylaMC/MCP_Archive/main/tiny_v1s/{tiny[0]}/{tiny[1]}",
        }
        )

        return False

    tinys = filter(zffu_helper, tinys)


    def gen_mcpbot_helper(tiny):
        if not tiny[3].startswith("bot"):
            return True
        bot_path = GEN_FORGEBOT if tiny[3] == "botFORGE.tiny" else GEN_ZFFUBOT
        entry_type = "generated forge config" if tiny[3] == "botFORGE.tiny" else "generated zffu config" 

        assert exists(join(
            bot_path, tiny[2]
        ))


        entries.append(
        {
            "type": entry_type,
            "mcp version": "UNKNOWN",
            "mc version": tiny[2],
            "link": f"https://cdn.githubraw.com/GrylaMC/MCP_Archive/main/{bot_path}/{tiny[2]}/",
            "tiny": f"https://cdn.githubraw.com/GrylaMC/MCP_Archive/main/tiny_v1s/{tiny[0]}/{tiny[1]}",
        }
        )
        return False

        
    tinys = list(filter(gen_mcpbot_helper, tinys))


    assert not tinys
    return sorted(entries, key=sort_key)



def generate_readme_table(entries):
    out   = "| Finding State     |  MCP Version   |   Tiny V1    | Minecraft Version |\n"
    out +=  "|-------------------|----------------|--------------|-------------------|\n"
    


    for entry in entries:
        mc_version = entry["mc version"].replace("@omni@", "")
        mcp_version =  entry["mcp version"].replace("UNKNOWN", "")
        tiny_name = entry["tiny"].split("/")[-1]

        if entry["type"] == "complete mcp":
            status = f"🟢 Found Completely ([link]({entry['link']}))"
        elif entry["type"] == "extracted forge config":
            status = f"🟡 Early Forge Config ([link]({entry['link']}))"
        elif entry["type"] == "generated forge config":
            status = f"🟣 MCPBot/Forge config ([link]({entry['link']}))"
        elif entry["type"] == "generated zffu config":
            status = f"⚫ MCPBot/Zffu config ([link]({entry['link']}))"
        elif entry["type"] == "zffu config":
            status = f"🟤 Zffu Config ([link]({entry['link']}))"
        else:
            assert False


        out += f"| {status} | {mc_version} | {mcp_version} | [{tiny_name}]({entry['tiny']}) |\n"

    return out



def main():
    data = generate_data()
    
    with open(join(PARENT_DIR, "entries.json"), "w") as f:
        json.dump(data, f, indent=2)

    with open(join(PARENT_DIR, "README.md"), "r") as f:
        readme = f.read()

    TARGET = "----------------\n"
    pos = readme.find(TARGET)
    assert pos != -1

    pos += len(TARGET)

    readme = readme[:pos] +  generate_readme_table(data)
    with open(join(PARENT_DIR, "README.md"), "w") as f:
        f.write(readme)






if __name__ == "__main__":
    main()
