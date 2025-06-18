from utils import *

data = readcsv()

with open("LUA/plate.lua", "w") as f:
    f.write("")

ii = 0
with open("LUA/plate.lua", "a") as f:
    for i in data.keys():
        for j in data[i]:
            if "plate" in j["name"]:
                if ispult(i):
                    s = j["scale"]
                    np = j["pos"]
                    a = getglobalpos_pult(i, np)
                    f.write(f"newmodel{ii} = Instance.new('Part')\n")
                    f.write(f"newmodel{ii}:PivotTo(CFrame.new({a[0][0]}, {a[0][1]}, {a[0][2]}) * CFrame.fromEulerAngles(0, math.rad({pul_rot + 90 - a[1]}), 0) * CFrame.fromEulerAngles(math.rad({-5 if isside(i) else 85}), 0, 0){ ' * CFrame.fromEulerAngles(math.rad(-75), 0, 0)' if isside(i) else '' })\n")
                    f.write(f"newmodel{ii}.Parent = workspace.devices.plate\n")
                    f.write(f"newmodel{ii}.Material = Enum.Material.Metal\n")
                    f.write(f"newmodel{ii}.Color = Color3.fromRGB(121, 148, 158)\n")
                    f.write(f"newmodel{ii}.Size = Vector3.new({-s[1] * .146 * 2 * 10}, {s[0] * .146 * 2 * 10}, {s[2] * .146 * 2 * 10})\n")
                    f.write(f"newmodel{ii}.Anchored = true\n")
                else:
                    s = j["scale"]
                    np = j["pos"]
                    np[2] = -np[2]
                    a = getglobalpos(i, np)
                    f.write(f"newmodel{ii} = Instance.new('Part')\n")
                    f.write(f"newmodel{ii}:PivotTo(CFrame.new({a[0][0]}, {a[0][1]}, {a[0][2]}) * CFrame.fromEulerAngles(0, math.rad({-90 - a[1] + pan_rot}), 0) * CFrame.fromEulerAngles(math.rad(-90), 0, math.rad(90)))\n")
                    f.write(f"newmodel{ii}.Parent = workspace.devices.plate\n")
                    f.write(f"newmodel{ii}.Material = Enum.Material.Metal\n")
                    f.write(f"newmodel{ii}.Color = Color3.fromRGB(204, 204, 204)\n")
                    f.write(f"newmodel{ii}.Size = Vector3.new({s[0] * .146 * 2 * 10}, {s[2] * .146 * 2 * 10}, {s[1] * .146 * 2 * 10})\n")
                    f.write(f"newmodel{ii}.Anchored = true\n")
                    ii += 1