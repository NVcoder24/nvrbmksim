from utils import *

data = readcsv()

with open("LUA/m1741.lua", "w") as f:
    f.write("")

ii = 0
with open("LUA/m1741.lua", "a") as f:
    for i in data.keys():
        for j in data[i]:
            if "m1741" in j["name"]:
                z = j["pos"]
                z[1] -= 0.12
                a = getglobalpos_pult(i, z)
                f.write(f"newmodel{ii} = workspace.prefabs.m1741:clone()\n")
                f.write(f"newmodel{ii}:PivotTo(CFrame.new({a[0][0]}, {a[0][1]}, {a[0][2]}) * CFrame.fromEulerAngles(0, math.rad({pul_rot + 0 - a[1]}), 0) * CFrame.fromEulerAngles(0, 0, math.rad(-10)))\n")
                f.write(f"newmodel{ii}.Parent = workspace.devices.m1741\n")
                ii += 1