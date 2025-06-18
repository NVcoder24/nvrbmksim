from utils import *
import random
import json

mtk_colors = []

mtk_colors_x = []
mtk_colors_y = []

with open("bikng.csv", "r") as f:
    lines = f.readlines()
    for y in range(len(lines)):
        l = lines[y].split(",")
        if y > 0:
            mtk_colors.append([])
        for x in range(len(l)):
            if y == 0:
                if x > 0:
                    mtk_colors_x.append(l[x])
            else:
                if x == 0:
                    mtk_colors_y.append(l[x])
                else:
                    mtk_colors[y - 1].append(l[x].strip())

bik = {}

for i in range(0,25):
    bik[i] = []

for y in range(len(mtk_colors)):
    for x in range(len(mtk_colors[y])):
        v = mtk_colors[y][x]
        if len(v) > 0:
            bik[int(v)].append([x+1,y+1])

#for i in bik:
#    print(i, len(bik[i]))

with open("bikng.lua", "w") as f:
    f.write("\n".join(
        f"bikng.bik{i} = {luaser(bik[i])}" for i in bik
    ))


for i in range(25):
    print(f"local b{i}n = #bikng.bik{i}")

print()
print()
print()

for i in range(25):
    print(f"local b{i}v = get_stuff(bikng.bik{i})")

print()
print()
print()

chamb = {
    "ar1_1": [2, "knk53m"],
    "ar1_2": [8, "knk53m"],
    "ar1_3": [14, "knk53m"],
    "ar1_4": [20, "knk53m"],

    "ar2_1": [5, "knk53m"],
    "ar2_2": [11, "knk53m"],
    "ar2_3": [17, "knk53m"],
    "ar2_4": [23, "knk53m"],

    "ar3_1": [5, "knk56"],
    "ar3_2": [11, "knk56"],
    "ar3_3": [17, "knk56"],
    "ar3_4": [23, "knk56"],

    "uzs_1": [6, "knk56"],
    "uzs_2": [12, "knk56"],
    "uzs_3": [18, "knk56"],

    "uzsr_1": [7, "knk53m"],
    "uzsr_2": [19, "knk53m"],
    "uzsr_3": [1, "knk53m"],

    "kd_1": [1, "knt31"],
    "kd_2": [7, "knt31"],
    "kd_3": [13, "knt31"],
    "kd_4": [19, "knt31"],
}

for i in chamb:
    biks = [chamb[i][0]]
    for j in range(1, 3):
        c1 = chamb[i][0] + j
        c2 = chamb[i][0] - j
        if c1 > 24:
            c1 = c1 - 24
        if c2 < 1:
            c2 = 23 - c2
        biks.append(c1)
        biks.append(c2)
    print(f"workspace.RBMKSIM.values.bik.{i}.Value = minmax_{chamb[i][1]}(({ '+'.join( [ 'b'+str(j)+'v' for j in biks ] ) }) / ({ '+'.join( [ 'b'+str(j)+'n' for j in biks ] ) }) / shitnumber)")