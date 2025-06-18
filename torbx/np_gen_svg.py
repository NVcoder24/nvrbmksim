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
                    selsins_x.append(l[x].strip())
            else:
                if x == 0:
                    selsins_y.append(l[x].strip())
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

W = 800
H = 300
FSIZE = 350
YFIX = -25

font_path = "GOST2930-62PART1.ttf"

font = ImageFont.truetype(font_path, FSIZE)
import numpy as np
for y in range(len(selsins_result)):
    for x in range(len(selsins_result[y])):
            if len(selsins_result[y][x]) == 0:
                continue
            if selsins_result[y][x][0] in allow:
                img = Image.new('RGBA', (W, H), (0, 0, 0, 0))
                draw = ImageDraw.Draw(img)
                fn = f"npshit/SEL_NP_{y}-{x}.png"
                s = f"{selsins_y[y]}-{selsins_x[x]}"
                #w, h = draw.textsize(s, font=font)
                draw.text(((W / 2), (H / 2) + YFIX), s, font=font, fill=(0,0,0), anchor="mm")
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

                print(W - max_ - min_)
                img = ImageChops.offset(img, int((W - max_ - min_) / 2), 0)

                img.save(fn)