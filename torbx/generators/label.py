from utils import *

data = readcsv()

with open("LUA/label.lua", "w") as f:
    f.write("")

ii = 0
with open("LUA/label.lua", "a") as f:
    for i in data.keys():
        if i not in ["p3"]: continue
        for j in data[i]:
            if "label" in j["name"]:
                if ispult(i):
                    if isside(i):
                        s = j["scale"]
                        np = j["pos"]
                        rsz = 0
                        if s[2] > 0.0004:
                            rsz = .002 * .146 * 2
                        else:
                            pass
                        s = j["scale"]
                        np = j["pos"]
                        a = getglobalpos_pult(i, np)
                        f.write(f"newmodel{ii} = Instance.new('Part')\n")
                        f.write(f"newmodel{ii}:PivotTo(CFrame.new({a[0][0]}, {a[0][1]}, {a[0][2]}) * CFrame.fromEulerAngles(0, math.rad({pul_rot + 90 - a[1]}), 0) * CFrame.fromEulerAngles(math.rad({-5 if isside(i) else 85}), 0, 0){ ' * CFrame.fromEulerAngles(math.rad(-75), 0, 0)' if isside(i) else '' })\n")
                        f.write(f"newmodel{ii}.Parent = workspace.devices.label\n")
                        f.write(f"newmodel{ii}.Material = Enum.Material.SmoothPlastic\n")
                        f.write(f"newmodel{ii}.Color = Color3.fromRGB(255, 255, 255)\n")
                        f.write(f"newmodel{ii}.Size = Vector3.new({s[0] * .146 * 2 * 10}, {rsz * 10}, {s[1] * .146 * 2 * 10})\n")
                        f.write(f"newmodel{ii}.Anchored = true\n")
                    else:
                        s = j["scale"]
                        np = j["pos"]
                        rsz = 0
                        if s[2] > 0.0004:
                            rsz = .002 * .146 * 2
                            if np[1] > 0.0025:
                                np[1] = .001 + 0.0025
                            else:
                                np[1] = .001
                        else:
                            if np[1] > 0.0025:
                                np[1] = .00025 + 0.0025
                            else:
                                np[1] = .00025
                            rsz = .0005 * .146 * 2
                        #s = [s[0] * 2, s[1] * 2, s[2] * 2]
                        a = getglobalpos_pult(i, np)
                        f.write(f"newmodel{ii} = Instance.new('Part')\n")
                        f.write(f"newmodel{ii}:PivotTo(CFrame.new({a[0][0]}, {a[0][1]}, {a[0][2]}) * CFrame.fromEulerAngles(0, math.rad({pul_rot + 90 - a[1]}), 0) * CFrame.fromEulerAngles(math.rad({-5 if isside(i) else 85}), 0, 0){ ' * CFrame.fromEulerAngles(math.rad(-75), 0, 0)' if isside(i) else '' })\n")
                        f.write(f"newmodel{ii}.Parent = workspace.devices.label\n")
                        f.write(f"newmodel{ii}.Material = Enum.Material.SmoothPlastic\n")
                        f.write(f"newmodel{ii}.Color = Color3.fromRGB(255, 255, 255)\n")
                        f.write(f"newmodel{ii}.Size = Vector3.new({-s[1] * .146 * 2 * 10}, {s[0] * .146 * 2 * 10}, {rsz * 10})\n")
                        f.write(f"newmodel{ii}.Anchored = true\n")
                    ii += 1
                else:
                    s = j["scale"]
                    np = j["pos"]
                    rsz = 0
                    if s[2] > 0.0004:
                        rsz = .002 * .146 * 2
                        if np[2] > 0.003:
                            np[2] = -.001 - 0.003
                        else:
                            np[2] = -.001
                    else:
                        np[2] = -.00025
                        rsz = .0005 * .146 * 2
                    a = getglobalpos(i, np)
                    f.write(f"newmodel{ii} = Instance.new('Part')\n")
                    f.write(f"newmodel{ii}:PivotTo(CFrame.new({a[0][0]}, {a[0][1]}, {a[0][2]}) * CFrame.fromEulerAngles(0, math.rad({-90 - a[1] + pan_rot}), 0) * CFrame.fromEulerAngles(math.rad(-90), 0, math.rad(90)))\n")
                    f.write(f"newmodel{ii}.Parent = workspace.devices.label\n")
                    f.write(f"newmodel{ii}.Material = Enum.Material.SmoothPlastic\n")
                    f.write(f"newmodel{ii}.Color = Color3.fromRGB(255, 255, 255)\n")
                    f.write(f"newmodel{ii}.Size = Vector3.new({s[0] * .146 * 2 * 10}, {rsz * 10}, {s[1] * .146 * 2 * 10})\n")
                    f.write(f"newmodel{ii}.Anchored = true\n")
                    ii += 1