from utils import *

data = readcsv()

with open("suz_js.lua", "w") as f:
    f.write("")

ii = 0
with open("suz_js.lua", "a") as f:
    for i in data.keys():
        if i != "4a":
            continue
        for j in data[i]:
            if "suz_js" in j["name"]:
                a = getglobalpos_pult(i, j["pos"])
                f.write(f"newmodel{ii} = workspace.prefabs.suz_js:clone()\n")
                f.write(f"newmodel{ii}:PivotTo(CFrame.new({a[0][0]}, {a[0][1]}, {a[0][2]}) * CFrame.fromEulerAngles(0, math.rad({pul_rot + 90 - a[1]}), 0) * CFrame.fromEulerAngles(math.rad({-5}), 0, 0))\n")
                f.write(f"newmodel{ii}.Parent = workspace.devices.suz_js\n")
                ii += 1