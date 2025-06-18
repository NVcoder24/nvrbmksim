import pygame

def readcsv():
    result = {}
    with open("stuff.csv", "r") as f:
        for i in f.readlines():
            a = i.split(";")
            if a[0] not in result.keys():
                result[a[0]] = []
            try:
                result[a[0]].append({
                    "name": a[1],
                    "pos": (float(a[2].replace(",", ".")), float(a[3].replace(",", ".")), float(a[4].replace(",", "."))),
                    "rot": (float(a[5].replace(",", ".")), float(a[6].replace(",", ".")), float(a[7].replace(",", "."))),
                    "scale":    (float(a[8].replace(",", ".")), float(a[9].replace(",", ".")), float(a[10].replace(",", "."))),
                })
            except Exception as e:
                print(e, i)
    return result

def pgv3_arr(v:pygame.Vector3):
    return [v.x, v.y, v.z]

pan_pos = pygame.Vector3(-8.551, 0.006, 20.065)
pan_rot = 59.01
scale = .146
ang_mul = 1
ang = 0
p1_pos = pygame.Vector3(0,0,0)
p1_vec = pygame.Vector3(1,0,0)
p1_ang = ang
ang += 2.5
p2_pos = p1_pos + p1_vec * 1000
p2_vec = p1_vec.rotate(ang, [0, 1, 0])
p2_ang = ang
ang += 5.25
p3_pos = p2_pos + p2_vec * 1000
p3_vec = p1_vec.rotate(ang, [0, 1, 0])
p3_pos += p3_vec * 50
p3_ang = ang
ang += 5.25
p4_pos = p3_pos + p3_vec * 1100
p4_vec = p1_vec.rotate(ang, [0, 1, 0])
p4_ang = ang
ang += 5.25
p5_pos = p4_pos + p4_vec * 1100
p5_vec = p1_vec.rotate(ang, [0, 1, 0])
p5_ang = ang
ang += 5.25
p6_pos = p5_pos + p5_vec * 1100
p6_vec = p1_vec.rotate(ang, [0, 1, 0])
p6_ang = ang
ang += 5.25
p7_pos = p6_pos + p6_vec * 1100
p7_vec = p1_vec.rotate(ang, [0, 1, 0])
p7_ang = ang
ang += 5.25
p8_pos = p7_pos + p7_vec * 1000
p8_vec = p1_vec.rotate(ang, [0, 1, 0])
p8_ang = ang
ang += 2.5
p9_pos = p8_pos + p8_vec * 1000
p9_vec = p1_vec.rotate(ang, [0, 1, 0])
p9_ang = ang
ang += 5.25
p10_pos = p9_pos + p9_vec * 1100
p10_vec = p1_vec.rotate(ang, [0, 1, 0])
p10_ang = ang
ang += 5.25
p11_pos = p10_pos + p10_vec * 1100
p11_vec = p1_vec.rotate(ang, [0, 1, 0])
p11_ang = ang
ang += 5.25
p12_pos = p11_pos + p11_vec * 1100
p12_vec = p1_vec.rotate(ang, [0, 1, 0])
p12_ang = ang
ang += 5.25
p13_pos = p12_pos + p12_vec * 1100
p13_vec = p1_vec.rotate(ang, [0, 1, 0])
p13_ang = ang
ang += 5.25
p14_pos = p13_pos + p13_vec * 1100
p14_vec = p1_vec.rotate(ang, [0, 1, 0])
p14_ang = ang
ang += 5.25
p15_pos = p14_pos + p14_vec * 1100
p15_vec = p1_vec.rotate(ang, [0, 1, 0])
p15_ang = ang
ang += 5.25
p16_pos = p15_pos + p15_vec * 1100
p16_vec = p1_vec.rotate(ang, [0, 1, 0])
p16_ang = ang
ang += 5.25
p17_pos = p16_pos + p16_vec * 1100
p17_vec = p1_vec.rotate(ang, [0, 1, 0])
p17_ang = ang
ang += 5.25
p18_pos = p17_pos + p17_vec * 1100
p18_vec = p1_vec.rotate(ang, [0, 1, 0])
p18_ang = ang
ang += 5.25
p19_pos = p18_pos + p18_vec * 1100
p19_vec = p1_vec.rotate(ang, [0, 1, 0])
p19_ang = ang
ang += 5.25
p20_pos = p19_pos + p19_vec * 1100
p20_vec = p1_vec.rotate(ang, [0, 1, 0])
p20_ang = ang
ang += 5.25
p21_pos = p20_pos + p20_vec * 1100
p21_vec = p1_vec.rotate(ang, [0, 1, 0])
p21_ang = ang
ang += 5.25
p22_pos = p21_pos + p21_vec * 1100
p22_vec = p1_vec.rotate(ang, [0, 1, 0])
p22_ang = ang
ang += 5.25
p23_pos = p22_pos + p22_vec * 1100
p23_vec = p1_vec.rotate(ang, [0, 1, 0])
p23_ang = ang
ang += 5.25
p24_pos = p23_pos + p23_vec * 1100
p24_vec = p1_vec.rotate(ang, [0, 1, 0])
p24_ang = ang
ang += 5.25
p25_pos = p24_pos + p24_vec * 1100
p25_vec = p1_vec.rotate(ang, [0, 1, 0])
p25_ang = ang
print(ang)

