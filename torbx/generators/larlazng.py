from utils import *
import random
import json

mtk_colors = []

mtk_colors_x = []
mtk_colors_y = []

with open("larlazng.csv", "r") as f:
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

c = [
    "0011100",
    "0111110",
    "1111111",
    "1111111",
    "1111111",
    "0111110",
    "0011100",
]

c_coords = []

for y in range(7):
    for x in range(7):
        v = c[y][x]
        if v == "1":
            c_coords.append([x-3,y-3])

reac = []

for i in range(48):
    reac.append([])
    for j in range(48):
        reac[-1].append([])

for y in range(len(mtk_colors)):
    for x in range(len(mtk_colors[y])):
        v = mtk_colors[y][x]
        if v != "" and v != "0":
            for i in c_coords:
                nx = x + i[0]
                ny = y + i[1]
                if nx >= 0 and nx < 48 and ny >= 0 and ny < 48:
                    if mtk_colors[ny][nx] != "0":
                        reac[ny][nx].append(v)
#print(luaser(a))

with open("larngtest.csv", "w") as f:
    f.write( "\n".join(
        [ 
            ",".join([
                " ".join(x) 
                for x in y
            ])
            for y in reac
        ]
    ) )

res = {}

for i in range(1,13):
    res[i]={}
    for j in range(1,5):
        res[i][j]=[]

for y in range(48):
    for x in range(48):
        for i in reac[y][x]:
            a = i.split("_")
            res[ int(a[0]) ][ int(a[1]) ].append([x+1,y+1])

with open("larlazng.lua", "w") as f:
    f.write("\n".join(
        f"larlazng.d{i} = {luaser(res[i])}" for i in res
    ))
