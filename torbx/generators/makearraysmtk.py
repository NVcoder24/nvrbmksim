import json

arr = {}

with open("mtk_posses_str.json", "r") as f:
    a = json.loads(f.read())
    for i in a:
        val = a[i]
        a1 = i.split("_")
        mtk_num = int(a1[0])
        x = int(a1[1])
        y = int(a1[2])
        if mtk_num not in arr.keys():
            arr[mtk_num] = {}
        if x not in arr[mtk_num].keys():
            arr[mtk_num][x] = {}
        arr[mtk_num][x][y] = val

def recurse_shit(a):
    if type(a) == int:
        return f"{a}"
    else:
        r = []
        for i in a.keys():
            r.append("["+f"{i}"+"]"+f" = {recurse_shit(a[i])}")
        return "{"+",".join(r)+"}"

r = f"mtkdata.nxy_to_i = {recurse_shit(arr)}"

with open("mtkdata.lua", "w") as f:
    f.write("local mtkdata = {}")

with open("mtkdata.lua", "a") as f:
    f.write("\n")
    f.write("\n")
    f.write(r)

def isexists(x, y):
    if f"1_{x}_{y}" in a.keys():
        return True
    return False

with open("mtkcolors.json", "r") as f:
    mtkcolors = json.loads(f.read())

def isexistsreal(x, y):
    try:
        if mtkcolors[y - 1][x - 1] not in ["", "g"]:
            return True
    except Exception as e:
        pass
    return False

ord_shit = "{"

for y in range(0, 50):
    for x in range(0, 50):
        if isexists(x, y):
            ord_shit += "{" + f"{x},{y}" + "},"

ord_shit += "}"

with open("mtkdata.lua", "a") as f:
    f.write("\n")
    f.write("\n")
    f.write("mtkdata.order = " + ord_shit)


ord_grp = [
    [[0, 5],
    [1, 5],
    [2, 5],
    [0, 4],
    [1, 4],
    [2, 4],
    [0, 3],
    [1, 3],
    [2, 3],],
    [[0, 0],
    [1, 0],
    [2, 0],
    [0, 1],
    [1, 1],
    [2, 1],
    [0, 2],
    [1, 2],
    [2, 2],],
    [[5, 0],
    [4, 0],
    [3, 0],
    [5, 1],
    [4, 1],
    [3, 1],
    [5, 2],
    [4, 2],
    [3, 2],],
    [[5, 5],
    [4, 5],
    [3, 5],
    [5, 4],
    [4, 4],
    [3, 4],
    [5, 3],
    [4, 3],
    [3, 3],]
]

ordcool = []

for i in ord_grp[0]:
    for y in [ 7 - i for i in range(0, 8)]:
        for x in range(0, 8):
            r = [i[0] * 8 + x + 1, i[1] * 8 + y + 1]
            if isexistsreal(r[0], r[1]):
                ordcool.append(r)

for i in ord_grp[1]:
    for y in range(0, 8):
        for x in range(0, 8):
            r = [i[0] * 8 + x + 1, i[1] * 8 + y + 1]
            if isexistsreal(r[0], r[1]):
                ordcool.append(r)

for i in ord_grp[2]:
    for y in range(0, 8):
        for x in [ 7 - i for i in range(0, 8)]:
            r = [i[0] * 8 + x + 1, i[1] * 8 + y + 1]
            if isexistsreal(r[0], r[1]):
                ordcool.append(r)

for i in ord_grp[3]:
    for y in [ 7 - i for i in range(0, 8)]:
        for x in [ 7 - i for i in range(0, 8)]:
            r = [i[0] * 8 + x + 1, i[1] * 8 + y + 1]
            if isexistsreal(r[0], r[1]):
                ordcool.append(r)

ordcoolstr = "{"

for i in ordcool:
    ordcoolstr += "{"+f"{i[0]},{i[1]}"+"},"

ordcoolstr += "}"

with open("mtkdata.lua", "a") as f:
    f.write("\n")
    f.write("\n")
    f.write("mtkdata.orderreal = " + ordcoolstr)

with open("mtkdata.lua", "a") as f:
    f.write("\n")
    f.write("\n")
    f.write("return mtkdata")
