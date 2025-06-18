from utils import *
import random
import json

mtk_colors = []

mtk_colors_x = []
mtk_colors_y = []

with open("bik_kd.csv", "r") as f:
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

kd = {1: [],2: [],3: [],4: []}

for y in range(len(mtk_colors)):
    for x in range(len(mtk_colors[y])):
        v = mtk_colors[y][x]
        if v == "1": kd[1].append([x+1,y+1])
        if v == "2": kd[2].append([x+1,y+1])
        if v == "3": kd[3].append([x+1,y+1])
        if v == "4": kd[4].append([x+1,y+1])


print("bik_data.kd = ", luaser(kd))