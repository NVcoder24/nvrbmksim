from utils import *
import random
import json

mtk_colors = []
mtk_outer = []

mtk_colors_x = []
mtk_colors_y = []

with open("mtkcolors.csv", "r") as f:
    lines = f.readlines()
    for y in range(len(lines)):
        l = lines[y].split(",")
        if y > 0:
            mtk_colors.append([])
        for x in range(len(l)):
            if y == 0:
                if x > 0:
                    mtk_colors_x.append(l[x].strip())
            else:
                if x == 0:
                    mtk_colors_y.append(l[x].strip())
                else:
                    mtk_colors[y - 1].append(l[x].strip())

print(mtk_colors_x)
print(mtk_colors_y)

mtk_c_good_x = {}
mtk_c_good_y = {}

for i in range(len(mtk_colors_x)):
    mtk_c_good_x[mtk_colors_x[i]] = i + 1

for i in range(len(mtk_colors_y)):
    mtk_c_good_y[mtk_colors_y[i]] = i + 1

print(mtk_c_good_x)
print(mtk_c_good_y)
print()

print(luaser(mtk_c_good_x))
print(luaser(mtk_c_good_y))

with open("mtkcolors.json", "w") as f:
    f.write(json.dumps(mtk_colors))

with open("mtkouter.csv", "r") as f:
    lines = f.readlines()
    for y in lines:
        mtk_outer.append([])
        for x in y.split(","):
            if x.strip() != "":
                mtk_outer[len(mtk_outer) - 1].append(x)
            else:
                mtk_outer[len(mtk_outer) - 1].append("")

max_y = len(mtk_outer)
max_x = max([ len(i) for i in mtk_outer ])

result = []

for y in range(max_y):
    result.append([])
    for x in range(max_x):
        result[-1].append([])
        try:
            if mtk_outer[y][x] != "":
                n = mtk_outer[y][x]
                if len(n) == 3:
                    n = "0" + n
                result[-1].pop()
                result[-1].append(
                    ["o", f"{n[0:2]}·{n[2:4]}"]
                )
        except Exception as e:
            pass
        if x > 0 and y > 0:
            try:
                s = mtk_colors[y - 1][x - 1]
                if s != "":
                    result[-1].pop()
                    result[-1].append([s, f"{mtk_colors_y[y - 1]}·{mtk_colors_x[x - 1]}"])
            except Exception as e:
                pass

mtk_edges = []

with open("mtkedges.csv", "r") as f:
    lines = f.readlines()
    for y in lines:
        mtk_edges.append([])
        for x in y.split(","):
            if x.strip() != "":
                mtk_edges[len(mtk_edges) - 1].append(x)
            else:
                mtk_edges[len(mtk_edges) - 1].append("")

edges = []

for y in range(max_y):
    edges.append([])
    for x in range(max_x):
        edges[-1].append("")
        try:
            if "t" in mtk_edges[y][x]:
                edges[-1][-1] += "t"
            if "b" in mtk_edges[y][x]:
                edges[-1][-1] += "b"
            if "l" in mtk_edges[y][x]:
                edges[-1][-1] += "l"
            if "r" in mtk_edges[y][x]:
                edges[-1][-1] += "r"
        except Exception as e:
            pass

with open("LUA/mtk.lua", "w") as f:
    f.write("")

pos_to_i = {}

