from utils import *

selsins = []

selsins_x = []
selsins_y = []

with open("1234ar.csv", "r") as f:
    lines = f.readlines()
    for y in range(len(lines)):
        l = lines[y].split(",")
        if y > 0:
            selsins.append([])
        for x in range(len(l)):
            if y == 0:
                if x > 0:
                    selsins_x.append(l[x])
            else:
                if x == 0:
                    selsins_y.append(l[x])
                else:
                    selsins[y - 1].append(l[x].strip())

selsins_result = []
for y in range(len(selsins)):
    selsins_result.append([])
    for x in range(len(selsins[y])):
        selsins_result[-1].append([])
        s = selsins[y][x]
        if s != "":
            selsins_result[-1].pop()
            selsins_result[-1].append([s, f"{selsins_y[y]}·{selsins_x[x]}"])

allow = ["g", "r", "y", "gr", "b", "w", "RE"]
defs = ["g", "r", "gr", "b", "w"]
cols = {
    "g": "Color3.fromRGB(106, 105, 107)",
    "r": "Color3.fromRGB(121, 0, 2)",
    "gr": "Color3.fromRGB(0, 77, 0)",
    "b": "Color3.fromRGB(0, 63, 97)",
    "w": "Color3.fromRGB(236, 232, 182)",
}

"""
register_selsins("#selsins_part1", 0, 6, 96.2, 70.65);
            register_selsins("#selsins_part2", 6, 17, 96.2, 70.65);
            register_selsins("#selsins_part3", 17, 23, 96.2, 70.65);
"""

ox = 96.2
oy = 70.65
hs = 95 / 2

lar = {}
ar1 = {}
ar2 = {}
arm = {}

shit = []
id_ = 1
for y in range(len(selsins_result)):
    for x in range(len(selsins_result[y])):
        if len(selsins_result[y][x]) == 0:
            continue
        v = selsins_result[y][x][0]
        print(v)
        if v[0] == "1":
            ar1[int(v[1:])] = id_
        if v[0] == "2":
            ar2[int(v[1:])] = id_
        if v[0] == "3":
            arm[int(v[1:])] = id_
        if v[0] == "4":
            lar[int(v[1:])] = id_
        id_ += 1

sel_conv = "{" + ",".join([ "{" + f"{i[0]},{i[1]}" + "}" for i in shit ]) + "}"

print(arm)

print("local ar1 = ", luaser(ar1))
print("local ar2 = ", luaser(ar2))
print("local arm = ", luaser(arm))
print("local lar = ", luaser(lar))

#print("{" + ",".join([ f"{i}" for i in az ]) + "}")
#print("{" + ",".join([ f"{i}" for i in usp ]) + "}")
#print("{" + ",".join([ f"{i}" for i in pk ]) + "}")