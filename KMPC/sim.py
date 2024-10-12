import math

# Константы
global T_crit,R_steam,nominal_pressure
T_crit = 647.1  # Критическая температура для воды в K
R_steam = 461.5  # Газовая постоянная для воды в J/(kg·K)
nominal_pressure = 7.5e6  # Номинальное давление в петли 7.5 МПа

# Входные данные
TPower_1 = 1600e6  # Мощность реактора в Вт в первой петле (1600 МВт)
TPower_2 = 1600e6  # Мощность реактора в Вт во второй петле (1600 МВт)
GCN_n1 = 2         #Количество ГЦН в работе
GCN_n2 = 2         #Количество ГЦН в работе

#ДРК ГЦН
DRK_GCN_11 = 1
#Напор ГЦН
ZGCN_GCN_11 = 1

DRK_GCN_12 = 1
ZGCN_GCN_12 = 1

DRK_GCN_13 = 0
ZGCN_GCN_13 = 0

DRK_GCN_14 = 0
ZGCN_GCN_14 = 0

DRK_GCN_21 = 1
ZGCN_GCN_21 = 1

DRK_GCN_22 = 1
ZGCN_GCN_22 = 1

DRK_GCN_23 = 0
ZGCN_GCN_23 = 0

DRK_GCN_24 = 0
ZGCN_GCN_24 = 0

#Напор ПН
ZPN_1 = 1
ZPN_2 = 1
ZPN_3 = 1
ZPN_4 = 1
ZPN_5 = 0

#Питательные узлы
ZPU_11 = 1
ZPU_12 = 1
ZPU_13 = 0

ZPU_21 = 1
ZPU_22 = 1
ZPU_23 = 0

# Функция для расчета плотности и давления
def get_properties(T, phase):
    if phase == 'water':
        # Плотность воды
        rho = 1000 - 0.07 * (T - 273.15)  # Плотность воды
        # Давление воды (приближенное)
        p = 611.2 * math.exp(T / (T_crit - T + 273.15))  # Давление в Паскалях
    elif phase == 'steam':
        # Давление пара (используем соотношение для насыщенного пара)
        p = 611.2 * math.exp(T / (T_crit - T + 273.15))  # Давление в Паскалях
        # Плотность пара
        rho = p / (R_steam * (T + 273.15))  # Плотность в кг/м³
    else:
        raise ValueError("Неизвестная фаза")
    return rho, p

