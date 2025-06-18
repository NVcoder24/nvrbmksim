from utils import *

data = readcsv()

with open("LUA/mtkind.lua", "w") as f:
    f.write("")

ccolor = {
    "r": "Color3.fromRGB(196, 40, 28)",
    "y": "Color3.fromRGB(226, 221, 77)",
    "g": "Color3.fromRGB(29, 156, 29)",
}

ii = 0
with open("LUA/mtkind.lua", "a") as f:
    for i in data.keys():
        for j in data[i]:
            if "mtkind" in j["name"]:
                if ispult(i):
                    z = j["pos"]
                    #z[2] -=  0.04
                    a = getglobalpos_pult(i, z)
                    f.write(f"newmodel{ii} = workspace.prefabs.mtkindd:clone()\n")
                    f.write(f"newmodel{ii}:PivotTo(CFrame.new({a[0][0]}, {a[0][1]}, {a[0][2]}) * CFrame.fromEulerAngles(0, math.rad({pul_rot + 0 - a[1]}), 0) * { 'CFrame.fromEulerAngles(0, 0, math.rad(80)' if isside(i) else 'CFrame.fromEulerAngles(0, 0, math.rad(5)'})* CFrame.fromEulerAngles(0, math.rad(90), 0))\n")
                    f.write(f"newmodel{ii}.Parent = workspace.devices.mtkind\n")
                    if j["ccolor"]:
                        f.write(f"newmodel{ii}.Body1.Color = {ccolor[j['ccolor']]}\n")
                    if j["ctex"]:
                        f.write(f"newmodel{ii}.Body1.Decal.Texture = '{j['ctex']}'\n")
                    ii += 1
                else:
                    z = j["pos"]
                    #z[0] -=  0.04
                    a = getglobalpos(i, z)
                    f.write(f"newmodel{ii} = workspace.prefabs.mtkindd:clone()\n")
                    f.write(f"newmodel{ii}:PivotTo(CFrame.new({a[0][0]}, {a[0][1]}, {a[0][2]}) * CFrame.fromEulerAngles(0, math.rad({-90 - a[1] + pan_rot}), 0)* CFrame.fromEulerAngles(0, 0, math.rad(90)))\n")
                    f.write(f"newmodel{ii}.Parent = workspace.devices.mtkind\n")
                    if j["ccolor"]:
                        f.write(f"newmodel{ii}.Body1.Color = {ccolor[j['ccolor']]}\n")
                    if j["ctex"]:
                        f.write(f"newmodel{ii}.Body1.Decal.Texture = '{j['ctex']}'\n")
                    ii += 1