p1_pos += pygame.Vector3(0, 3300, 0)
p2_pos += pygame.Vector3(0, 3300, 0)
p3_pos += pygame.Vector3(0, 3295, 0)
p4_pos += pygame.Vector3(0, 3295, 0)
p5_pos += pygame.Vector3(0, 3295, 0)
p6_pos += pygame.Vector3(0, 3295, 0)
p7_pos += pygame.Vector3(0, 3300, 0)
p8_pos += pygame.Vector3(0, 3300, 0)
p9_pos += pygame.Vector3(0, 2470, 0)
p10_pos += pygame.Vector3(0, 2470, 0)
p11_pos += pygame.Vector3(0, 2470, 0)
p12_pos += pygame.Vector3(0, 2470, 0)
p13_pos += pygame.Vector3(0, 2470, 0)
p14_pos += pygame.Vector3(0, 2470, 0)
p15_pos += pygame.Vector3(0, 2470, 0)
p16_pos += pygame.Vector3(0, 2470, 0)
p17_pos += pygame.Vector3(0, 2470, 0)
p18_pos += pygame.Vector3(0, 2470, 0)
p19_pos += pygame.Vector3(0, 2470, 0)
p20_pos += pygame.Vector3(0, 2470, 0)
p21_pos += pygame.Vector3(0, 2470, 0)
p22_pos += pygame.Vector3(0, 2470, 0)
p23_pos += pygame.Vector3(0, 2470, 0)
p24_pos += pygame.Vector3(0, 2470, 0)
p25_pos += pygame.Vector3(0, 2470, 0)

pans = {}

with open("test111.csv", "r") as f:
    for i in f.readlines():
        a = i[:-1].split(";")
        pans[a[0]] = [[float(a[1].replace(",", ".")), float(a[2].replace(",", ".")), float(a[3].replace(",", "."))], float(a[4].replace(",", "."))]

def getglobalpos(panel, pos):
    pos = pygame.Vector3(0,0,0)
    vec = pygame.Vector3(1,0,0)
    if panel == "p1": pos, vec, ang = p1_pos, p1_vec, p1_ang
    if panel == "p2": pos, vec, ang = p2_pos, p2_vec, p2_ang
    if panel == "p3": pos, vec, ang = p3_pos, p3_vec, p3_ang
    if panel == "p4": pos, vec, ang = p4_pos, p4_vec, p4_ang
    if panel == "p5": pos, vec, ang = p5_pos, p5_vec, p5_ang
    if panel == "p6": pos, vec, ang = p6_pos, p6_vec, p6_ang
    if panel == "p7": pos, vec, ang = p7_pos, p7_vec, p7_ang
    if panel == "p8": pos, vec, ang = p8_pos, p8_vec, p8_ang
    if panel == "p9": pos, vec, ang = p9_pos, p9_vec, p9_ang
    if panel == "p10": pos, vec, ang = p10_pos, p10_vec, p10_ang
    if panel == "p11": pos, vec, ang = p11_pos, p11_vec, p11_ang
    if panel == "p12": pos, vec, ang = p12_pos, p12_vec, p12_ang
    if panel == "p13": pos, vec, ang = p13_pos, p13_vec, p13_ang
    if panel == "p14": pos, vec, ang = p14_pos, p14_vec, p14_ang
    if panel == "p15": pos, vec, ang = p15_pos, p15_vec, p15_ang
    if panel == "p16": pos, vec, ang = p16_pos, p16_vec, p16_ang
    if panel == "p17": pos, vec, ang = p17_pos, p17_vec, p17_ang
    if panel == "p18": pos, vec, ang = p18_pos, p18_vec, p18_ang
    if panel == "p19": pos, vec, ang = p19_pos, p19_vec, p19_ang
    if panel == "p20": pos, vec, ang = p20_pos, p20_vec, p20_ang
    if panel == "p21": pos, vec, ang = p21_pos, p21_vec, p21_ang
    if panel == "p22": pos, vec, ang = p22_pos, p22_vec, p22_ang
    if panel == "p23": pos, vec, ang = p23_pos, p23_vec, p23_ang
    if panel == "p24": pos, vec, ang = p24_pos, p24_vec, p24_ang
    if panel == "p25": pos, vec, ang = p25_pos, p25_vec, p25_ang
    pos_local = vec * pos[0] * 1000 - pygame.Vector3(0, -1, 0) * pos[1] * 1000 + vec[2] * 1000 * vec.rotate(90, [0, 1, 0])
    #pos_local = pygame.Vector3(-pos_local.x, pos_local.y, -pos_local.z)
    rot_local = ang
    #pos_global = pos_local.rotate(-pan_rot, [0, 1, 0]) / 100000 * 2 * scale + pan_pos
    #rot_global = rot_local + pan_rot
    return pgv3_arr(pygame.Vector3(-pos_local.x, pos_local.y, pos_local.z).rotate(pan_rot, [0, 1, 0]) / 100000 * 0.146 * 2 + pan_pos), 0 #return pgv3_arr(pos_global), rot_global
    p1 = pygame.Vector3(pans[panel][0])
    vec = pygame.Vector3(1, 0, 0).rotate(pans[panel][1], [0, 1, 0])
    p1_ = p1 + vec * pos[0] - pygame.Vector3(0, -1, 0) * pos[1] + pos[2] * vec.rotate(90, [0, 1, 0])
    p2 = pygame.Vector3(-p1_.x, p1_.y, p1_.z)
    p3 = p2.rotate(pan_rot + 180, [0, 1, 0])
    p4 = p3 * 1.46 * 2 + pan_pos
    return pgv3_arr(p4), pans[panel][1]