def KMPC_1(TPower_1,GCN_n1,DRK_GCN_11,DRK_GCN_12,DRK_GCN_13,DRK_GCN_14,expense_GCN_11,expense_GCN_12,expense_GCN_13,expense_GCN_14,ZPN_1,ZPN_2,ZPN_3,ZPN_4,ZPN_5,ZPU_11,ZPU_12,ZPU_13):

    print("***ЛЕВАЯ ПЕТЛЯ КМПЦ***")

    #Контроль ГЦН
    G_water_11 = DRK_GCN_11 * expense_GCN_11 * 2225
    G_water_12 = DRK_GCN_12 * expense_GCN_12 * 2225
    G_water_13 = DRK_GCN_13 * expense_GCN_13 * 2225
    G_water_14 = DRK_GCN_14 * expense_GCN_14 * 2225
    G_total_water_1 = (G_water_11 + G_water_12 + G_water_13 + G_water_14)
    print(f"Расход левой половины: {G_total_water_1 * 3.6:.2f} т/ч")

    if TPower_1 <1920e6:
        if GCN_n1 == 2:
            G_water_nominal = ((-3e-06*((TPower_1/1e6)**3) + 0.0094*((TPower_1/1e6)**2) - 2.3395*(TPower_1/1e6) + 27146)/3.6)/2
        if GCN_n1 == 3:
            G_water_nominal = ((4e-06*((TPower_1/1e6)**3) - 0.0131*((TPower_1/1e6)**2) + 13.361*(TPower_1/1e6) + 39181)/3.6)/3
    elif TPower_1 >1920e6 and GCN_n1 == 3:
        G_water_nominal = ((-6E-08*((TPower_1/1e6)**3) + 0.0003*((TPower_1/1e6)**2) - 0.0595*(TPower_1/1e6) + 6875.7) * 3)/3.6

    tolerance=0.1
    lower_bound = G_water_nominal * (1 - tolerance)  # Нижняя граница (90%)
    upper_bound = G_water_nominal * (1 + tolerance)  # Верхняя граница (110%)

    if lower_bound<=G_total_water_1<=upper_bound:
        print(f"Значение расхода ГЦН: {G_total_water_1 * 3.6:.2f} находится в пределах Gном: {G_water_nominal * 3.6:.2f}")
    elif G_total_water_1>=upper_bound:
        TPower_1 = TPower_1 * 0.95
        print(f"Значение расхода ГЦН: {G_total_water_1 * 3.6:.2f} превышено Gном: {G_water_nominal * 3.6:.2f}")
    elif G_total_water_1<=lower_bound:
        TPower_1 = TPower_1 * 1.05
        print(f"Значение расхода ГЦН: {G_total_water_1 * 3.6:.2f} занижено Gном: {G_water_nominal * 3.6:.2f}")

    # 1. Расчет давления на выходе из реактора (с учётом номинала)
    p_out_reactor_1 = nominal_pressure * (G_total_water_1 / G_water_nominal) * ((TPower_1 + 0.01)/3200e6)
    T_out1 = 20 + (TPower_1 * 0.084) / 1e6
    x_steam_1 = (TPower_1 * 4.767e-5) / 1e6 * 0.955 #Паросодержание, массовые доли (+ поправочный коэффициент)

    # 2. Выход пароводяной смеси из реактора
    rho_water_1, p_water1 = get_properties(T_out1, 'water')
    rho_steam_1, p_steam1 = get_properties(T_out1, 'steam')

    rho_mix_1 = (1 - x_steam_1) * rho_water_1 + x_steam_1 * rho_steam_1  # Плотность смеси
    Q_mix_1 = G_total_water_1 / rho_mix_1  # Объемный расход смеси (м^3/с)
    print(f"Температура ПВС на выходе из реактора: {T_out1:.2f} °C")
    print(f"Давление на выходе из реактора: {p_out_reactor_1 / 1e6:.2f} МПа")

    # 3. Потери давления в трубах
    v_mix = G_total_water_1 / rho_mix_1  # Скорость потока смеси (м/с)
    L = 61  # Длина трубопровода (м)
    D = 0.325  # Диаметр труб (м)
    μ = 0.000183/(1 + 0.0337 * T_out1 + 0.000221 * T_out1**2) #Вязкость
    Re = (rho_mix_1 * v_mix * D)/μ #Расчёт критерия Рейнольдса

    #Расчёт коэффициента трения от критерия Рейнольдса
    if Re==0:
        lambda_pipe = 0
    elif Re<2300:
        lambda_pipe = 64/Re
    elif Re>4000:
        lambda_pipe = 1/((-2*math.log10((0.01/(3.71 * D)) + (2.51/(Re * math.sqrt(μ)))))**2)
    # Потери давления (добавить для цикла ДЭ-ПЭ-БС-ГЦН)
    delta_p_pipe = lambda_pipe * (L / D) * (rho_mix_1 * v_mix ** 2) / 2
    if delta_p_pipe>p_out_reactor_1:
        p_after_pipes = p_out_reactor_1
    else:
        p_after_pipes = p_out_reactor_1 - delta_p_pipe  # Давление после труб

    print(f"Давление смеси после труб: {p_after_pipes / 1e6:.2f} МПа")

    # 4. Сепарация в барабан-сепараторе (давление принимаем равным после труб)
    p_bs = p_after_pipes
    q_steam = x_steam_1 * G_total_water_1

    # Проверка давления в барабан-сепараторе, оно не должно быть ниже номинального
    #if p_bs < nominal_pressure:
    #    print("qqq")

    # Температура пара в барабан-сепараторе
    T_steam = T_out1
    print(f"Давление в барабане-сепараторе: {p_bs / 1e6:.2f} МПа")
    print(f"Парообразование: {q_steam:.2f} кг/с")
    print(f"Температура пара в барабане-сепараторе: {T_steam:.2f} °C")
    
    #Сепаратор-пароперегреватель (острый пар)
    q_steam_SPP = 0.1 * q_steam
    q_steam = q_steam - q_steam_SPP
    print(f"Острый пар на СПП: {q_steam_SPP:.2f} кг/с")

    # 5. Поступление пара на турбину   
    #ЦВД
    #На перегрев в СПП
    steam_out_1 = 0.1 * q_steam
    #Для подогрев в деаэратор
    steam_out_2 = 0.05 * q_steam
    #На подогрев в ПНД-3,4
    steam_out_3 = 0.05 * q_steam
    steam_out_4 = 0.05 * q_steam
    q_steam = q_steam - (steam_out_1 + steam_out_2 + steam_out_3 + steam_out_4)
    #Pвыход ЦВД
    P_CVD = 0.293 * p_bs
    T_CVD = 35.53483 * math.log(P_CVD/1e6) + 209.26655
    
    #Сепаратор-пароперегреватель (перегрев пара с ЦВД)
    q_steam_SPP_total = q_steam_SPP + steam_out_1
    #На деаэратор
    q_mix_SPP_1 = 2/3 * q_steam_SPP_total
    #На ПНД-3
    q_mix_SPP_2 = q_steam_SPP_total - q_mix_SPP_1
    print(f"Расход пара через СПП: {q_steam_SPP_total:.2f} кг/с")
    
    #Pвыход ЦСД
    P_CSD = 0.074 * p_bs
    T_CSD = 35.53483 * math.log(P_CSD/1e6) + 209.26655

    #ЦНД
    #На подогрев в ПНД-5,6,7
    steam_out_5 = 0.05 * q_steam
    steam_out_6 = 0.05 * q_steam
    steam_out_7 = 0.05 * q_steam
    q_steam = q_steam - (steam_out_5 + steam_out_6 + steam_out_7)

    #Pвыход ЦНД
    P_CND = 0.0023 * p_bs
    T_CND = 35.53483 * math.log(P_CND/1e6) + 209.26655
    
    # 6. Конденсация пара
    #Подогреватели низкого давления
    q_PND_1 = steam_out_7
    q_PND_2 = steam_out_6
    q_PND_3 = steam_out_5 + q_mix_SPP_2
    q_PND_4 = steam_out_4
    q_PND_5 = steam_out_3
    print(f"Расход ПНД-1 {q_PND_1:.2f} кг/с")
    print(f"Расход ПНД-2 {q_PND_2:.2f} кг/с")
    print(f"Расход ПНД-3 {q_PND_3:.2f} кг/с")
    print(f"Расход ПНД-4 {q_PND_4:.2f} кг/с")
    print(f"Расход ПНД-5 {q_PND_5:.2f} кг/с")
    #Расход на охладителе дренажа с ПНД
    q_OD = q_PND_1 + q_PND_2 + q_PND_3 + q_PND_4 + q_PND_5
    print(f"Расход ОД {q_OD:.2f} кг/с")
    
    T_cond = 0.121 * T_out1 # Температура на выходе из конденсатора
    m_only_after_CND = q_steam
    m_cond = q_steam + q_OD  # Масса сконденсированной воды
    print(f"Масса воды после конденсата с ЦНД: {m_only_after_CND:.2f} кг/с")
    print(f"Масса воды перед КН1: {m_cond:.2f} кг/с")
    print(f"Температура конденсата: {T_cond:.2f} °C")
    
    #КН1
    q_KN1 = q_KN2 = m_cond
    #Давление на выходе КН1
    p_KN1 = P_CND + q_KN1 * 0.00419e6
    #T_after_KN1 = 35.53483 * math.log(p_KN1/1e6) + 209.26655
    print(f"Давление на выходе КН1: {p_KN1/1e6:.2f} МПа")
    #print(f"Температура на выходе КН1: {T_after_KN1} МПа")
    #КН2
    #Давление на выходе КН2
    p_KN2 = p_KN1 + q_KN2 * 0.00419e6
    #T_after_KN2 = 35.53483 * math.log(p_KN2/1e6) + 209.26655
    print(f"Давление на выходе КН2: {p_KN2/1e6:.2f} МПа")
    #print(f"Температура на выходе КН2: {T_after_KN2} МПа")

    #Потери давления в трубах от КН2 до ДЭ
    rho_water_KN2, p_water1 = get_properties(T_cond, 'water')
    v_mix = q_KN2 / rho_water_KN2  # Скорость потока конденсата (м/с)
    L = 61  # Длина трубопровода (м)
    D = 0.325  # Диаметр труб (м)
    μ = 0.000183/(1 + 0.0337 * T_cond + 0.000221 * T_cond**2) #Вязкость
    Re = (rho_water_KN2 * v_mix * D)/μ #Расчёт критерия Рейнольдса

    #Расчёт коэффициента трения от критерия Рейнольдса
    if Re==0:
        lambda_pipe = 0
    elif Re<2300:
        lambda_pipe = 64/Re
    elif Re>4000:
        lambda_pipe = 1/((-2*math.log10((0.01/(3.71 * D)) + (2.51/(Re * math.sqrt(μ)))))**2)

    # Потери давления (добавить для цикла ДЭ-ПЭ-БС-ГЦН)
    delta_p_pipe = lambda_pipe * (L / D) * (rho_water_KN2 * v_mix ** 2) / 2
    if delta_p_pipe>p_KN2:
        pass
    else:
        p_KN2 = p_KN2 - delta_p_pipe  # Давление после труб

    print(f"Давление смеси после КН2: {p_KN2 / 1e6:.2f} МПа")

    #Нагрев ПНД
    t1 = T_cond
    t2 = t1 * 1.162
    t3 = t2 * 1.162
    t4 = t3 * 1.162
    t5 = t4 * 1.162
    t6 = t5 * 1.162
    t7 = t6 * 1.162
    
    #Деаэратор
    q_water_deaerator = q_KN2 + q_mix_SPP_1 + steam_out_2
    p_deaerator = p_KN2
    T_water_before_deaerator = t7
    print(f"Расход воды через деаэратор: {q_water_deaerator:.2f} кг/c")
    print(f"Температура воды на входе в деаэратор: {T_water_before_deaerator:.2f} °C")
    print(f"Давление в деаэраторе: {p_deaerator/1e6:.2f} МПа")
    
    #Питательные насосы
    if ZPN_1 and ZPN_2 and ZPN_3 and ZPN_4 and ZPN_5>0:
        #ПН-1
        m_PN1 = q_water_deaerator/5 * ZPN_1
        if m_PN1>400:
            print('WARNING! Количество воды через ПЭН-1 на максимальном уровне!')
        #ПН-2
        m_PN2 = q_water_deaerator/5 * ZPN_2
        if m_PN2>400:
            print('WARNING! Количество воды через ПЭН-2 на максимальном уровне!')
        #ПН-3
        m_PN3 = q_water_deaerator/5 * ZPN_3
        if m_PN3>400:
            print('WARNING! Количество воды через ПЭН-3 на максимальном уровне!')
        #ПН-4
        m_PN4 = q_water_deaerator/5 * ZPN_4
        if m_PN4>400:
            print('WARNING! Количество воды через ПЭН-4 на максимальном уровне!')
        #ПН-5
        m_PN5 = q_water_deaerator/5 * ZPN_5
        if m_PN5>400:
            print('WARNING! Количество воды через ПЭН-5 на максимальном уровне!')
        m_PU_1 = m_PN1 + m_PN2 + m_PN3 + m_PN4 + m_PN5
    elif ZPN_5==0:
        #ПН-1
        m_PN1 = q_water_deaerator/4 * ZPN_1
        if m_PN1>400:
            print('WARNING! Количество воды через ПЭН-1 на максимальном уровне!')
        #ПН-2
        m_PN2 = q_water_deaerator/4 * ZPN_2
        if m_PN2>400:
            print('WARNING! Количество воды через ПЭН-2 на максимальном уровне!')
        #ПН-3
        m_PN3 = q_water_deaerator/4 * ZPN_3
        if m_PN3>400:
            print('WARNING! Количество воды через ПЭН-3 на максимальном уровне!')
        #ПН-4
        m_PN4 = q_water_deaerator/4 * ZPN_4
        if m_PN4>400:
            print('WARNING! Количество воды через ПЭН-4 на максимальном уровне!')
        m_PU_1 = m_PN1 + m_PN2 + m_PN3 + m_PN4
        
    #Питательный узел (ПУ)
    if ZPU_11 and ZPU_12 and ZPU_13>0:
        m_water_nitka_PU_11 = m_PU_1/3 * ZPU_11
        if m_water_nitka_PU_11>450:
            print('WARNING! Количество воды через нитку 11 ПУ-1 на максимальном уровне!')
        m_water_nitka_PU_12 = m_PU_1/3 * ZPU_12
        if m_water_nitka_PU_12>450:
            print('WARNING! Количество воды через нитку 12 ПУ-1 на максимальном уровне!')
        m_water_nitka_PU_13 = m_PU_1/3 * ZPU_13
        if m_water_nitka_PU_13>450:
            print('WARNING! Количество воды через нитку 13 ПУ-1 на максимальном уровне!')
        m_feedwater_1 = m_water_nitka_PU_11 + m_water_nitka_PU_12 + m_water_nitka_PU_13
    elif ZPU_13==0:
        m_water_nitka_PU_11 = m_PU_1/2 * ZPU_11
        if m_water_nitka_PU_11>450:
            print('WARNING! Количество воды через нитку 11 ПУ-1 на максимальном уровне!')
        m_water_nitka_PU_12 = m_PU_1/2 * ZPU_12
        if m_water_nitka_PU_12>450:
            print('WARNING! Количество воды через нитку 12 ПУ-1 на максимальном уровне!')
        m_feedwater_1 = m_water_nitka_PU_11 + m_water_nitka_PU_12
        

    #Потери давления в трубах от ПН до БС
    rho_water_PN, p_water1 = get_properties(T_water_before_deaerator, 'water')
    v_mix = m_feedwater_1 / rho_water_PN  # Скорость потока конденсата (м/с)
    L = 61  # Длина трубопровода (м)
    D = 0.325  # Диаметр труб (м)
    μ = 0.000183/(1 + 0.0337 * T_water_before_deaerator + 0.000221 * T_water_before_deaerator**2) #Вязкость
    Re = (rho_water_PN * v_mix * D)/μ #Расчёт критерия Рейнольдса

    #Расчёт коэффициента трения от критерия Рейнольдса
    if Re==0:
        lambda_pipe = 0
    elif Re<2300:
        lambda_pipe = 64/Re
    elif Re>4000:
        lambda_pipe = 1/((-2*math.log10((0.01/(3.71 * D)) + (2.51/(Re * math.sqrt(μ)))))**2)

    delta_p_pipe = lambda_pipe * (L / D) * (rho_water_PN * v_mix ** 2) / 2
    if delta_p_pipe>p_deaerator:
        P_after_PN = p_deaerator
    else:
        P_after_PN = p_deaerator - delta_p_pipe  # Давление после труб

    print(f"Давление смеси после ПН: {P_after_PN / 1e6:.2f} МПа")

    #Возвращение питательной воды в БС
    m_water_after_BS = G_total_water_1 * (1 - x_steam_1) + m_feedwater_1
    T_feedwater_BS = 35.53483 * math.log(P_after_PN/1e6) + 209.26655

    #Потери давления в трубах от БС до ГЦН
    rho_water_GCN, p_water1 = get_properties(T_feedwater_BS, 'water')
    v_mix = m_water_after_BS / rho_water_GCN  # Скорость потока конденсата (м/с)
    L = 61  # Длина трубопровода (м)
    D = 0.325  # Диаметр труб (м)
    μ = 0.000183/(1 + 0.0337 * T_feedwater_BS + 0.000221 * T_feedwater_BS**2) #Вязкость
    Re = (rho_water_GCN * v_mix * D)/μ #Расчёт критерия Рейнольдса

    #Расчёт коэффициента трения от критерия Рейнольдса
    if Re==0:
        lambda_pipe = 0
    elif Re<2300:
        lambda_pipe = 64/Re
    elif Re>4000:
        lambda_pipe = 1/((-2*math.log10((0.01/(3.71 * D)) + (2.51/(Re * math.sqrt(μ)))))**2)
    delta_p_pipe = lambda_pipe * (L / D) * (rho_water_GCN * v_mix ** 2) / 2
    if delta_p_pipe>P_after_PN:
        P_after_BS = P_after_PN
    else:
        P_after_BS = P_after_PN - delta_p_pipe  # Давление после труб

    print(f"Давление смеси после БС: {P_after_BS / 1e6:.2f} МПа")

    # 7. Возвращение воды через ГЦН
    P_after_GCN = P_after_BS * 1.231
    T_in = 20 + (TPower_1 * 0.077) / 1e6
    print(f"Расход воды через ГЦН: {m_water_after_BS * 3.6:.2f} т/ч")
    print(f"Температура воды на входе в реактора: {T_in:.2f} °C")
    print(f"Давление воды на входе в реактора: {P_after_GCN/1e6:.2f} МПа")



