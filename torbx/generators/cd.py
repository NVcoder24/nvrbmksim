from utils import *

data = readcsv()

with open("LUA/cd.lua", "w") as f:
    f.write("")

ii = 0
with open("LUA/cd.lua", "a") as f:
    for i in data.keys():
        for j in data[i]:
            if "cd_part1" in j["name"]:
                if ispult(i):
                    a = getglobalpos_pult(i, j["pos"])
                    f.write(f"newmodel{ii} = workspace.prefabs.cd_part1_fix:clone()\n")
                    f.write(f"newmodel{ii}:PivotTo(CFrame.new({a[0][0]}, {a[0][1]}, {a[0][2]}) * CFrame.fromEulerAngles(0, math.rad({pul_rot + 90 - a[1]}), 0) * CFrame.fromEulerAngles(math.rad({-5}), 0, 0){ ' * CFrame.fromEulerAngles(math.rad(-75), 0, 0)' if isside(i) else '' })\n")
                    f.write(f"newmodel{ii}.Parent = workspace.devices.cd\n")
                    ii += 1
            if "cd_part2" in j["name"]:
                if ispult(i):
                    a = getglobalpos_pult(i, j["pos"])
                    f.write(f"newmodel{ii} = workspace.prefabs.cd_part2_fix:clone()\n")
                    f.write(f"newmodel{ii}:PivotTo(CFrame.new({a[0][0]}, {a[0][1]}, {a[0][2]}) * CFrame.fromEulerAngles(0, math.rad({pul_rot + 90 - a[1]}), 0) * CFrame.fromEulerAngles(math.rad({-5}), 0, 0){ ' * CFrame.fromEulerAngles(math.rad(-75), 0, 0)' if isside(i) else '' })\n")
                    f.write(f"newmodel{ii}.Parent = workspace.devices.cd\n")
                    ii += 1