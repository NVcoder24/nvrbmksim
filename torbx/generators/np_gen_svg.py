#from utils import *

DEBUG = False

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

allow = ["g", "r", "y", "gr", "b", "w"]

XL = 40
YL = 15

XM = 11
YM = 21

W = XL * XM
H = YL * YM

MAXII = XM * YM

stuff = {}

ii = 0 
lastimgi = 0


YFIX = 4.5
FSIZE = 20

with open(f"np{lastimgi}.svg", "w") as f:
    f.write(f'''<svg width="{W}" height="{H}" xmlns="http://www.w3.org/2000/svg">
<defs>
<font-face>
<font-face-src>
<font-face-uri href="GOST2930-62PART1.ttf"/>
</font-face-src>
</font-face>
</defs>\n''')

for y in range(len(selsins_result)):
    for x in range(len(selsins_result[y])):
            if len(selsins_result[y][x]) == 0:
                continue
            if selsins_result[y][x][0] in allow:
                imgi = math.floor(ii / MAXII)
                if imgi != lastimgi:
                    with open(f"np{lastimgi}.svg", "a") as f:
                        f.write('</svg>')
                    with open(f"np{imgi}.svg", "w") as f:
                        f.write(f'''<svg width="{W}" height="{H}" xmlns="http://www.w3.org/2000/svg">
                    <defs>
                    <font-face>
                    <font-face-src>
                    <font-face-uri href="GOST2930-62PART1.ttf"/>
                    </font-face-src>
                    </font-face>
                    </defs>\n''')

                local_i = ii - imgi * MAXII
                pos_y = math.floor(local_i / XM)
                pos_x = local_i - pos_y * XM
                if DEBUG:
                    if pos_x == 0 and pos_y == 0:
                        with open(f"np{imgi}.svg", "a") as f:
                            f.write(f'<rect width="{XL}" height="{YL}" fill="#ccc" x="0" y="0" />')
                with open(f"np{imgi}.svg", "a") as f:
                    f.write(f'<text fill="#000" stroke="#000" stroke-width="0" x="{pos_x * XL + XL / 2}" y="{pos_y * YL + YL / 2 + YFIX}" font-size="16" text-anchor="middle" xml:space="preserve" style="font-family: \'GOST 2930-62 PART 1\';">{selsins_y[y]}-{selsins_x[x]}</text>')
                stuff[f"{y}-{x}"] = {
                    "imgi": imgi,
                    "x": pos_x,
                    "y": pos_y,
                }
                ii += 1
                lastimgi = imgi

with open(f"np{lastimgi}.svg", "a") as f:
    f.write('</svg>')

with open(f"np.json", "w") as f:
    f.write(json.dumps(stuff))