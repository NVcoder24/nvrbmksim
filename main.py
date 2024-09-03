import math
import sim.reactor as reactor_sim

mtk_colors = []

mtk_colors_x = []
mtk_colors_y = []

with open("mtkcolors.csv", "r") as f:
    lines = f.readlines()
    for y in range(len(lines)):
        l = lines[y].split(",")
        if y > 0:
            mtk_colors.append([])
        for x in range(len(l)):
            if y == 0:
                if x > 0:
                    mtk_colors_x.append(l[x].strip())
            else:
                if x == 0:
                    mtk_colors_y.append(l[x].strip())
                else:
                    mtk_colors[y - 1].append(l[x].strip())

class ch:
    def __init__(self, mtkcolor, posstr) -> None:
        self.mtkcolor = mtkcolor
        self.posstr = posstr

class ch_fuel(ch):
    def __init__(self, mtkcolor, posstr) -> None:
        super().__init__(mtkcolor, posstr)
        self.influences = []
        self.power = 0
        self.temp = 0
        self.lastneutr = 0

    def __str__(self) -> str:
        inflstr = ""
        n = 1
        for i in self.influences:
            inflstr += f"{n}) CHYX={str(i[0])}; POS={mtk_colors_y[i[0][0]]}-{mtk_colors_x[i[0][1]]}; COEF={i[1]}\n"
            n += 1
        return f"ch_fuel\n=== PARAM ===\nTPower: {self.power} MW\nTemp: {self.temp} C\nLast Neutr Recv: {self.lastneutr}\n=== INFL ===\n{inflstr}"

class ch_rod(ch):
    def __init__(self, mtkcolor, posstr) -> None:
        super().__init__(mtkcolor, posstr)
        self.pos = 7.0

    def setpos(self, pos):
        if pos > 7: self.pos = 7.0; return
        if pos < 0: self.pos = 0.0; return
        self.pos = pos

    def __str__(self) -> str:
        return f"ch_rod\npos={self.pos}"

class ch_az(ch_rod):
    def __init__(self, mtkcolor, posstr) -> None:
        super().__init__(mtkcolor, posstr)

    def __str__(self) -> str:
        return f"ch_az\npos={self.pos}"

class ch_usp(ch_rod):
    def __init__(self, mtkcolor, posstr) -> None:
        super().__init__(mtkcolor, posstr)

    def __str__(self) -> str:
        return f"ch_usp\npos={self.pos}"

