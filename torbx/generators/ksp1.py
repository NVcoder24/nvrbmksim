from utils import *

data = readcsv()

with open("LUA/ksp1.lua", "w") as f:
    f.write("")

ii = 0
with open("LUA/ksp1.lua", "a") as f:
    for i in data.keys():
        for j in data[i]:
            if "ksp1" in j["name"]:
                a = getglobalpos(i, j["pos"])
                f.write(f"newmodel{ii} = workspace.prefabs.ksp1:clone()\n")
                f.write(f"newmodel{ii}:PivotTo(CFrame.new({a[0][0]}, {a[0][1]}, {a[0][2]}) * CFrame.fromEulerAngles(0, math.rad({-90 - a[1] + pan_rot}), 0))\n")
                f.write(f"newmodel{ii}.Parent = workspace.devices.ksp1\n")
                ii += 1