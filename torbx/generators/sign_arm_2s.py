from utils import *

data = readcsv()

with open("LUA/sign_arm_2s.lua", "w") as f:
    f.write("")

ii = 0
with open("LUA/sign_arm_2s.lua", "a") as f:
    for i in data.keys():
        for j in data[i]:
            if "sign_arm_2s" in j["name"] and "handle" not in j["name"]:
                if ispult(i):
                    a = getglobalpos_pult(i, j["pos"])
                    f.write(f"newmodel{ii} = workspace.prefabs.sign_arm_2s:clone()\n")
                    f.write(f"newmodel{ii}:PivotTo(CFrame.new({a[0][0]}, {a[0][1]}, {a[0][2]}) * CFrame.fromEulerAngles(0, math.rad({pul_rot + 90 - a[1]}), 0) * CFrame.fromEulerAngles(math.rad({-5}), 0, 0){ ' * CFrame.fromEulerAngles(math.rad(-75), 0, 0)' if isside(i) else '' })\n")
                    f.write(f"newmodel{ii}.Parent = workspace.devices.sign_arm_2s\n")
                    ii += 1
                else:
                    a = getglobalpos(i, j["pos"])
                    f.write(f"newmodel{ii} = workspace.prefabs.sign_arm_2s:clone()\n")
                    f.write(f"newmodel{ii}:PivotTo(CFrame.new({a[0][0]}, {a[0][1]}, {a[0][2]}) * CFrame.fromEulerAngles(0, math.rad({-90 - a[1] + pan_rot}), 0) * CFrame.fromEulerAngles(math.rad(-90), 0, math.rad(90)))\n")
                    f.write(f"newmodel{ii}.Parent = workspace.devices.sign_arm_2s\n")
                    ii += 1