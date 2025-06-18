from utils import *

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

allow = ["g", "r", "y", "gr", "b", "w", "RE"]
defs = ["g", "r", "gr", "b", "w"]
cols = {
    "g": "Color3.fromRGB(106, 105, 107)",
    "r": "Color3.fromRGB(218, 0, 7)",
    "gr": "Color3.fromRGB(0, 112, 0)",
    "b": "Color3.fromRGB(86, 200, 218)",
    "w": "Color3.fromRGB(250, 243, 229)",
}

"""
register_selsins("#selsins_part1", 0, 6, 96.2, 70.65);
            register_selsins("#selsins_part2", 6, 17, 96.2, 70.65);
            register_selsins("#selsins_part3", 17, 23, 96.2, 70.65);
"""

ox = 96.2
oy = 70.65
hs = 95 / 2

with open("LUA/selsins.lua", "w") as f:
    f.write("")

az = []

usp = []
pk = []

shit = []
id_ = 1
with open("LUA/selsins.lua", "a") as f:
    ii = 0
    for y in range(len(selsins_result)):
        for x in range(len(selsins_result[y])):
            if len(selsins_result[y][x]) == 0:
                continue
            if selsins_result[y][x][0] in allow:
                folder = "p4"
                a = getglobalpos("p4", [-(x * ox + hs + 500) / 1000, -(y * oy + 110 + hs) / 1000, 0])
                if x > 5:
                    folder = "p5"
                    a = getglobalpos("p5", [-((x - 6) * ox + hs + 25) / 1000, -(y * oy + 110 + hs) / 1000, 0])
                if x > 16:
                    folder = "p6"
                    a = getglobalpos("p6", [-((x - 17) * ox + hs + 25) / 1000, -(y * oy + 110 + hs) / 1000, 0])
                if selsins_result[y][x][0] in defs:
                    f.write(f"newmodel{ii} = workspace.prefabs.selsin.def:clone()\n")
                    f.write(f"newmodel{ii}.Body4.Color = {cols[selsins_result[y][x][0]]}\n")
                else:
                    f.write(f"newmodel{ii} = workspace.prefabs.selsin.s_{selsins_result[y][x][0]}:clone()\n")
                f.write(f"newmodel{ii}:PivotTo(CFrame.new({a[0][0]}, {a[0][1]}, {a[0][2]}) * CFrame.fromEulerAngles(0, math.rad({-90 - a[1] + pan_rot}), 0))\n")
                if selsins_result[y][x][0]== "RE":
                    f.write(f"newmodel{ii}.Parent = workspace.devices.RE\n")
                else:
                    f.write(f"newmodel{ii}.Parent = workspace.devices.selsins\n")
                    shit.append([2 + x * 2, 2 + y * 2])
                    if selsins_result[y][x][0] == "w":
                        pk.append(id_)
                    if selsins_result[y][x][0] == "y":
                        usp.append(id_)
                    if selsins_result[y][x][0] == "r":
                        az.append(id_)
                    id_ += 1
                ii += 1

sel_conv = "{" + ",".join([ "{" + f"{i[0]},{i[1]}" + "}" for i in shit ]) + "}"

print("{" + ",".join([ f"{i}" for i in az ]) + "}")
print("{" + ",".join([ f"{i}" for i in usp ]) + "}")
print("{" + ",".join([ f"{i}" for i in pk ]) + "}")

with open("sel_conv.lua", "w") as f:
    f.write("sel_conv.sel_conv = " + sel_conv)