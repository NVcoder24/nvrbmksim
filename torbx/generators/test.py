from utils import *

data = readcsv()

pi = 0

with open("test.lua", "w") as f:
    f.write("")

with open("test.lua", "a") as f:
    for i in data.keys():
        p = getglobalpos(i, [0, 0, 0])
        f.write(f"local part{pi} = Instance.new('Part')\n")
        f.write(f"part{pi}.Anchored = true\n")
        f.write(f"part{pi}.Parent = workspace.TEST\n")
        f.write(f"part{pi}.CFrame = CFrame.new({','.join([ str(j) for j in p[0] ])})\n")
        pi += 1