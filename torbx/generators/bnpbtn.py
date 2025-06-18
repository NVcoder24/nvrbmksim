M = 0.004

from utils import *
import selsins

np_colors = []

np_colors_x = []
np_colors_y = []

with open("bnp_new.csv", "r", encoding="UTF-8") as f:
    lines = f.readlines()
    for y in range(len(lines)):
        l = lines[y].split(",")
        if y > 0:
            np_colors.append([])
        for x in range(len(l)):
            if y == 0:
                if x > 0:
                    np_colors_x.append(l[x].strip())
            else:
                if x == 0:
                    np_colors_y.append(l[x].strip())
                else:
                    np_colors[y - 1].append(l[x].strip())

shit = []
with open("bnp_lbl2.csv", "r", encoding="UTF-8") as f:
    lines = f.readlines()
    for y in range(len(lines)):
        l = lines[y].split(",")
        if y > 0:
            shit.append([])
        for x in range(len(l)):
            if y == 0:
                if x > 0:
                    pass
            else:
                if x == 0:
                    pass
                else:
                    shit[y - 1].append(l[x].strip())

#data = readcsv()

with open("LUA/np_btn_U3.lua", "w") as f:
    f.write("")

ii = 0
id_ = 1

az = []
pkaz = []
w = []

with open("LUA/np_btn_U3.lua", "a") as f:
    for y in range(len(np_colors)):
        for x in range(len(np_colors[y])):
            c = np_colors[y][x]
            lbl = shit[y][x]
            if c != "":
                n = ""
                try:
                    n = selsins.selsins_result[y][x][0]
                except Exception as e:
                    pass
                if c == "c":
                    f.write(f"newmodel{ii} = workspace.scam.prefabs.Selector_c:clone()\n")
                if c == "y":
                    f.write(f"newmodel{ii} = workspace.scam.prefabs.Selector_y:clone()\n")
                if c == "b":
                    f.write(f"newmodel{ii} = workspace.scam.prefabs.Selector_b:clone()\n")
                if c == "w":
                    f.write(f"newmodel{ii} = workspace.scam.prefabs.Selector_w:clone()\n")
                f.write(f"newmodel{ii}.Parent = workspace.scam.np\n")
                if n != "RE":
                    f.write(f"newmodel{ii}.Value.Value = {id_}\n")
                    if c == "b":
                        print(str(id_) + ",", end="")
                    id_ += 1
                if len(lbl) > 1:
                    if lbl == "CLEAR":
                        #f.write(f"newmodel{ii}.p2p.Cap.SurfaceGui.TextLabel.Text = ''\n")
                        pass
                    else:
                        #f.write(f"newmodel{ii}.p2p.Cap.SurfaceGui.TextLabel.Text = '{lbl}'\n")
                        #f.write(f"newmodel{ii}.p2p.Cap.SurfaceGui.TextLabel.Text = ''\n")
                        pass
                else:
                    #f.write(f"newmodel{ii}.p2p.Cap.SurfaceGui.TextLabel.Text = \"{np_colors_y[y]}-{np_colors_x[x]}\"\n")
                    pass
                f.write(f"newmodel{ii}.p2p.Body7.SurfaceGui.ImageLabel.Image = 'rbxgameasset://Images/NPBTN_{y}-{x} (1)'\n")
                    
                f.write(f"newmodel{ii}:PivotTo(CFrame.new(workspace.scam.prefabs.Part.CFrame.Position + Vector3.new({-M * x * 25}, {0}, {-M * y * 25})) * CFrame.fromEulerAngles(0, math.rad(180), 0))\n")
                ii += 1

print(az)
print(pkaz)