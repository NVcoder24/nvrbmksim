"""

REACTOR SIM
------------------
GENERATION: autism
VERSION: 0.0.1
------------------
BY NVCODER

"""

print("REACTOR SIM INIT")

import math
import time
import random

"""
====================================
           CONFIG
====================================
"""
DO_LOG = False
DO_PRINT_LOG = True

MAX_INFL = 7
SIM_RES_Y = 7
AZ_H = 7
ONE_LVL_H = AZ_H / SIM_RES_Y

NEUTR_MUL = 1
BASE_NEUTR = 1

MAX_BLOCK_ROD = .2

"""
====================================
           UTILS
====================================
"""
# LOGGER
with open("log_reactor.txt", "w") as f:
    f.write("")
def log(t):
    if not DO_LOG:
        return
    if DO_PRINT_LOG:
        print(t)
    with open("log_reactor.txt", "a", encoding="utf-8") as f:
        f.write(str(t) + "\n")

# ARDUINO MAP FUNCTION
def mapval(x, in_min, in_max, out_min, out_max):
    return (x - in_min) * (out_max - out_min) / (in_max - in_min) + out_min

"""
====================================
        CHANNELS CLASSES
====================================
"""
class ch:
    def __init__(self) -> None:
        pass

class ch_fuel(ch):
    def __init__(self) -> None:
        super().__init__()
        self.infl = []
        self.Kcoef = [1] * SIM_RES_Y

class ch_rod(ch):
    def __init__(self) -> None:
        self.bottom_min_out = 0
        self.bottom_max_out = 7
        self.block_len = 6.790
        self.accel_len = 4.5
        self.bottom_pos = self.bottom_min_out
        self.prevpos = self.bottom_pos

class ch_usp(ch_rod):
    def __init__(self) -> None:
        self.bottom_min_out = .5
        self.bottom_max_out = 4
        self.block_len = 6.7
        self.accel_len = 0
        self.bottom_pos = self.bottom_min_out
        self.prevpos = self.bottom_pos

# HEIGHTS OF SIMULATION LEVELS
lvl_h = [AZ_H / SIM_RES_Y / 2] + [AZ_H / SIM_RES_Y / 2 + AZ_H / SIM_RES_Y * i for i in range(1, SIM_RES_Y)]
lvl_bottoms = [ i - AZ_H / SIM_RES_Y / 2 for i in lvl_h ]
lvl_tops =    [ i + AZ_H / SIM_RES_Y / 2 for i in lvl_h ]

"""
====================================
           MTK ARRAY
====================================
"""
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

"""
====================================
           SELSINS ARRAY
====================================
"""
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
            selsins_result[f"{1 + x * 2}-{1 + y * 2}"] = s

"""
====================================
       BUILDING REACTOR GRID
====================================
"""
for y in range(len(mtk_colors)):
    reactor.append([])
    for x in range(len(mtk_colors[y])):
        if f"{x}-{y}" in selsins_result.keys():
            c = selsins_result[f"{x}-{y}"]
            if c == "RE":
                reactor[-1].append(None)
            elif c == "y":
                reactor[-1].append(ch_usp())
            else:
                reactor[-1].append(ch_rod())
        else:
            if mtk_colors[y][x] != "":
                reactor[-1].append(ch_fuel())
            else:
                reactor[-1].append(None)

rod_coords = []
fuel_coords = []
for y in range(len(reactor)):
    for x in range(len(reactor[y])):
        if type(reactor[y][x]) in [ch_fuel]:
            fuel_coords.append([x, y])
        if type(reactor[y][x]) in [ch_rod, ch_usp]:
            rod_coords.append([x, y])

"""
====================================
       CALCULATING INFLUENCES
====================================
"""
for y1 in range(len(reactor)):
    for x1 in range(len(reactor[y1])):
        try:
            if type(reactor[y1][x1]) in [ch_fuel]:
                infls = []
                dists = []
                coords = []
                for i in rod_coords:
                    x2, y2 = int(i[0]), int(i[1])
                    dist = math.sqrt(((x2 - x1) ** 2) + ((y2 - y1) ** 2))
                    if dist < MAX_INFL:
                        coords.append([x2, y2])
                        dists.append(dist)
                mindist = min(dists)
                maxdist = max(dists)
                for i in range(len(coords)):
                    norm_dist = mapval(dists[i], mindist, maxdist, 0, 1)
                    infl = (1 - norm_dist) ** 2
                    if infl > 0:
                        infls.append([coords[i][0], coords[i][1], infl])
                reactor[y1][x1].infl = infls
        except Exception as e:
            log(f"INFL CALC ERR {mtk_colors_x[x1]}-{mtk_colors_y[y1]}")

"""
====================================
       CREATE BASE POPULATION
====================================
"""
neutr_population = []
for y in range(len(reactor)):
    neutr_population.append([])
    for x in range(len(reactor[y])):
        if type(reactor[y][x]) in [ch_fuel]:
            neutr_population[-1].append([0] * SIM_RES_Y)
        else:
            neutr_population[-1].append(None)

for i in range(BASE_NEUTR):
    coord = random.choice(fuel_coords)
    h = random.choice(range(SIM_RES_Y))
    neutr_population[coord[1]][coord[0]][h] += 1

base_neutr = 0