ii = 0
id_ = 1
with open("LUA/mtk.lua", "a") as f:    
    for y in range(len(result)):
        for x in range(len(result[y])):
            if len(result[y][x]) == 0:
                continue
            folder = "mtk1"
            a = getglobalpos("p1", [-(x * 40) / 1000, -((y + 1) * 40 + 120) / 1000, 0])
            if x > 24:
                a = getglobalpos("p2", [-((x - 25) * 40) / 1000, -((y + 1) * 40 + 120) / 1000, 0])
            #{result[y][x][0]}
            f.write(f"newmodel{ii} = workspace.prefabs.mtkind.mtkindlp_{result[y][x][0]}:clone()\n")
            f.write(f"newmodel{ii}:PivotTo(CFrame.new({a[0][0]}, {a[0][1]}, {a[0][2]}) * CFrame.fromEulerAngles(0, math.rad({-90 - a[1] + pan_rot}), 0) * CFrame.fromEulerAngles(0, math.rad(-90), 0)* CFrame.fromEulerAngles(math.rad(90), 0,0))\n")
            f.write(f"newmodel{ii}.Parent = workspace.RBMKSYS.viur.mtk.{folder}\n")
            f.write(f"newmodel{ii}.RandBr.Value = {random.uniform(0, .6)}\n")
            pos_to_i[f"1_{x}_{y}"] = id_
            ii += 1
            id_ += 1

id_ = 1
with open("LUA/mtk.lua", "a") as f:    
    for y in range(len(result)):
        for x in range(len(result[y])):
            if len(result[y][x]) == 0:
                continue
            folder = "mtk2"
            a = getglobalpos("p7", [-(x * 40) / 1000, -((y + 1) * 40 + 120) / 1000, 0])
            if x > 24:
                a = getglobalpos("p8", [-((x - 25) * 40) / 1000, -((y + 1) * 40 + 120) / 1000, 0])
            #{result[y][x][0]}
            f.write(f"newmodel{ii} = workspace.prefabs.mtkind.mtkindlp_{result[y][x][0]}:clone()\n")
            f.write(f"newmodel{ii}:PivotTo(CFrame.new({a[0][0]}, {a[0][1]}, {a[0][2]}) * CFrame.fromEulerAngles(0, math.rad({-90 - a[1] + pan_rot}), 0) * CFrame.fromEulerAngles(0, math.rad(-90), 0)* CFrame.fromEulerAngles(math.rad(90), 0,0))\n")
            f.write(f"newmodel{ii}.Parent = workspace.RBMKSYS.viur.mtk.{folder}\n")
            f.write(f"newmodel{ii}.RandBr.Value = {random.uniform(0, .6)}\n")
            pos_to_i[f"2_{x}_{y}"] = id_
            ii += 1
            id_ += 1

import json

with open("mtk_posses_str.json", "w") as f:
    f.write(json.dumps(pos_to_i))

with open("LUA/mtkcorners.lua", "w") as f:
    f.write("")

with open("LUA/mtkcorners.lua", "a") as f:
    for y in range(len(edges)):
        for x in range(len(edges[y])):
            if len(edges[y][x]) == 0:
                continue
            e = list(edges[y][x])
            folder = "mtkcorners"
            xoff = 0
            yoff = 0
            a = getglobalpos("p7", [-(x * 40 + xoff) / 1000, -(y * 40 + 120 + yoff) / 1000, 0])
            if x > 24:
                a = getglobalpos("p8", [-((x - 25) * 40 + xoff) / 1000, -(y * 40 + 120 + yoff) / 1000, 0])
            #{result[y][x][0]}
            if "t" in e:
                f.write(f"newmodel{ii} = workspace.prefabs.mtkc_t:clone()\n")
                f.write(f"newmodel{ii}:PivotTo(CFrame.new({a[0][0]}, {a[0][1]}, {a[0][2]}) * CFrame.fromEulerAngles(0, math.rad({-90 - a[1] + pan_rot}), 0) * CFrame.fromEulerAngles(0, math.rad(180), math.rad(-90)))\n")
                f.write(f"newmodel{ii}.Parent = workspace.devices.{folder}\n")
                ii += 1
            if "l" in e:
                f.write(f"newmodel{ii} = workspace.prefabs.mtkc_l:clone()\n")
                f.write(f"newmodel{ii}:PivotTo(CFrame.new({a[0][0]}, {a[0][1]}, {a[0][2]}) * CFrame.fromEulerAngles(0, math.rad({-90 - a[1] + pan_rot}), 0) * CFrame.fromEulerAngles(0, math.rad(180), math.rad(-90)))\n")
                f.write(f"newmodel{ii}.Parent = workspace.devices.{folder}\n")
                ii += 1
            if "r" in e:
                f.write(f"newmodel{ii} = workspace.prefabs.mtkc_r:clone()\n")
                f.write(f"newmodel{ii}:PivotTo(CFrame.new({a[0][0]}, {a[0][1]}, {a[0][2]}) * CFrame.fromEulerAngles(0, math.rad({-90 - a[1] + pan_rot}), 0) * CFrame.fromEulerAngles(0, math.rad(180), math.rad(-90)))\n")
                f.write(f"newmodel{ii}.Parent = workspace.devices.{folder}\n")
                ii += 1
            if "b" in e:
                f.write(f"newmodel{ii} = workspace.prefabs.mtkc_b:clone()\n")
                f.write(f"newmodel{ii}:PivotTo(CFrame.new({a[0][0]}, {a[0][1]}, {a[0][2]}) * CFrame.fromEulerAngles(0, math.rad({-90 - a[1] + pan_rot}), 0) * CFrame.fromEulerAngles(0, math.rad(180), math.rad(-90)))\n")
                f.write(f"newmodel{ii}.Parent = workspace.devices.{folder}\n")
                ii += 1

