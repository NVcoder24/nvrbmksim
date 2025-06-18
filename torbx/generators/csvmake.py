import os, sys, shutil

if getattr(sys, 'frozen', False):
    application_path = os.path.dirname(sys.executable)
elif __file__:
    application_path = os.path.dirname(__file__)

s = []

for i in os.walk(application_path + "\\stuff"):
    for j in i[2]:
        ext = j.split(".")[-1]
        if ext == "csv":
            print(i, i[0])
            with open(f"{i[0]}\\{j}", "r") as f:
                for a in f.readlines():
                    if a != "\n": s.append(a[:-1])

with open("stuff.csv", "w") as f:
    f.write("\n".join(s))