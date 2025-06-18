#from utils import *

DEBUG = True
from PIL import Image, ImageFont, ImageDraw, ImageChops
import math
import math
import json

selsins = []

selsins_x = []
selsins_y = []

with open("selsins.csv", "r") as f:
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

np_colors = []

np_colors_x = []
np_colors_y = []

with open("bnp.csv", "r", encoding="UTF-8") as f:
    lines = f.readlines()
    for y in range(len(lines)):
        l = lines[y].split(",")
        if y > 0:
            np_colors.append([])
        for x in range(len(l)):
            if y == 0:
                if x > 0:
                    np_colors_x.append(l[x].strip())
            else:
                if x == 0:
                    np_colors_y.append(l[x].strip())
                else:
                    np_colors[y - 1].append(l[x].strip())

shit = []
with open("bnp_lbl2.csv", "r", encoding="UTF-8") as f:
    lines = f.readlines()
    for y in range(len(lines)):
        l = lines[y].split(",")
        if y > 0:
            shit.append([])
        for x in range(len(l)):
            if y == 0:
                if x > 0:
                    pass
            else:
                if x == 0:
                    pass
                else:
                    shit[y - 1].append(l[x].strip())

W = 600
H = 600
FSIZE = 200
YFIX = -11

font_path = "GOST2930-62PART1.ttf"

font = ImageFont.truetype(font_path, FSIZE)
import numpy as np
for y in range(len(np_colors)):
        for x in range(len(np_colors[y])):
            c = np_colors[y][x]
            lbl = shit[y][x]
            if c != "":
                n = ""
                try:
                    n = selsins.selsins_result[y][x][0]
                except Exception as e:
                    pass
                img = Image.new('RGBA', (W, H), (255, 255, 255, 0))
                draw = ImageDraw.Draw(img)
                fn = f"BR/NPBTN_{y}-{x}.png"
                s = f"{selsins_y[y]}-{selsins_x[x]}"
                if len(lbl) > 1:
                    if lbl == "CLEAR":
                        s = ""
                    else:
                        s = f'{lbl}'
                #w, h = draw.textsize(s, font=font)
                color = (255,255,255)
                if c == "b": color = (255,255,255)
                draw.text(((W / 2), (H / 2) + YFIX), s, font=font, fill=color, anchor="mm")
                max_ = 0
                min_ = W
                for y_ in np.array(img):
                    x__ = 0
                    for x_ in y_:
                        if x_[3] > 0:
                            if x__ > max_:
                                max_ = x__
                            if x__ < min_:
                                min_ = x__
                        x__ += 1

                print(fn, W - max_ - min_)
                img = ImageChops.offset(img, int((W - max_ - min_) / 2), 0)

                img.save(fn)