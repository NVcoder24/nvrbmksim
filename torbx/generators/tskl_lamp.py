from utils import *

data = readcsv()

with open("LUA/tskl_lamp.lua", "w") as f:
    f.write("")

ii = 0
with open("LUA/tskl_lamp.lua", "a") as f:
    for i in data.keys():
        for j in data[i]:
            if "tskl_lamp" in j["name"]:
                if ispult(i):
                    z = j["pos"]
                    #z[2] -=  0.04
                    a = getglobalpos_pult(i, z)
                    f.write(f"newmodel{ii} = workspace.prefabs.tskl_lamp:clone()\n")
                    f.write(f"newmodel{ii}:PivotTo(CFrame.new({a[0][0]}, {a[0][1]}, {a[0][2]}) * CFrame.fromEulerAngles(0, math.rad({pul_rot + 0 - a[1]}), 0) * CFrame.fromEulerAngles(0, 0, math.rad(-10)))\n")
                    f.write(f"newmodel{ii}.Parent = workspace.devices.tskl_lamp\n")
                    ii += 1
                else:
                    z = j["pos"]
                    #z[0] -=  0.04
                    a = getglobalpos(i, z)
                    f.write(f"newmodel{ii} = workspace.prefabs.tskl_lamp:clone()\n")
                    f.write(f"newmodel{ii}:PivotTo(CFrame.new({a[0][0]}, {a[0][1]}, {a[0][2]}) * CFrame.fromEulerAngles(0, math.rad({-90 - a[1] + pan_rot}), 0) * CFrame.fromEulerAngles(0, 0, math.rad(0)))\n")
                    f.write(f"newmodel{ii}.Parent = workspace.devices.tskl_lamp\n")
                    ii += 1