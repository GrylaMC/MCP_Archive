"""
Copyright (C) 2026 - PsychedelicPalimpsest
Feel free to share this within the bounds of 
CC0 1.0 Universal
"""

import os

from os.path import dirname, abspath
os.chdir(dirname(dirname(abspath(__file__))))

def main():
    # Data structure: data[mc_version][mcp_version] = set(found_attributes)
    data = {}
    newer_mappings_mc_versions = set()

    # --- Helper Functions ---

    def mark_found(mc_ver, mcp_ver, attribute):
        if mc_ver not in data:
            data[mc_ver] = {}
        if mcp_ver not in data[mc_ver]:
            data[mc_ver][mcp_ver] = set()
        data[mc_ver][mcp_ver].add(attribute)

    # Standard natural sort key generator (splits text into numbers and strings)
    # Returns a list of tuples: [(0, int), (1, str), ...]
    # 0 is assigned to integers so they sort before strings (if that situation arises),
    # mostly just to allow int comparisons vs string comparisons.
    def natural_keys(text):
        out = []
        current = ""
        is_digit = False
        
        for char in text:
            if char.isdigit():
                if not is_digit and current:
                    out.append((1, current)) # 1 = String chunk
                    current = ""
                is_digit = True
            else:
                if is_digit and current:
                    out.append((0, int(current))) # 0 = Integer chunk
                    current = ""
                is_digit = False
            current += char
        
        if current:
            out.append((0, int(current)) if is_digit else (1, current))
            
        return out

    # Custom sort for Minecraft Versions: Alpha < Beta < Release
    def mc_version_sort_key(ver_str):
        # Determine Category Priority
        # 0 = Alpha (starts with 'a')
        # 1 = Beta (starts with 'b')
        # 2 = Release (starts with number or anything else)
        
        priority = 2 
        lower_ver = ver_str.lower()
        
        if lower_ver.startswith('a'):
            priority = 0
        elif lower_ver.startswith('b'):
            priority = 1
            
        # Return tuple: (Category Priority, Natural Sort breakdown)
        return (priority, natural_keys(ver_str))

    # --- Scanning Logic ---

    # 1. Scan tiny_v1s
    if os.path.isdir("tiny_v1s"):
        for mc_ver in os.listdir("tiny_v1s"):
            path = os.path.join("tiny_v1s", mc_ver)
            if os.path.isdir(path):
                for fname in os.listdir(path):
                    if fname.endswith(".tiny") and "-mcp" in fname:
                        # Parse: 1.6.1-mcp803.tiny -> 803
                        name_no_ext = fname[:-5]
                        idx = name_no_ext.rfind("-mcp")
                        if idx != -1:
                            mcp_ver = name_no_ext[idx+4:]
                            mark_found(mc_ver, mcp_ver, "tiny")

    # 2. Scan extracted_forge_configs
    if os.path.isdir("extracted_forge_configs"):
        for mc_ver in os.listdir("extracted_forge_configs"):
            path = os.path.join("extracted_forge_configs", mc_ver)
            if os.path.isdir(path):
                for item in os.listdir(path):
                    if item.startswith("mcp") and os.path.isdir(os.path.join(path, item)):
                        mcp_ver = item[3:] 
                        mark_found(mc_ver, mcp_ver, "extracted")

    # 3. Scan complete_packs
    if os.path.isdir("complete_packs"):
        for mc_ver in os.listdir("complete_packs"):
            path = os.path.join("complete_packs", mc_ver)
            if os.path.isdir(path):
                for fname in os.listdir(path):
                    if fname.startswith("mcp") and fname.endswith(".zip"):
                        mcp_ver = fname[3:-4]
                        mark_found(mc_ver, mcp_ver, "pack")

    # 4. Scan configs
    if os.path.isdir("configs"):
        for mc_ver in os.listdir("configs"):
            path = os.path.join("configs", mc_ver)
            if os.path.isdir(path):
                for item in os.listdir(path):
                    if item.startswith("mcp") and os.path.isdir(os.path.join(path, item)):
                        mcp_ver = item[3:]
                        mark_found(mc_ver, mcp_ver, "config")

    # 5. Scan newer_mappings
    if os.path.isdir("newer_mappings") and os.path.isdir(os.path.join("newer_mappings", "versions")):
        base_path = os.path.join("newer_mappings", "versions")
        for mc_ver in os.listdir(base_path):
            if os.path.isdir(os.path.join(base_path, mc_ver)):
                newer_mappings_mc_versions.add(mc_ver)
                if mc_ver not in data:
                    data[mc_ver] = {}

    # --- Report Generation ---

    lines = []
    lines.append("# Project Status Report")
    lines.append("")
    lines.append("| MC Version | MCP Version | Tiny | Configs | Pack | Extracted | Newer Maps |")
    lines.append("| :--- | :--- | :---: | :---: | :---: | :---: | :---: |")

    warnings = []

    # Sort MC versions using the custom priority key
    sorted_mc_versions = sorted(data.keys(), key=mc_version_sort_key)

    for mc in sorted_mc_versions:
        mcp_dict = data[mc]
        
        # If no specific MCP versions found (only newer_mappings present)
        if not mcp_dict:
            status_new = "✅" if mc in newer_mappings_mc_versions else "❌"
            lines.append(f"| {mc} | - | ❌ | ❌ | ❌ | ❌ | {status_new} |")
            continue

        # Sort MCP versions naturally (they are usually just numbers)
        sorted_mcp_versions = sorted(mcp_dict.keys(), key=natural_keys)

        for mcp in sorted_mcp_versions:
            attrs = mcp_dict[mcp]
            
            s_tiny = "✅" if "tiny" in attrs else "❌"
            s_conf = "✅" if "config" in attrs else "❌"
            s_pack = "✅" if "pack" in attrs else "❌"
            s_extr = "✅" if "extracted" in attrs else "❌"
            s_new = "✅" if mc in newer_mappings_mc_versions else "❌"

            lines.append(f"| {mc} | {mcp} | {s_tiny} | {s_conf} | {s_pack} | {s_extr} | {s_new} |")

            # Warning Check: Pack exists but Configs missing
            if "pack" in attrs and "config" not in attrs:
                warnings.append(f"- Warning: Pack `mcp{mcp}.zip` for `{mc}` exists, but config folder is missing.")

    if warnings:
        lines.append("")
        lines.append("## Warnings")
        for w in warnings:
            lines.append(w)

    with open("report.md", "w", encoding="utf-8") as f:
        f.write("\n".join(lines))
    
    print("report.md has been generated.")

if __name__ == "__main__":
    main()