"""
====================================
       SIMULATION VARS
====================================
"""
SIM_WATER_DENSITY = 1000
SIM_WATER_LEVEL = .3

"""
====================================
       SIMULATION TICK
====================================
"""
def count_neutr():
    all_neutr = 0
    for y in range(len(neutr_population)):
        for x in range(len(neutr_population[y])):
            if neutr_population[y][x] != None:
                for i in neutr_population[y][x]:
                    all_neutr += i
    return all_neutr

def minmax(n , mi, ma):
    if n > ma: return ma
    if n < mi: return mi
    return n

last_tick = 0
last_global_k = 1
last_reactor_log = ""

def updatesim():
    global last_tick
    global neutr_population
    global last_reactor_log

    for_shits = 0

    DT = 0

    if last_tick == 0:
        last_tick = time.time()
        return
    else:
        DT = time.time() - last_tick
        last_tick = time.time()

    neutr_pre_tick = count_neutr()
    log_temp = ""

    # count neutrons
    log_temp += f"НЕЙТРОНОВ В РЕАКТОРЕ ДО ТАКТА: {count_neutr()}\n"
    # neutron count calculation
    for y in range(len(reactor)):
        for x in range(len(reactor[y])):
            if type(reactor[y][x]) in [ch_fuel]:
                for lvl in range(SIM_RES_Y):
                    # calculate K coef
                    Kcoef = 1

                    # calculate control rods blocking coef
                    block_coefs = []
                    accel_coefs = []
                    sum_div = 0
                    sum_div_accel = 0
                    for infl in reactor[y][x].infl:
                        for_shits += 1
                        rod = reactor[infl[1]][infl[0]]
                        i = infl[2]
                        sum_div += i

                        rod_bottom_out = rod.bottom_pos
                        rod_top_out = rod.bottom_pos + rod.block_len
                        # TODO: REPLACE 4 IFs WITH SINGLE EXPRESSION
                        if rod_bottom_out < lvl_bottoms[lvl] and rod_top_out > lvl_tops[lvl]:
                            block_coefs.append(1 * i)
                        elif rod_bottom_out > lvl_tops[lvl] or rod_top_out < lvl_bottoms[lvl]:
                            block_coefs.append(0)
                        elif lvl_bottoms[lvl] < rod_top_out and rod_top_out < lvl_tops[lvl]:
                            block_coefs.append((rod_top_out - lvl_bottoms[lvl]) / ONE_LVL_H * i)
                        else:
                            block_coefs.append((lvl_tops[lvl] - rod_bottom_out) / ONE_LVL_H * i)

                        accel_bottom_out = rod.bottom_pos - rod.accel_len
                        accel_top_out = rod.bottom_pos
                        accel_infl_koef = 0
                        if rod.prevpos > rod.bottom_pos and rod.bottom_pos > .1:
                            accel_infl_koef = 1
                        # TODO: REPLACE 4 IFs WITH SINGLE EXPRESSION
                        if accel_bottom_out < lvl_bottoms[lvl] and accel_top_out > lvl_tops[lvl]:
                            accel_coefs.append(1 * i * accel_infl_koef)
                        elif accel_bottom_out > lvl_tops[lvl] or accel_top_out < lvl_bottoms[lvl]:
                            accel_coefs.append(0)
                        elif lvl_bottoms[lvl] < accel_top_out and accel_top_out < lvl_tops[lvl]:
                            accel_coefs.append((accel_top_out - lvl_bottoms[lvl]) / ONE_LVL_H * i * accel_infl_koef)
                        else:
                            accel_coefs.append((lvl_tops[lvl] - accel_bottom_out) / ONE_LVL_H * i * accel_infl_koef)

                    rod_block_coef = sum(block_coefs) / sum_div
                    rod_accel_coef = sum(accel_coefs) / sum_div

                    # Kcoef formula
                    Kcoef = 1 + .2 - rod_block_coef * .3 + rod_accel_coef * .1

                    reactor[y][x].Kcoef[lvl] = Kcoef

                    # calculate new neutron count for cell
                    neutr_population[y][x][lvl] += (neutr_population[y][x][lvl] + BASE_NEUTR) * (Kcoef - 1) * NEUTR_MUL * DT
                    if neutr_population[y][x][lvl] < 0:
                        neutr_population[y][x][lvl] = 0
    for i in rod_coords:
        reactor[i[1]][i[0]].prevpos = reactor[i[1]][i[0]].bottom_pos


    c = count_neutr()
    log_temp += f"НЕЙТРОНОВ В РЕАКТОРЕ ПОСЛЕ ТАКТА: {c}\n"
    try:
        last_global_k = c / neutr_pre_tick
    except Exception as e:
        last_global_k = 1
    
    log_temp += f"K: {last_global_k}\n"
    log_temp += f"for shits: {for_shits}\n"
    #if c < BASE_NEUTR:
    #    neutr_population = base_neutr
    sfkre = (c) / 332_054_516_680_000_000_000_000
    log_temp += f"=====| СФКРЭ: {int(sfkre)} МВт |=====\n"

    last_reactor_log = log_temp

    log(log_temp)

"""start1 = time.time()
for i in range(10):
    start = time.time()
    updatesim()
    result = time.time() - start
    log(f"update tick took {result}")
result1 = time.time() - start1
log(f"=========================\n10 UPDATES TOOK {result1}")"""