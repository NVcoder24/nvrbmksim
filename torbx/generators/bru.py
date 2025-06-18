from utils import *

data = readcsv()

with open("LUA/bru.lua", "w") as f:
    f.write("")

ii = 0
with open("LUA/bru.lua", "a") as f:
    for i in data.keys():
        for j in data[i]:
            if "bruk" in j["name"]:
                a = getglobalpos_pult(i, j["pos"])
                f.write(f"newmodel{ii} = workspace.prefabs.bruk:clone()\n")
                f.write(f"newmodel{ii}:PivotTo(CFrame.new({a[0][0]}, {a[0][1]}, {a[0][2]}) * CFrame.fromEulerAngles(0, math.rad({pul_rot + 90 - a[1]}), 0) * CFrame.fromEulerAngles(math.rad({-5}), 0, 0){ ' * CFrame.fromEulerAngles(math.rad(-75), 0, 0)' if isside(i) else '' })\n")
                f.write(f"newmodel{ii}.Parent = workspace.devices.bruk\n")
                ii += 1
            if "bruu" in j["name"]:
                a = getglobalpos_pult(i, j["pos"])
                f.write(f"newmodel{ii} = workspace.prefabs.bruu:clone()\n")
                f.write(f"newmodel{ii}:PivotTo(CFrame.new({a[0][0]}, {a[0][1]}, {a[0][2]}) * CFrame.fromEulerAngles(0, math.rad({pul_rot + 90 - a[1]}), 0) * CFrame.fromEulerAngles(math.rad({-5}), 0, 0){ ' * CFrame.fromEulerAngles(math.rad(-75), 0, 0)' if isside(i) else '' })\n")
                f.write(f"newmodel{ii}.Parent = workspace.devices.bruu\n")
                ii += 1
            if "bru_2k" in j["name"]:
                a = getglobalpos_pult(i, j["pos"])
                f.write(f"newmodel{ii} = workspace.prefabs.bru_2k:clone()\n")
                f.write(f"newmodel{ii}:PivotTo(CFrame.new({a[0][0]}, {a[0][1]}, {a[0][2]}) * CFrame.fromEulerAngles(0, math.rad({pul_rot + 90 - a[1]}), 0) * CFrame.fromEulerAngles(math.rad({-5}), 0, 0){ ' * CFrame.fromEulerAngles(math.rad(-75), 0, 0)' if isside(i) else '' })\n")
                f.write(f"newmodel{ii}.Parent = workspace.devices.bru_2k\n")
                ii += 1
            if "rzd_k" in j["name"]:
                a = getglobalpos_pult(i, j["pos"])
                f.write(f"newmodel{ii} = workspace.prefabs.rzd_k:clone()\n")
                f.write(f"newmodel{ii}:PivotTo(CFrame.new({a[0][0]}, {a[0][1]}, {a[0][2]}) * CFrame.fromEulerAngles(0, math.rad({pul_rot + 90 - a[1]}), 0) * CFrame.fromEulerAngles(math.rad({-5}), 0, 0){ ' * CFrame.fromEulerAngles(math.rad(-75), 0, 0)' if isside(i) else '' })\n")
                f.write(f"newmodel{ii}.Parent = workspace.devices.rzd_k\n")
                ii += 1
                