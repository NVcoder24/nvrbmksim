from utils import *
import random
import json

mtk_colors = []

mtk_colors_x = []
mtk_colors_y = []

with open("larlaz.csv", "r") as f:
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

a = {}

for y in range(len(mtk_colors)):
    for x in range(len(mtk_colors[y])):
        v = mtk_colors[y][x]
        if v != "":
            a1 = v.split("_")
            ch = int(a1[0])
            n = int(a1[1])
            if ch not in a.keys():
                a[ch] = {}
            a[ch][n] = [x+1,y+1,0]

print(luaser(a))