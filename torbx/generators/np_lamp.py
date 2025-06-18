from utils import *
import selsins

np_colors = []

np_colors_x = []
np_colors_y = []

with open("nplamps.csv", "r") as f:
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

with open("LUA/np_lamp_real.lua", "w") as f:
    f.write("")

az = ['7,1', '11,1', '15,1', '2,6', '6,6', '10,6', '14,6', '18,6', '6,10', '10,10', '14,10', '18,10', '1,11', '21,11', '1,15', '5,15', '9,15', '13,15', '17,15', '21,15', '5,19', '9,19', '13,19', '17,19']
az2 = []

ii = 0
id_ = 1
with open("LUA/np_lamp_real.lua", "a") as f:
    for y in range(len(np_colors)):
        for x in range(len(np_colors[y])):
            c = np_colors[y][x]
            if c == "1":
                print(f"{x},{y}")
                if f"{x},{y}" in az:
                    az2.append(id_)
                a = getglobalpos_pult("4a", [(- 115 - 25 * (y - 1)) / 1000, 0, (-216 - 25 * x) / 1000])
                f.write(f"newmodel{ii} = workspace.prefabs.np_lamp_real:clone()\n")
                f.write(f"newmodel{ii}:PivotTo(CFrame.new({a[0][0]}, {a[0][1]}, {a[0][2]}) * CFrame.fromEulerAngles(0, math.rad({pul_rot + 90 - a[1]}), 0) * CFrame.fromEulerAngles(math.rad({-5}), 0, 0))\n")
                f.write(f"newmodel{ii}.Parent = workspace.devices.np_l\n")
                ii += 1
                id_ += 1

print("{" + ",".join([ f"{i}" for i in az2 ]) + "}")