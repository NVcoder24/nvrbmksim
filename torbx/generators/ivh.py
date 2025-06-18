from utils import *

data = readcsv()

with open("LUA/ivh.lua", "w") as f:
    f.write("")

ii = 0
with open("LUA/ivh.lua", "a") as f:
    for i in data.keys():
        for j in data[i]:
            if "ivh" in j["name"]:
                np = j["pos"]
                #p = j["pos"]
                #np = [p[0], p[1] - .065, p[2]]
                a = getglobalpos(i, np)
                f.write(f"newmodel{ii} = workspace.prefabs.ivh:clone()\n")
                f.write(f"newmodel{ii}:PivotTo(CFrame.new({a[0][0]}, {a[0][1]}, {a[0][2]}) * CFrame.fromEulerAngles(0, math.rad({-90 - a[1] + pan_rot + 90}), 0))\n")
                f.write(f"newmodel{ii}.Parent = workspace.devices.ivh\n")
                ii += 1