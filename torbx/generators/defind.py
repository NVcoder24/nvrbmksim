from utils import *
import random

data = readcsv()

with open("LUA/defind.lua", "w") as f:
    f.write("")

ii = 0
with open("LUA/defind.lua", "a") as f:
    for i in data.keys():
        for j in data[i]:
            if "defind" in j["name"]:
                a = getglobalpos(i, j["pos"])
                if j["ccolor"] != "":
                    f.write(f"newmodel{ii} = workspace.prefabs.defind_{j['ccolor']}:clone()\n")
                else:
                    f.write(f"newmodel{ii} = workspace.prefabs.defind:clone()\n")
                f.write(f"newmodel{ii}:PivotTo(CFrame.new({a[0][0]}, {a[0][1]}, {a[0][2]}) * CFrame.fromEulerAngles(0, math.rad({-90 - a[1] + pan_rot}), 0))\n")
                f.write(f"newmodel{ii}.Parent = workspace.devices.definds\n")
                f.write(f"newmodel{ii}.RandBr.Value = {random.uniform(0, .6)}\n")
                ii += 1