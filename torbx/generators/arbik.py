from utils import *
import random
import json

mtk_colors = []

mtk_colors_x = []
mtk_colors_y = []

with open("arbik.csv", "r") as f:
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

ar1 = {1: [],2: [],3: [],4: []}
ar2 = {1: [],2: [],3: [],4: []}
ar3 = {1: [],2: [],3: [],4: []}

for y in range(len(mtk_colors)):
    for x in range(len(mtk_colors[y])):
        v = mtk_colors[y][x]
        if v == "11": ar1[1].append([x+1,y+1])
        if v == "12": ar1[2].append([x+1,y+1])
        if v == "13": ar1[3].append([x+1,y+1])
        if v == "14": ar1[4].append([x+1,y+1])

        if v == "21": ar2[1].append([x+1,y+1])
        if v == "22": ar2[2].append([x+1,y+1])
        if v == "23": ar2[3].append([x+1,y+1])
        if v == "24": ar2[4].append([x+1,y+1])

        if v == "31": ar3[1].append([x+1,y+1])
        if v == "32": ar3[2].append([x+1,y+1])
        if v == "33": ar3[3].append([x+1,y+1])
        if v == "34": ar3[4].append([x+1,y+1])

print("bik_data.ar1_bik = ", luaser(ar1))
print("bik_data.ar2_bik = ", luaser(ar2))
print("bik_data.ar3_bik = ", luaser(ar3))