class Reactor():
    def __init__(self) -> None:
        self.rod_poses = []
        self.mtk_colors_x = []
        self.mtk_colors_y = []
        self.rod_types = [ch_rod, ch_az, ch_usp]
        self.fuel_types = [ch_fuel]
        self.reactor = self.constructreactor()

    def getchibypos(self, pos):
        return self.mtk_colors_y.index(pos.split("-")[0]), self.mtk_colors_x.index(pos.split("-")[1])

    def getchbypos(self, pos):
        i1, i2 = self.getchibypos(pos)
        return self.reactor[i1][i2]

    def constructreactor(self):
        reactor = []
        selsins = []

        selsins_x = []
        selsins_y = []

        with open("selsins.csv", "r") as f:
            lines = f.readlines()
            for y in range(len(lines)):
                l = lines[y].split(",")
                if y > 0:
                    selsins.append([])
                for x in range(len(l)):
                    if y == 0:
                        if x > 0:
                            selsins_x.append(l[x].strip())
                    else:
                        if x == 0:
                            selsins_y.append(l[x].strip())
                        else:
                            selsins[y - 1].append(l[x].strip())
        selsins_result = {}
        for y in range(len(selsins)):
            for x in range(len(selsins[y])):
                s = selsins[y][x]
                if s != "":
                    selsins_result[f"{selsins_y[y]}-{selsins_x[x]}"] = s
        
        mtk_colors = []

        mtk_colors_x = []
        mtk_colors_y = []

        with open("mtkcolors.csv", "r") as f:
            lines = f.readlines()
            for y in range(len(lines)):
                l = lines[y].split(",")
                if y > 0:
                    mtk_colors.append([])
                for x in range(len(l)):
                    if y == 0:
                        if x > 0:
                            mtk_colors_x.append(l[x].strip())
                    else:
                        if x == 0:
                            mtk_colors_y.append(l[x].strip())
                        else:
                            mtk_colors[y - 1].append(l[x].strip())
        
        for y in range(len(mtk_colors)):
            reactor.append([])
            for x in range(len(mtk_colors[y])):
                if f"{mtk_colors_y[y]}-{mtk_colors_x[x]}" in selsins_result.keys():
                    c = selsins_result[f"{mtk_colors_y[y]}-{mtk_colors_x[x]}"]
                    if c == "r":
                        reactor[-1].append(ch_az(mtk_colors[y][x], f"{mtk_colors_y[y]}-{mtk_colors_x[x]}"))
                        self.rod_poses.append([x,y])
                    elif c == "y":
                        reactor[-1].append(ch_usp(mtk_colors[y][x], f"{mtk_colors_y[y]}-{mtk_colors_x[x]}"))
                        self.rod_poses.append([x,y])
                    else:
                        if c != "RE":
                            reactor[-1].append(ch_rod(mtk_colors[y][x], f"{mtk_colors_y[y]}-{mtk_colors_x[x]}"))
                            self.rod_poses.append([x,y])
                        else:
                            reactor[-1].append(None)
                else:
                    if mtk_colors[y][x] != "":
                        reactor[-1].append(ch_fuel(mtk_colors[y][x], f"{mtk_colors_y[y]}-{mtk_colors_x[x]}"))
                    else:
                        reactor[-1].append(None)
        self.mtk_colors_x = mtk_colors_x
        self.mtk_colors_y = mtk_colors_y
        return reactor

reactor = Reactor()

selsins = []

selsins_x = []
selsins_y = []

selected_rods = []

with open("selsins.csv", "r") as f:
    lines = f.readlines()
    for y in range(len(lines)):
        l = lines[y].split(",")
        if y > 0:
            selsins.append([])
        for x in range(len(l)):
            if y == 0:
                if x > 0:
                    selsins_x.append(l[x])
            else:
                if x == 0:
                    selsins_y.append(l[x])
                else:
                    selsins[y - 1].append(l[x].strip())

selsins_result = []
for y in range(len(selsins)):
    selsins_result.append([])
    for x in range(len(selsins[y])):
        selsins_result[-1].append([])
        s = selsins[y][x]
        if s != "":
            selsins_result[-1].pop()
            selsins_result[-1].append([s, f"{selsins_y[y]}-{selsins_x[x]}".strip()])

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

np_result = []
for y in range(len(np_colors)):
    np_result.append([])
    for x in range(len(np_colors[y])):
        np_result[-1].append([])
        s = np_colors[y][x]
        if s != "":
            np_result[-1].pop()
            if selsins[y][x] != "RE":
                np_result[-1].append([s, f"{np_colors_y[y]}-{np_colors_x[x]}".strip()])
            else:
                np_result[-1].append([s, f"".strip()])

np_joystick = 0

from flask import Flask, render_template, jsonify
from threading import Thread
import time

app = Flask(__name__, static_url_path="")

# PUBLIC ROUTES
@app.route("/")
def index():
    return render_template("index.html")

@app.route("/splitscreen")
def splitscreen():
    return render_template("splitscreen.html")

@app.route("/am")
def am(): return render_template("AM.html")

@app.route("/ass")
def ass(): return render_template("ASS.html")

@app.route("/mtk")
def mtk_():
    mtk = "<table border='#ccc' class='mtk mainelement'>"
    for i in reactor.reactor:
        mtk += "<tr>"
        for j in i:
            mtk += "<td style='background: "
            if j == None:
                mtk += "#ccc"
                mtk += ";'></td>"
            else:
                if j.mtkcolor == "w":
                    mtk += "#fff"
                elif j.mtkcolor == "y":
                    mtk += "yellow"
                elif j.mtkcolor == "g":
                    mtk += "green"
                else:
                    mtk += "#ccc"
                mtk += f";'>{ j.posstr }</td>"
        mtk += "</tr>"
    mtk += "</table>"
    
    return render_template("mtk.html", mtk=mtk)

