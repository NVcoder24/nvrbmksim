from utils import *

data = readcsv()

with open("LUA/lplace.lua", "w") as f:
    f.write("")

ii = 0
with open("LUA/lplace.lua", "a") as f:
    for i in data.keys():
        if i not in ["p17", "p18", "p19", "p20", "p21", "p22", "p23", "p24", "p25"]: continue
        for j in data[i]:
            if "lplace" in j["name"]:
                if ispult(i):
                    s = j["scale"]
                    np = j["pos"]
                    a = getglobalpos_pult(i, np)
                    f.write(f"newmodel{ii} = Instance.new('Part')\n")
                    f.write(f"newmodel{ii}:PivotTo(CFrame.new({a[0][0]}, {a[0][1]}, {a[0][2]}) * CFrame.fromEulerAngles(0, math.rad({pul_rot + 90 - a[1]}), 0) * CFrame.fromEulerAngles(math.rad({-5 if isside(i) else 85}), 0, 0){ ' * CFrame.fromEulerAngles(math.rad(-75), 0, 0)' if isside(i) else '' })\n")
                    f.write(f"newmodel{ii}.Parent = workspace.devices.lplace\n")
                    f.write(f"newmodel{ii}.Material = Enum.Material.SmoothPlastic\n")
                    f.write(f"newmodel{ii}.Color = Color3.fromRGB(255, 255, 255)\n")
                    f.write(f"newmodel{ii}.Size = Vector3.new({-s[1] * .146 * 2 * 10}, {s[0] * .146 * 2 * 10}, {s[2] * .146 * 2 * 10})\n")
                    f.write(f"newmodel{ii}.Anchored = true\n")
                else:
                    s = j["scale"]
                    np = j["pos"]
                    np[2] = -np[2]
                    a = getglobalpos(i, np)
                    f.write(f"newmodel{ii} = Instance.new('Part')\n")
                    f.write(f"newmodel{ii}:PivotTo(CFrame.new({a[0][0]}, {a[0][1]}, {a[0][2]}) * CFrame.fromEulerAngles(0, math.rad({-90 - a[1] + pan_rot}), 0) * CFrame.fromEulerAngles(math.rad(-90), 0, math.rad(90)))\n")
                    f.write(f"newmodel{ii}.Parent = workspace.devices.lplace\n")
                    f.write(f"newmodel{ii}.Material = Enum.Material.SmoothPlastic\n")
                    f.write(f"newmodel{ii}.Color = Color3.fromRGB(255, 255, 255)\n")
                    f.write(f"newmodel{ii}.Size = Vector3.new({s[0] * .146 * 2 * 10}, {s[2] * .146 * 2 * 10}, {s[1] * .146 * 2 * 10})\n")
                    f.write(f"newmodel{ii}.Anchored = true\n")
                    ii += 1