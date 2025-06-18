from utils import *
import random
import json

mtk_colors = []

mtk_colors_x = []
mtk_colors_y = []

with open("uzsbik.csv", "r") as f:
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

uzs = {1: [],2: [],3: []}
uzsr = {1: [],2: [],3: []}

for y in range(len(mtk_colors)):
    for x in range(len(mtk_colors[y])):
        v = mtk_colors[y][x]
        if v == "11": uzs[1].append([x+1,y+1])
        if v == "12": uzs[2].append([x+1,y+1])
        if v == "13": uzs[3].append([x+1,y+1])

        if v == "31": uzsr[1].append([x+1,y+1])
        if v == "22": uzsr[2].append([x+1,y+1])
        if v == "23": uzsr[3].append([x+1,y+1])

print("bik_data.uzs_bik = ", luaser(uzs))
print("bik_data.uzsr_bik = ", luaser(uzsr))