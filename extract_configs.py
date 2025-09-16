"""
Go through and extract all the configs.

"""
import subprocess, os
import sys




for x in os.listdir("complete_packs"):
    for z in os.listdir(os.path.join("complete_packs", x)):

        extra = []
        sep = '/'
        if z in ["mcp20.zip", "mcp20a.zip", "mcp23.zip", "mcp21.zip", "mcp25.zip", "mcp24.zip"]:
            extra = []
            sep = '\\\\'
        if x == "a1.1.2" and z != "revengpack16.zip":
            continue

        if x == "a1.1.2" and z == "revengpack16.zip":
            sep = '\\\\'


        out = os.path.join("configs", x, z.split(".")[0])
        os.makedirs(out)
        p = subprocess.Popen(["unzip",
                  "-j", '-q', *extra,
                    os.path.join("complete_packs", x, z),
                    f'conf{sep}*',
                    "-x", f"conf{sep}*{sep}",'*.patch',
                     "-d", 
                     out
                ], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        p.wait()
        if len(os.listdir(out)) == 0:
            print("Error on", x, z)
            sys.stdout.buffer.write(p.stderr.read())
