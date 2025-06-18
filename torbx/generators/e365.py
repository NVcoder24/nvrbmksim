from utils import *

data = readcsv()

with open("LUA/e365.lua", "w") as f:
    f.write("")

ii = 0
with open("LUA/e365.lua", "a") as f:
    for i in data.keys():
        for j in data[i]:
            if "e365" in j["name"]:
                np = j["pos"]
                np[2] = -np[2]
                a = getglobalpos(i, np)
                f.write(f"newmodel{ii} = workspace.prefabs.e365:clone()\n")
                f.write(f"newmodel{ii}:PivotTo(CFrame.new({a[0][0]}, {a[0][1]}, {a[0][2]}) * CFrame.fromEulerAngles(0, math.rad({-90 - a[1] + pan_rot}), 0))\n")
                f.write(f"newmodel{ii}.Parent = workspace.devices.e365\n")
                ii += 1