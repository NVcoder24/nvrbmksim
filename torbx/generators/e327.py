from utils import *

data = readcsv()

with open("LUA/e327.lua", "w") as f:
    f.write("")

ii = 0
with open("LUA/e327.lua", "a") as f:
    for i in data.keys():
        for j in data[i]:
            if "e327" in j["name"]:
                if ispult(i):
                    a = getglobalpos_pult(i, j["pos"])
                    f.write(f"newmodel{ii} = workspace.prefabs.e327:clone()\n")
                    f.write(f"newmodel{ii}:PivotTo(CFrame.new({a[0][0]}, {a[0][1]}, {a[0][2]}) * CFrame.fromEulerAngles(0, math.rad({pul_rot + 90 - a[1]}), 0) * CFrame.fromEulerAngles(math.rad({-5}), 0, 0){ ' * CFrame.fromEulerAngles(math.rad(-75), 0, 0)' if isside(i) else '' })\n")
                    f.write(f"newmodel{ii}.Parent = workspace.devices.e327\n")
                    ii += 1
                else:
                    np = j["pos"]
                    np[2] = -np[2]
                    a = getglobalpos(i, np)
                    f.write(f"newmodel{ii} = workspace.prefabs.e327:clone()\n")
                    f.write(f"newmodel{ii}:PivotTo(CFrame.new({a[0][0]}, {a[0][1]}, {a[0][2]}) * CFrame.fromEulerAngles(0, math.rad({-90 - a[1] + pan_rot}), 0) * CFrame.fromEulerAngles(math.rad(-90), 0, math.rad(90)))\n")
                    f.write(f"newmodel{ii}.Parent = workspace.devices.e327\n")
                    ii += 1