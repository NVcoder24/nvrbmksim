from utils import *

data = readcsv()

with open("LUA/p2p1t.lua", "w") as f:
    f.write("")

ccolor = {
    "r": "Color3.fromRGB(196, 40, 28)",
    "c": "Color3.fromRGB(0, 143, 156)",
}

ii = 0
with open("LUA/p2p1t.lua", "a") as f:
    for i in data.keys():
        for j in data[i]:
            if "p2p1t" in j["name"] and "handle" not in j["name"]:
                if ispult(i):
                    a = getglobalpos_pult(i, j["pos"])
                    if j["ccolor"]:
                        if j["ccolor"] == "r":
                            f.write(f"newmodel{ii} = workspace.prefabs.p2p1t_red:clone()\n")
                        if j["ccolor"] == "c":
                            f.write(f"newmodel{ii} = workspace.prefabs.p2p1t_cyan:clone()\n")
                    else:
                        f.write(f"newmodel{ii} = workspace.prefabs.p2p1t:clone()\n")
                    f.write(f"newmodel{ii}:PivotTo(CFrame.new({a[0][0]}, {a[0][1]}, {a[0][2]}) * CFrame.fromEulerAngles(0, math.rad({pul_rot + 90 - a[1]}), 0) * CFrame.fromEulerAngles(math.rad({-5}), 0, 0))\n")
                    f.write(f"newmodel{ii}.Parent = workspace.devices.p2p1t\n")
                    ii += 1
                else:
                    continue