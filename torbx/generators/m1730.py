from utils import *

data = readcsv()

with open("LUA/m1730.lua", "w") as f:
    f.write("")

ii = 0
with open("LUA/m1730.lua", "a") as f:
    for i in data.keys():
        for j in data[i]:
            if "m1730" in j["name"]:
                if ispult(i):
                    z = j["pos"]
                    z[1] -= 0.03
                    a = getglobalpos_pult(i, z)
                    f.write(f"newmodel{ii} = workspace.prefabs.m1730:clone()\n")
                    f.write(f"newmodel{ii}:PivotTo(CFrame.new({a[0][0]}, {a[0][1]}, {a[0][2]}) * CFrame.fromEulerAngles(0, math.rad({pul_rot + 0 - a[1]}), 0) * CFrame.fromEulerAngles(0, 0, math.rad(-10)))\n")
                    f.write(f"newmodel{ii}.Parent = workspace.devices.m1730\n")
                    ii += 1
                else:
                    z = j["pos"]
                    z[1] -= 0.03
                    a = getglobalpos(i, z)
                    f.write(f"newmodel{ii} = workspace.prefabs.m1730:clone()\n")
                    f.write(f"newmodel{ii}:PivotTo(CFrame.new({a[0][0]}, {a[0][1]}, {a[0][2]}) * CFrame.fromEulerAngles(0, math.rad({-90 - a[1] + pan_rot}), 0))\n")
                    f.write(f"newmodel{ii}.Parent = workspace.devices.m1730\n")
                    ii += 1