@app.route("/selsins")
def selsins_():
    return render_template("selsins.html")

@app.route("/np")
def np_():
    s = ""

    for i in np_result:
        s += "<tr>"
        for j in i:
            s += f"<td "
            if len(j) > 0:
                if j[1] != "":
                    s += f"onclick='c(\"{j[1]}\")'"
                s += f" class='btn {j[0]}'"
                s += ">"
                s += f"{j[1]}"
            else:
                s += ">"
            s += "</td>"
        s += "</tr>"
    
    l = f"""<div class="lamp { 'on' if len(selected_rods) == 1 else '' }">1</div>
        <div class="lamp { 'on' if len(selected_rods) == 2 else '' }">2</div>
        <div class="lamp { 'on' if len(selected_rods) == 3 else '' }">3</div>
        <div class="lamp { 'on' if len(selected_rods) == 4 else '' }">4</div>
        <div class="lamp last { 'on' if len(selected_rods) >= 5 else '' }">5<br>огр<br>вверх</div>"""
    return render_template("np.html", np=s, nplamps=l)

# API
@app.route("/api/getchdata/<string:ch>")
def api_getchdata(ch):
    return (f"=== REACTOR ===\n{reactor_sim.last_reactor_log}\n=== CH ===\n" + "").replace("\n", "<br>")

@app.route("/api/getselsins/")
def api_getselsins():
    s = ""

    for i in selsins_result:
        s += "<tr>"
        for j in i:
            s += "<td"
            if len(j) > 0 and j[0] != "RE":
                c = reactor.getchbypos(j[1])
                s += " class='selsin'"
                s += ">"
                if c.pos == 0:
                    s += "<p class='posind1'>ВК</p>"
                s += f"<p class='pos'>{str(round(c.pos, 2)).ljust(4, '0')}</p>"
                if c.pos == 7:
                    s += "<p class='posind2'>НК</p>"
                s += f"<span>{j[1]}</span>"
            else:
                s += ">"
            s += "</td>"
        s += "</tr>"
    return s

@app.route("/api/npdoshit/<string:s>")
def api_npdoshit(s):
    if s in selected_rods:
        selected_rods.remove(s)
    else:
        selected_rods.append(s)
    return ""

@app.route("/api/getnp/")
def api_getnp():
    return jsonify(selected_rods)

@app.route("/api/resetnp/")
def api_resetnp():
    global selected_rods
    selected_rods = []
    return ""

@app.route("/api/npstartup/")
def api_npstartup(): global np_joystick; np_joystick = -1; return ""
@app.route("/api/npstopup/")
def api_npstopup(): global np_joystick; np_joystick = 0; return ""

@app.route("/api/npstartdown/")
def api_npstartdown(): global np_joystick; np_joystick = 1; return ""
@app.route("/api/npstopdown/")
def api_npstopdown(): global np_joystick; np_joystick = 0; return ""

is_main_running = True

def SUZ_THREAD():
    print("started SIM thread")
    import time
    global reactor
    global selected_rods
    global np_joystick
    global is_main_running
    lastdt = time.time()
    while is_main_running:
        # SUZ
        dt = time.time() - lastdt
        lastdt = time.time()
        for i in selected_rods:
            i1, i2 = reactor.getchibypos(i)
            reactor.reactor[i1][i2].setpos(reactor.reactor[i1][i2].pos + .5 * np_joystick * dt)

        # COPY SUZ POS
        for i in reactor_sim.rod_coords:
            pos = reactor.reactor[i[1]][i[0]].pos
            reactor_sim.reactor[i[1]][i[0]].bottom_pos = reactor_sim.mapval(pos, 0, 7, reactor_sim.reactor[i[1]][i[0]].bottom_max_out, reactor_sim.reactor[i[1]][i[0]].bottom_min_out)

        # REACTOR SIM
        reactor_sim.updatesim()

Thread(target=SUZ_THREAD).start()

# APP RUN
try:
    app.run(debug=True)
    is_main_running = False
except Exception as e:
    is_main_running = False