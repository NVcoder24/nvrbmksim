from utils import *

selsins = []

selsins_x = []
selsins_y = []

with open("bselsins_new.csv", "r") as f:
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

allow = ["g", "r", "y", "gr", "b", "w"]#, "RE"]
defs = ["g", "r", "gr", "b", "w"]
cols = {
    "g": "Color3.fromRGB(82, 78, 97)",
    "r": "Color3.fromRGB(184, 72, 27)",
    "gr": "Color3.fromRGB(18, 97, 0)",
    "b": "Color3.fromRGB(52, 129, 176)",
    "w": "Color3.fromRGB(255, 255, 255)",
}

"""
register_selsins("#selsins_part1", 0, 6, 96.2, 70.65);
            register_selsins("#selsins_part2", 6, 17, 96.2, 70.65);
            register_selsins("#selsins_part3", 17, 23, 96.2, 70.65);
"""

ox = 96.2
oy = 70.65
hs = 95 / 2
M = 0.004
with open("LUA/selsins_U3.lua", "w") as f:
    f.write("")

id_ = 1

with open("LUA/selsins_U3.lua", "a") as f:
    ii = 0
    for y in range(len(selsins_result)):
        for x in range(len(selsins_result[y])):
            if len(selsins_result[y][x]) == 0:
                continue
            if selsins_result[y][x][0] in allow:
                if selsins_result[y][x][0] == "w":
                    print(str(id_) + ",", end="")
                #if selsins_result[y][x][0] == "g":
                    #print(str(id_) + ",", end="")
                id_ += 1
                if selsins_result[y][x][0] in defs:
                    f.write(f"newmodel{ii} = workspace.scam.prefabs.sdef:clone()\n")
                    f.write(f"newmodel{ii}.Body4.Color = {cols[selsins_result[y][x][0]]}\n")
                else:
                    f.write(f"newmodel{ii} = workspace.scam.prefabs.susp:clone()\n")
                folder = "p1"
                part = "Part1"
                if x > 5:
                    folder = "p2"
                    part = "Part2"
                    f.write(f"newmodel{ii}:PivotTo(CFrame.new(workspace.scam.prefabs.{part}.CFrame.Position + Vector3.new({-((x - 6) * ox + hs) * M}, {-(y * oy + 110) * M}, 0)) * CFrame.fromEulerAngles(0, math.rad(-90), 0))\n")
                if x > 16:
                    folder = "p3"
                    part = "Part3"
                    f.write(f"newmodel{ii}:PivotTo(CFrame.new(workspace.scam.prefabs.{part}.CFrame.Position + Vector3.new({-((x - 17) * ox + hs) * M}, {-(y * oy + 110) * M}, 0)) * CFrame.fromEulerAngles(0, math.rad(-90), 0))\n")
                else:
                    f.write(f"newmodel{ii}:PivotTo(CFrame.new(workspace.scam.prefabs.{part}.CFrame.Position + Vector3.new({-((x) * ox + hs) * M}, {-(y * oy + 110) * M}, 0)) * CFrame.fromEulerAngles(0, math.rad(-90), 0))\n")
                f.write(f"newmodel{ii}.Parent = workspace.scam.selsins.s\n")
                ii += 1