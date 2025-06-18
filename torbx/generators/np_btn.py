from utils import *
import selsins

np_colors = []

np_colors_x = []
np_colors_y = []

with open("np_colors.csv", "r") as f:
    lines = f.readlines()
    for y in range(len(lines)):
        l = lines[y].split(",")
        if y > 0:
            np_colors.append([])
        for x in range(len(l)):
            if y == 0:
                if x > 0:
                    np_colors_x.append(l[x])
            else:
                if x == 0:
                    np_colors_y.append(l[x])
                else:
                    np_colors[y - 1].append(l[x].strip())

data = readcsv()

with open("LUA/np_btn.lua", "w") as f:
    f.write("")

cols = {
    "w": "Color3.fromRGB(252, 250, 255)",
    "r": "Color3.fromRGB(170, 32, 34)",
    "c": "Color3.fromRGB(0, 143, 156)",
    "b": "Color3.fromRGB(0, 62, 100)",
    "y": "Color3.fromRGB(239, 243, 18)",
}

az = [6,8,10,48,50,52,54,56,92,94,96,98,101,109,145,146,148,149,151,152,186,187,189,190]
az2 = []
az3 = []

usp = [7,9,39,41,43,45,78,80,82,84,86,88,122,124,126,128,130,132,166,168,170,172,202,204]
usp1 = []

pk = [13,15,16,18,38,46,66,68,69,72,74,75,77,133,135,136,139,141,142,144,193,195,196,198]
pk1 = []

ii = 0
id_ = 1
with open("LUA/np_btn.lua", "a") as f:
    for y in range(len(np_colors)):
        for x in range(len(np_colors[y])):
            c = np_colors[y][x]
            if c != "":
                n = ""
                try:
                    n = selsins.selsins_result[y][x][0]
                except Exception as e:
                    pass
                a = getglobalpos_pult("4a", [(- 115 - 25 * y) / 1000, 0, (-216 - 25 * x) / 1000])
                f.write(f"newmodel{ii} = workspace.prefabs.np_btn.np_btn_{c}:clone()\n")
                #f.write(f"newmodel{ii}.Body2.Color = {cols[c]}\n")
                f.write(f"newmodel{ii}.id.Value = 0\n")
                if n != "RE":
                    f.write(f"newmodel{ii}.id.Value = {id_}\n")
                    if id_ in az:
                        az2.append(ii + 1)
                        az3.append(f"{x},{y}")
                    if id_ in usp:
                        usp1.append(ii + 1)
                    if id_ in pk:
                        pk1.append(ii + 1)
                    id_ += 1
                f.write(f"newmodel{ii}:PivotTo(CFrame.new({a[0][0]}, {a[0][1]}, {a[0][2]}) * CFrame.fromEulerAngles(0, math.rad({pul_rot + 90 - a[1]}), 0) * CFrame.fromEulerAngles(math.rad({-5}), 0, 0))\n")
                f.write(f"newmodel{ii}.Parent = workspace.devices.np\n")
                f.write(f"newmodel{ii}.Body2.lbl.ImageLabel.Image = \"rbxgameasset://Images/NPBTN_{y}-{x}\"\n")
                #if c in ["w","y","c"]:
                #    f.write(f"newmodel{ii}.Body2.Decal.Color3 = Color3.fromRGB(0, 0, 0)\n")
                ii += 1

print("{" + ",".join([ f"{i}" for i in az2 ]) + "}")
print("{" + ",".join([ f"{i}" for i in usp1 ]) + "}")
print("{" + ",".join([ f"{i}" for i in pk1 ]) + "}")
print(az3)