with open("LUA/mtkcorners.lua", "a") as f:
    for y in range(len(edges)):
        for x in range(len(edges[y])):
            if len(edges[y][x]) == 0:
                continue
            e = list(edges[y][x])
            folder = "mtkcorners"
            xoff = 0
            yoff = 0
            a = getglobalpos("p1", [-(x * 40 + xoff) / 1000, -(y * 40 + 120 + yoff) / 1000, 0])
            if x > 24:
                a = getglobalpos("p2", [-((x - 25) * 40 + xoff) / 1000, -(y * 40 + 120 + yoff) / 1000, 0])
            #{result[y][x][0]}
            if "t" in e:
                f.write(f"newmodel{ii} = workspace.prefabs.mtkc_t:clone()\n")
                f.write(f"newmodel{ii}:PivotTo(CFrame.new({a[0][0]}, {a[0][1]}, {a[0][2]}) * CFrame.fromEulerAngles(0, math.rad({-90 - a[1] + pan_rot}), 0) * CFrame.fromEulerAngles(0, math.rad(180), math.rad(-90)))\n")
                f.write(f"newmodel{ii}.Parent = workspace.devices.{folder}\n")
                ii += 1
            if "l" in e:
                f.write(f"newmodel{ii} = workspace.prefabs.mtkc_l:clone()\n")
                f.write(f"newmodel{ii}:PivotTo(CFrame.new({a[0][0]}, {a[0][1]}, {a[0][2]}) * CFrame.fromEulerAngles(0, math.rad({-90 - a[1] + pan_rot}), 0) * CFrame.fromEulerAngles(0, math.rad(180), math.rad(-90)))\n")
                f.write(f"newmodel{ii}.Parent = workspace.devices.{folder}\n")
                ii += 1
            if "r" in e:
                f.write(f"newmodel{ii} = workspace.prefabs.mtkc_r:clone()\n")
                f.write(f"newmodel{ii}:PivotTo(CFrame.new({a[0][0]}, {a[0][1]}, {a[0][2]}) * CFrame.fromEulerAngles(0, math.rad({-90 - a[1] + pan_rot}), 0) * CFrame.fromEulerAngles(0, math.rad(180), math.rad(-90)))\n")
                f.write(f"newmodel{ii}.Parent = workspace.devices.{folder}\n")
                ii += 1
            if "b" in e:
                f.write(f"newmodel{ii} = workspace.prefabs.mtkc_b:clone()\n")
                f.write(f"newmodel{ii}:PivotTo(CFrame.new({a[0][0]}, {a[0][1]}, {a[0][2]}) * CFrame.fromEulerAngles(0, math.rad({-90 - a[1] + pan_rot}), 0) * CFrame.fromEulerAngles(0, math.rad(180), math.rad(-90)))\n")
                f.write(f"newmodel{ii}.Parent = workspace.devices.{folder}\n")
                ii += 1