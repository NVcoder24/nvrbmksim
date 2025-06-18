from utils import *

data = readcsv()

with open("LUA/mnemo.lua", "w") as f:
    f.write("")

ii = 0
with open("LUA/mnemo.lua", "a") as f:
    for i in data.keys():
        for j in data[i]:
            if "mnemo" in j["name"]:
                a = getglobalpos(i, j["pos"])
                print(a)
                f.write(f"newmodel{ii} = workspace.prefabs.mnemo300{'200' if '200' in j['name'] else '300'}:clone()\n")
                f.write(f"newmodel{ii}:PivotTo(CFrame.new({a[0][0]}, {a[0][1]}, {a[0][2]}) * CFrame.fromEulerAngles(0, math.rad({pan_rot - 90 - a[1]}), 0) * CFrame.fromEulerAngles(0, 0, math.rad(15)))\n")
                f.write(f"newmodel{ii}.Parent = workspace.devices.mnemo\n")
                ii += 1