import pygame
import math

errs = 0

def readcsv():
    global errs
    result = {}
    with open("stuff.csv", "r") as f:
        for i in f.readlines():
            a = i.split(";")
            if a[0] not in result.keys():
                result[a[0]] = []
            try:
                result[a[0]].append({
                    "name": a[1],
                    "pos": [float(a[2].replace(",", ".")), float(a[3].replace(",", ".")), float(a[4].replace(",", "."))],
                    "rot": [float(a[5].replace(",", ".")), float(a[6].replace(",", ".")), float(a[7].replace(",", "."))],
                    "scale": [float(a[8].replace(",", ".")), float(a[9].replace(",", ".")), float(a[10].replace(",", "."))],
                    "ccolor": a[11].strip(),
                    "ctex": a[12].strip(),
                })
            except Exception as e:
                #print(e, i)
                errs += 1
    print(f"Errors while reading stuff.csv: {errs}")
    return result

def pgv3_arr(v:pygame.Vector3):
    return [v.x, v.y, v.z]

pan_pos = pygame.Vector3(-8.551, 0.006, 20.065)
pan_rot = 59.01
scale = .146

pans = {}

with open("test111.csv", "r") as f:
    for i in f.readlines():
        a = i[:-1].split(";")
        pans[a[0]] = [[float(a[1].replace(",", ".")), float(a[2].replace(",", ".")), float(a[3].replace(",", "."))], float(a[4].replace(",", "."))]

def getglobalpos(panel, pos):
    p1 = pygame.Vector3(pans[panel][0])
    vec = pygame.Vector3(1, 0, 0).rotate(pans[panel][1], [0, 1, 0])
    if "(" in panel:
        p1_ = p1 + vec * pos[0] - pygame.Vector3(0, -1, 0) * pos[1] * math.cos(math.radians(15)) + pos[1] * vec.rotate(90, [0, 1, 0]) * -math.sin(math.radians(15))
    else:
        p1_ = p1 + vec * pos[0] - pygame.Vector3(0, -1, 0) * pos[1] + pos[2] * vec.rotate(90, [0, 1, 0])
    p2 = pygame.Vector3(-p1_.x, p1_.y, p1_.z)
    p3 = p2.rotate(pan_rot + 180, [0, 1, 0])
    p4 = p3 * 1.46 * 2 + pan_pos
    return pgv3_arr(p4), pans[panel][1]

pul_pos = pygame.Vector3(-14.613, 0.298, 21.023)
pul_rot = -35.247
scale = .146

def ispult(name):
    try:
        int(name[0])
        return True
    except Exception as e:
        return False

def isside(name):
    try:
        if "(" in name:
            return True
        return False
    except Exception as e:
        return False

def getglobalpos_pult(pult, pos):
    if pult[-1] == ")":
        p1 = pygame.Vector3(pans[pult][0])
        vec = pygame.Vector3(1, 0, 0).rotate(pans[pult][1], [0, 1, 0])
        vec2 = pygame.Vector3(1, 0, 0).rotate(-100, [0, 0, 1]).rotate(pans[pult][1], [0, 1, 0])
        p1_ = p1 + vec2 * -pos[1] + -pos[2] * vec.rotate(90, [0, 1, 0]) + pos[0] * vec2.rotate(90, [0, 0, 1])
        p2 = pygame.Vector3(-p1_.x, p1_.y, p1_.z)
        p3 = p2.rotate(pul_rot + 180, [0, 1, 0])
        p4 = p3 * 1.46 * 2 + pul_pos
        return pgv3_arr(p4), pans[pult][1], -95
    else:
        p1 = pygame.Vector3(pans[pult][0])
        vec = pygame.Vector3(1, 0, 0).rotate(pans[pult][1], [0, 1, 0])
        vec2 = pygame.Vector3(1, 0, 0).rotate(5, [0, 0, 1]).rotate(pans[pult][1], [0, 1, 0])
        p1_ = p1 + vec2 * pos[0] + -pos[2] * vec.rotate(90, [0, 1, 0]) + pos[1] * vec.rotate(90, [1, 0, 1])
        p2 = pygame.Vector3(-p1_.x, p1_.y, p1_.z)
        p3 = p2.rotate(pul_rot + 180, [0, 1, 0])
        p4 = p3 * 1.46 * 2 + pul_pos
        return pgv3_arr(p4), pans[pult][1], 5

def luaser(obj):
    if type(obj) == list:
        return "{" + ",".join([ luaser(i) for i in obj ]) + "}"
    if type(obj) == float or type(obj) == int:
        return str(obj)
    if type(obj) == dict:
        return "{" + ",".join([ f"[{luaser(i)}]={luaser(obj[i])}" for i in obj.keys() ]) + "}"
    if type(obj) == str:
        return f"'{obj}'"