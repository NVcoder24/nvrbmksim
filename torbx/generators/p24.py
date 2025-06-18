from utils import *

data = readcsv()

with open("LUA/p24.lua", "w") as f:
    f.write("")

with open("LUA/p24.lua", "a") as f:
    for i in data.keys():
        for j in data[i]:
            if "p24" in j["name"]:
                a = getglobalpos(i, j["pos"])
                f.write(f"workspace.devices.p24:PivotTo(CFrame.new({a[0][0]}, {a[0][1]}, {a[0][2]}) * CFrame.fromEulerAngles(0, math.rad({-90 - a[1] + pan_rot}), 0))\n")
            if "p25" in j["name"]:
                a = getglobalpos(i, j["pos"])
                f.write(f"workspace.devices.p25:PivotTo(CFrame.new({a[0][0]}, {a[0][1]}, {a[0][2]}) * CFrame.fromEulerAngles(0, math.rad({-90 - a[1] + pan_rot}), 0))\n")
            if "e1" in j["name"]:
                a = getglobalpos_pult(i, j["pos"])
                f.write(f"workspace.devices.e1:PivotTo(CFrame.new({a[0][0]}, {a[0][1]}, {a[0][2]}) * CFrame.fromEulerAngles(0, math.rad({pul_rot + 90 - a[1]}), 0) * CFrame.fromEulerAngles(math.rad({-5}), 0, 0))\n")
            if "e2" in j["name"]:
                a = getglobalpos_pult(i, j["pos"])
                f.write(f"workspace.devices.e2:PivotTo(CFrame.new({a[0][0]}, {a[0][1]}, {a[0][2]}) * CFrame.fromEulerAngles(0, math.rad({pul_rot + 90 - a[1]}), 0) * CFrame.fromEulerAngles(math.rad({-5}), 0, 0))\n")