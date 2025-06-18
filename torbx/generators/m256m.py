from utils import *

data = readcsv()

with open("LUA/m256m.lua", "w") as f:
    f.write("")

ii = 0
with open("LUA/m256m.lua", "a") as f:
    for i in data.keys():
        for j in data[i]:
            if "m256m" in j["name"] and "handle" not in j["name"]:
                a = getglobalpos_pult(i, j["pos"])
                f.write(f"newmodel{ii} = workspace.prefabs.m265m:clone()\n")
                f.write(f"newmodel{ii}:PivotTo(CFrame.new({a[0][0]}, {a[0][1]}, {a[0][2]}) * CFrame.fromEulerAngles(0, math.rad({pul_rot + 90 - a[1]}), 0) * CFrame.fromEulerAngles(math.rad({-5}), 0, 0){ ' * CFrame.fromEulerAngles(math.rad(-75), 0, 0)' if isside(i) else '' })\n")
                f.write(f"newmodel{ii}.Parent = workspace.devices.pamir\n")
                ii += 1