def KMPC_2(TPower_2,GCN_n2,DRK_GCN_21,DRK_GCN_22,DRK_GCN_23,DRK_GCN_24,expense_GCN_21,expense_GCN_22,expense_GCN_23,expense_GCN_24,ZPN_1,ZPN_2,ZPN_3,ZPN_4,ZPN_5,ZPU_21,ZPU_22,ZPU_23):

    print("***ПРАВАЯ ПЕТЛЯ КМПЦ***")

    #Контроль ГЦН
    G_water_21 = DRK_GCN_21 * expense_GCN_21 * 2225
    G_water_22 = DRK_GCN_22 * expense_GCN_22 * 2225
    G_water_23 = DRK_GCN_23 * expense_GCN_23 * 2225
    G_water_24 = DRK_GCN_24 * expense_GCN_24 * 2225
    G_total_water_2 = (G_water_21 + G_water_22 + G_water_23 + G_water_24)
    print(f"Расход правой половины: {G_total_water_2 * 3.6:.2f} т/ч")

    if TPower_2 <1920e6:
        if GCN_n2 == 2:
            G_water_nominal = ((-3e-06*((TPower_2/1e6)**3) + 0.0094*((TPower_2/1e6)**2) - 2.3395*(TPower_2/1e6) + 27146)/3.6)/2
        if GCN_n2 == 3:
            G_water_nominal = ((4e-06*((TPower_2/1e6)**3) - 0.0131*((TPower_2/1e6)**2) + 13.361*(TPower_2/1e6) + 39181)/3.6)/3
    elif TPower_2 >1920e6 and GCN_n2 == 3:
        G_water_nominal = ((-6E-08*((TPower_2/1e6)**3) + 0.0003*((TPower_2/1e6)**2) - 0.0595*(TPower_2/1e6) + 6875.7) * 3)/3.6

    tolerance=0.1
    lower_bound = G_water_nominal * (1 - tolerance)  # Нижняя граница (90%)
    upper_bound = G_water_nominal * (1 + tolerance)  # Верхняя граница (110%)

    if lower_bound<=G_total_water_2<=upper_bound:
        print(f"Значение расхода ГЦН: {G_total_water_2 * 3.6:.2f} находится в пределах Gном: {G_water_nominal * 3.6:.2f}")
    elif G_total_water_2>=upper_bound:
        TPower_2 = TPower_2 * 0.95
        print(f"Значение расхода ГЦН: {G_total_water_2 * 3.6:.2f} превышено Gном: {G_water_nominal * 3.6:.2f}")
    elif G_total_water_2<=lower_bound:
        TPower_2 = TPower_2 * 1.05
        print(f"Значение расхода ГЦН: {G_total_water_2 * 3.6:.2f} занижено Gном: {G_water_nominal * 3.6:.2f}")

    # 1. Расчет давления на выходе из реактора (с учётом номинала)
    p_out_reactor_2 = nominal_pressure * (G_total_water_2 / G_water_nominal) * ((TPower_2 + 0.01)/3200e6)
    T_out2 = 20 + (TPower_2 * 0.084) / 1e6
    x_steam_2 = (TPower_2 * 4.767e-5) / 1e6 * 0.955 #Паросодержание, массовые доли (+ поправочный коэффициент)

    # 2. Выход пароводяной смеси из реактора
    rho_water_2, p_water1 = get_properties(T_out2, 'water')
    rho_steam_2, p_steam1 = get_properties(T_out2, 'steam')

    rho_mix_2 = (1 - x_steam_2) * rho_water_2 + x_steam_2 * rho_steam_2  # Плотность смеси
    Q_mix_2 = G_total_water_2 / rho_mix_2  # Объемный расход смеси (м^3/с)
    print(f"Температура ПВС на выходе из реактора: {T_out2:.2f} °C")
    print(f"Давление на выходе из реактора: {p_out_reactor_2 / 1e6:.2f} МПа")

    # 3. Потери давления в трубах
    v_mix = G_total_water_2 / rho_mix_2  # Скорость потока смеси (м/с)
    L = 61  # Длина трубопровода (м)
    D = 0.325  # Диаметр труб (м)
    μ = 0.000183/(1 + 0.0337 * T_out2 + 0.000221 * T_out2**2) #Вязкость
    Re = (rho_mix_2 * v_mix * D)/μ #Расчёт критерия Рейнольдса

    #Расчёт коэффициента трения от критерия Рейнольдса
    if Re==0:
        lambda_pipe = 0
    elif Re<2300:
        lambda_pipe = 64/Re
    elif Re>4000:
        lambda_pipe = 1/((-2*math.log10((0.01/(3.71 * D)) + (2.51/(Re * math.sqrt(μ)))))**2)
    # Потери давления (добавить для цикла ДЭ-ПЭ-БС-ГЦН)
    delta_p_pipe = lambda_pipe * (L / D) * (rho_mix_2 * v_mix ** 2) / 2
    if delta_p_pipe>p_out_reactor_2:
        p_after_pipes = p_out_reactor_2
    else:
        p_after_pipes = p_out_reactor_2 - delta_p_pipe  # Давление после труб

    print(f"Давление смеси после труб: {p_after_pipes / 1e6:.2f} МПа")

    # 4. Сепарация в барабан-сепараторе (давление принимаем равным после труб)
    p_bs = p_after_pipes
    q_steam = x_steam_2 * G_total_water_2

    # Проверка давления в барабан-сепараторе, оно не должно быть ниже номинального
    #if p_bs < nominal_pressure:
    #    print("qqq")

    # Температура пара в барабан-сепараторе
    T_steam = T_out2
    print(f"Давление в барабане-сепараторе: {p_bs / 1e6:.2f} МПа")
    print(f"Парообразование: {q_steam:.2f} кг/с")
    print(f"Температура пара в барабане-сепараторе: {T_steam:.2f} °C")
    
    #Сепаратор-пароперегреватель (острый пар)
    q_steam_SPP = 0.1 * q_steam
    q_steam = q_steam - q_steam_SPP
    print(f"Острый пар на СПП: {q_steam_SPP:.2f} кг/с")

    # 5. Поступление пара на турбину   
    #ЦВД
    #На перегрев в СПП
    steam_out_1 = 0.1 * q_steam
    #Для подогрев в деаэратор
    steam_out_2 = 0.05 * q_steam
    #На подогрев в ПНД-3,4
    steam_out_3 = 0.05 * q_steam
    steam_out_4 = 0.05 * q_steam
    q_steam = q_steam - (steam_out_1 + steam_out_2 + steam_out_3 + steam_out_4)
    #Pвыход ЦВД
    P_CVD = 0.293 * p_bs
    T_CVD = 35.53483 * math.log(P_CVD/1e6) + 209.26655
    
    #Сепаратор-пароперегреватель (перегрев пара с ЦВД)
    q_steam_SPP_total = q_steam_SPP + steam_out_1
    #На деаэратор
    q_mix_SPP_1 = 2/3 * q_steam_SPP_total
    #На ПНД-3
    q_mix_SPP_2 = q_steam_SPP_total - q_mix_SPP_1
    print(f"Расход пара через СПП: {q_steam_SPP_total:.2f} кг/с")
    
    #Pвыход ЦСД
    P_CSD = 0.074 * p_bs
    T_CSD = 35.53483 * math.log(P_CSD/1e6) + 209.26655

    #ЦНД
    #На подогрев в ПНД-5,6,7
    steam_out_5 = 0.05 * q_steam
    steam_out_6 = 0.05 * q_steam
    steam_out_7 = 0.05 * q_steam
    q_steam = q_steam - (steam_out_5 + steam_out_6 + steam_out_7)

    #Pвыход ЦНД
    P_CND = 0.0023 * p_bs
    T_CND = 35.53483 * math.log(P_CND/1e6) + 209.26655
    
    # 6. Конденсация пара
    #Подогреватели низкого давления
    q_PND_1 = steam_out_7
    q_PND_2 = steam_out_6
    q_PND_3 = steam_out_5 + q_mix_SPP_2
    q_PND_4 = steam_out_4
    q_PND_5 = steam_out_3
    print(f"Расход ПНД-1 {q_PND_1:.2f} кг/с")
    print(f"Расход ПНД-2 {q_PND_2:.2f} кг/с")
    print(f"Расход ПНД-3 {q_PND_3:.2f} кг/с")
    print(f"Расход ПНД-4 {q_PND_4:.2f} кг/с")
    print(f"Расход ПНД-5 {q_PND_5:.2f} кг/с")
    #Расход на охладителе дренажа с ПНД
    q_OD = q_PND_1 + q_PND_2 + q_PND_3 + q_PND_4 + q_PND_5
    print(f"Расход ОД {q_OD:.2f} кг/с")
    
    T_cond = 0.121 * T_out2 # Температура на выходе из конденсатора
    m_only_after_CND = q_steam
    m_cond = q_steam + q_OD  # Масса сконденсированной воды
    print(f"Масса воды после конденсата с ЦНД: {m_only_after_CND:.2f} кг/с")
    print(f"Масса воды перед КН1: {m_cond:.2f} кг/с")
    print(f"Температура конденсата: {T_cond:.2f} °C")
    
    #КН1
    q_KN1 = q_KN2 = m_cond
    #Давление на выходе КН1
    p_KN1 = P_CND + q_KN1 * 0.00419e6
    #T_after_KN1 = 35.53483 * math.log(p_KN1/1e6) + 209.26655
    print(f"Давление на выходе КН1: {p_KN1/1e6:.2f} МПа")
    #print(f"Температура на выходе КН1: {T_after_KN1} МПа")
    #КН2
    #Давление на выходе КН2
    p_KN2 = p_KN1 + q_KN2 * 0.00419e6
    #T_after_KN2 = 35.53483 * math.log(p_KN2/1e6) + 209.26655
    print(f"Давление на выходе КН2: {p_KN2/1e6:.2f} МПа")
    #print(f"Температура на выходе КН2: {T_after_KN2} МПа")

    #Потери давления в трубах от КН2 до ДЭ
    rho_water_KN2, p_water1 = get_properties(T_cond, 'water')
    v_mix = q_KN2 / rho_water_KN2  # Скорость потока конденсата (м/с)
    L = 61  # Длина трубопровода (м)
    D = 0.325  # Диаметр труб (м)
    μ = 0.000183/(1 + 0.0337 * T_cond + 0.000221 * T_cond**2) #Вязкость
    Re = (rho_water_KN2 * v_mix * D)/μ #Расчёт критерия Рейнольдса

    #Расчёт коэффициента трения от критерия Рейнольдса
    if Re==0:
        lambda_pipe = 0
    elif Re<2300:
        lambda_pipe = 64/Re
    elif Re>4000:
        lambda_pipe = 1/((-2*math.log10((0.01/(3.71 * D)) + (2.51/(Re * math.sqrt(μ)))))**2)

    # Потери давления (добавить для цикла ДЭ-ПЭ-БС-ГЦН)
    delta_p_pipe = lambda_pipe * (L / D) * (rho_water_KN2 * v_mix ** 2) / 2
    if delta_p_pipe>p_KN2:
        pass
    else:
        p_KN2 = p_KN2 - delta_p_pipe  # Давление после труб

    print(f"Давление смеси после КН2: {p_KN2 / 1e6:.2f} МПа")

    #Нагрев ПНД
    t1 = T_cond
    t2 = t1 * 1.162
    t3 = t2 * 1.162
    t4 = t3 * 1.162
    t5 = t4 * 1.162
    t6 = t5 * 1.162
    t7 = t6 * 1.162
    
    #Деаэратор
    q_water_deaerator = q_KN2 + q_mix_SPP_1 + steam_out_2
    p_deaerator = p_KN2
    T_water_before_deaerator = t7
    print(f"Расход воды через деаэратор: {q_water_deaerator:.2f} кг/c")
    print(f"Температура воды на входе в деаэратор: {T_water_before_deaerator:.2f} °C")
    print(f"Давление в деаэраторе: {p_deaerator/1e6:.2f} МПа")
    
    #Питательные насосы
    if ZPN_1 and ZPN_2 and ZPN_3 and ZPN_4 and ZPN_5>0:
        #ПН-1
        m_PN1 = q_water_deaerator/5 * ZPN_1
        if m_PN1>400:
            print('WARNING! Количество воды через ПЭН-1 на максимальном уровне!')
        #ПН-2
        m_PN2 = q_water_deaerator/5 * ZPN_2
        if m_PN2>400:
            print('WARNING! Количество воды через ПЭН-2 на максимальном уровне!')
        #ПН-3
        m_PN3 = q_water_deaerator/5 * ZPN_3
        if m_PN3>400:
            print('WARNING! Количество воды через ПЭН-3 на максимальном уровне!')
        #ПН-4
        m_PN4 = q_water_deaerator/5 * ZPN_4
        if m_PN4>400:
            print('WARNING! Количество воды через ПЭН-4 на максимальном уровне!')
        #ПН-5
        m_PN5 = q_water_deaerator/5 * ZPN_5
        if m_PN5>400:
            print('WARNING! Количество воды через ПЭН-5 на максимальном уровне!')
        m_PU_1 = m_PN1 + m_PN2 + m_PN3 + m_PN4 + m_PN5
    elif ZPN_5==0:
        #ПН-1
        m_PN1 = q_water_deaerator/4 * ZPN_1
        if m_PN1>400:
            print('WARNING! Количество воды через ПЭН-1 на максимальном уровне!')
        #ПН-2
        m_PN2 = q_water_deaerator/4 * ZPN_2
        if m_PN2>400:
            print('WARNING! Количество воды через ПЭН-2 на максимальном уровне!')
        #ПН-3
        m_PN3 = q_water_deaerator/4 * ZPN_3
        if m_PN3>400:
            print('WARNING! Количество воды через ПЭН-3 на максимальном уровне!')
        #ПН-4
        m_PN4 = q_water_deaerator/4 * ZPN_4
        if m_PN4>400:
            print('WARNING! Количество воды через ПЭН-4 на максимальном уровне!')
        m_PU_1 = m_PN1 + m_PN2 + m_PN3 + m_PN4
        
    #Питательный узел (ПУ)
    if ZPU_21 and ZPU_22 and ZPU_23>0:
        m_water_nitka_PU_21 = m_PU_1/3 * ZPU_21
        if m_water_nitka_PU_21>450:
            print('WARNING! Количество воды через нитку 21 ПУ-2 на максимальном уровне!')
        m_water_nitka_PU_22 = m_PU_1/3 * ZPU_22
        if m_water_nitka_PU_22>450:
            print('WARNING! Количество воды через нитку 22 ПУ-2 на максимальном уровне!')
        m_water_nitka_PU_23 = m_PU_1/3 * ZPU_23
        if m_water_nitka_PU_23>450:
            print('WARNING! Количество воды через нитку 23 ПУ-2 на максимальном уровне!')
        m_feedwater_2 = m_water_nitka_PU_21 + m_water_nitka_PU_22 + m_water_nitka_PU_23
    elif ZPU_23==0:
        m_water_nitka_PU_21 = m_PU_1/2 * ZPU_21
        if m_water_nitka_PU_21>450:
            print('WARNING! Количество воды через нитку 21 ПУ-2 на максимальном уровне!')
        m_water_nitka_PU_22 = m_PU_1/2 * ZPU_22
        if m_water_nitka_PU_22>450:
            print('WARNING! Количество воды через нитку 22 ПУ-2 на максимальном уровне!')
        m_feedwater_2 = m_water_nitka_PU_21 + m_water_nitka_PU_22
        

    #Потери давления в трубах от ПН до БС
    rho_water_PN, p_water = get_properties(T_water_before_deaerator, 'water')
    v_mix = m_feedwater_2 / rho_water_PN  # Скорость потока конденсата (м/с)
    L = 61  # Длина трубопровода (м)
    D = 0.325  # Диаметр труб (м)
    μ = 0.000183/(1 + 0.0337 * T_water_before_deaerator + 0.000221 * T_water_before_deaerator**2) #Вязкость
    Re = (rho_water_PN * v_mix * D)/μ #Расчёт критерия Рейнольдса

    #Расчёт коэффициента трения от критерия Рейнольдса
    if Re==0:
        lambda_pipe = 0
    elif Re<2300:
        lambda_pipe = 64/Re
    elif Re>4000:
        lambda_pipe = 1/((-2*math.log10((0.01/(3.71 * D)) + (2.51/(Re * math.sqrt(μ)))))**2)

    delta_p_pipe = lambda_pipe * (L / D) * (rho_water_PN * v_mix ** 2) / 2
    if delta_p_pipe>p_deaerator:
        P_after_PN = p_deaerator
    else:
        P_after_PN = p_deaerator - delta_p_pipe  # Давление после труб

    print(f"Давление смеси после ПН: {P_after_PN / 1e6:.2f} МПа")

    #Возвращение питательной воды в БС
    m_water_after_BS = G_total_water_2 * (1 - x_steam_2) + m_feedwater_2
    T_feedwater_BS = 35.53483 * math.log(P_after_PN/1e6) + 209.26655

    #Потери давления в трубах от БС до ГЦН
    rho_water_GCN, p_water1 = get_properties(T_feedwater_BS, 'water')
    v_mix = m_water_after_BS / rho_water_GCN  # Скорость потока конденсата (м/с)
    L = 61  # Длина трубопровода (м)
    D = 0.325  # Диаметр труб (м)
    μ = 0.000183/(1 + 0.0337 * T_feedwater_BS + 0.000221 * T_feedwater_BS**2) #Вязкость
    Re = (rho_water_GCN * v_mix * D)/μ #Расчёт критерия Рейнольдса

    #Расчёт коэффициента трения от критерия Рейнольдса
    if Re==0:
        lambda_pipe = 0
    elif Re<2300:
        lambda_pipe = 64/Re
    elif Re>4000:
        lambda_pipe = 1/((-2*math.log10((0.01/(3.71 * D)) + (2.51/(Re * math.sqrt(μ)))))**2)
    delta_p_pipe = lambda_pipe * (L / D) * (rho_water_GCN * v_mix ** 2) / 2
    if delta_p_pipe>P_after_PN:
        P_after_BS = P_after_PN
    else:
        P_after_BS = P_after_PN - delta_p_pipe  # Давление после труб

    print(f"Давление смеси после БС: {P_after_BS / 1e6:.2f} МПа")

    # 7. Возвращение воды через ГЦН
    P_after_GCN = P_after_BS * 1.231
    T_in = 20 + (TPower_2 * 0.077) / 1e6
    print(f"Расход воды через ГЦН: {m_water_after_BS * 3.6:.2f} т/ч")
    print(f"Температура воды на входе в реактора: {T_in:.2f} °C")
    print(f"Давление воды на входе в реактора: {P_after_GCN/1e6:.2f} МПа")

KMPC_1(TPower_1,GCN_n1,DRK_GCN_11,DRK_GCN_12,DRK_GCN_13,DRK_GCN_14,ZGCN_GCN_11,ZGCN_GCN_12,ZGCN_GCN_13,ZGCN_GCN_14,ZPN_1,ZPN_2,ZPN_3,ZPN_4,ZPN_5,ZPU_11,ZPU_12,ZPU_13)
KMPC_2(TPower_2,GCN_n2,DRK_GCN_21,DRK_GCN_22,DRK_GCN_23,DRK_GCN_24,ZGCN_GCN_21,ZGCN_GCN_22,ZGCN_GCN_23,ZGCN_GCN_24,ZPN_1,ZPN_2,ZPN_3,ZPN_4,ZPN_5,ZPU_21,ZPU_22,ZPU_23)
