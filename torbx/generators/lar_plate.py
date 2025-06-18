from utils import *

data = readcsv()

with open("LUA/lar_plate.lua", "w") as f:
    f.write("")

with open("LUA/lar_plate.lua", "a") as f:
    for i in data.keys():
        for j in data[i]:
            if "larcorrectorplate" in j["name"]:
                if ispult(i):
                    a = getglobalpos_pult(i, j["pos"])
                    f.write(f"workspace.devices.lar_plate:PivotTo(CFrame.new({a[0][0]}, {a[0][1]}, {a[0][2]}) * CFrame.fromEulerAngles(0, math.rad({pul_rot + 90 - a[1]}), 0) * CFrame.fromEulerAngles(math.rad({-5}), 0, 0))\n")