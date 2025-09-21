import os, hashlib



def report(file):
    f = open(file, "r")
    data = f.read()
    f.close()

    md5 = hashlib.md5(data.encode("utf-8")).hexdigest()

    classes = 0
    fields = 0
    methods = 0
    for l in data.split("\n"):
        if l.startswith("CLASS"):
            classes += 1
        if l.startswith("FIELD"):
            fields += 1
        if l.startswith("METHOD"):
            methods += 1
    return md5, classes, fields, methods, len(data.split("\t"))


if __name__ == "__main__":
    for diR in sorted(os.listdir("tiny_v1s")):
        full_dir = os.path.join("tiny_v1s", diR)
        print()
        print(f"{diR}\t\t\t\t\tmd5\t\t\t\t\tclasses\tfields\tmethods\tsize")
        for file in sorted(os.listdir(full_dir)):
            full_file = os.path.join(full_dir, file)
            print("\t" + file + "\t\t" + ( "\t".join(
                str(e)
                for e in report(full_file)

            )))







