import math
import numpy as np
import matplotlib.pyplot as plt

# Константы
global T_crit,R_steam,nominal_pressure,ambient_temp
T_crit = 647.1  # Критическая температура для воды в K
ambient_temp = 11 #Температура "холодного" реактора
R_steam = 461.5  # Газовая постоянная для воды в J/(kg·K)
nominal_pressure = 7.5e6  # Номинальное давление в петли 7.5 МПа

# Входные данные
TPower_1 = 3200e6  # Мощность реактора в Вт в первой петле (1600 МВт)
TPower_2 = 3200e6  # Мощность реактора в Вт во второй петле (1600 МВт)
GCN_n1 = 3         #Количество ГЦН в работе
GCN_n2 = 3         #Количество ГЦН в работе

#ДРК ГЦН
DRK_GCN_11 = 1
#Напор ГЦН
ZGCN_GCN_11 = 0.9

DRK_GCN_12 = 1
ZGCN_GCN_12 = 0.9

DRK_GCN_13 = 1
ZGCN_GCN_13 = 0.9

DRK_GCN_14 = 0
ZGCN_GCN_14 = 0

DRK_GCN_21 = 1
ZGCN_GCN_21 = 0.9

DRK_GCN_22 = 1
ZGCN_GCN_22 = 0.9

DRK_GCN_23 = 1
ZGCN_GCN_23 = 0.9

DRK_GCN_24 = 0
ZGCN_GCN_24 = 0

#Напор ПН первой половины
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

#СК ТГ
SK1_TG1 = True
SK2_TG1 = True
SK1_TG2 = True
SK2_TG2 = True

#Разгон ТГ
RTG1 = True
RTG2 = True
alpha1 = 200
alpha2 = 200

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

print("***РАБОТА КМПЦ***")
#Контроль ГЦН
G_water_11 = DRK_GCN_11 * ZGCN_GCN_11 * 2225
G_water_12 = DRK_GCN_12 * ZGCN_GCN_12 * 2225
G_water_13 = DRK_GCN_13 * ZGCN_GCN_13 * 2225
G_water_14 = DRK_GCN_14 * ZGCN_GCN_14 * 2225
G_total_water_1 = (G_water_11 + G_water_12 + G_water_13 + G_water_14)

G_water_21 = DRK_GCN_21 * ZGCN_GCN_21 * 2225
G_water_22 = DRK_GCN_22 * ZGCN_GCN_22 * 2225
G_water_23 = DRK_GCN_23 * ZGCN_GCN_23 * 2225
G_water_24 = DRK_GCN_24 * ZGCN_GCN_24 * 2225
G_total_water_2 = (G_water_21 + G_water_22 + G_water_23 + G_water_24)

print(f"Расход левой половины: {G_total_water_1 * 3.6:.2f} т/ч")
print(f"Расход право половины: {G_total_water_2 * 3.6:.2f} т/ч")

if TPower_1 <1920e6:
    if GCN_n1 == 2:
        G_water_nominal1 = ((-3e-06*((TPower_1/1e6)**3) + 0.0094*((TPower_1/1e6)**2) - 2.3395*(TPower_1/1e6) + 27146)/3.6)/2
    if GCN_n1 == 3:
        G_water_nominal1 = ((4e-06*((TPower_1/1e6)**3) - 0.0131*((TPower_1/1e6)**2) + 13.361*(TPower_1/1e6) + 39181)/3.6)/3
else: 
    G_water_nominal1 = ((-6E-08*((TPower_1/1e6)**3) + 0.0003*((TPower_1/1e6)**2) - 0.0595*(TPower_1/1e6) + 6875.7) * 3)/3.6
if TPower_2 <1920e6:
    if GCN_n2 == 2:
        G_water_nominal2 = ((-3e-06*((TPower_2/1e6)**3) + 0.0094*((TPower_2/1e6)**2) - 2.3395*(TPower_2/1e6) + 27146)/3.6)/2
    if GCN_n2 == 3:
        G_water_nominal2 = ((4e-06*((TPower_2/1e6)**3) - 0.0131*((TPower_2/1e6)**2) + 13.361*(TPower_2/1e6) + 39181)/3.6)/3
else: 
    G_water_nominal2 = ((-6E-08*((TPower_2/1e6)**3) + 0.0003*((TPower_2/1e6)**2) - 0.0595*(TPower_2/1e6) + 6875.7) * 3)/3.6

tolerance=0.1
lower_bound1 = G_water_nominal1 * (1 - tolerance)  # Нижняя граница (90%)
upper_bound1 = G_water_nominal1 * (1 + tolerance)  # Верхняя граница (110%)
lower_bound2 = G_water_nominal2 * (1 - tolerance)  # Нижняя граница (90%)
upper_bound2 = G_water_nominal2 * (1 + tolerance)  # Верхняя граница (110%)


if lower_bound1<=G_total_water_1<=upper_bound1:
    print(f"Значение расхода ГЦН левой половины: {G_total_water_1 * 3.6:.2f} находится в пределах Gном: {G_water_nominal1 * 3.6:.2f}")
elif G_total_water_1>=upper_bound1:
    TPower_1 = TPower_1 * 0.95
    print(f"Значение расхода ГЦН левой половины: {G_total_water_1 * 3.6:.2f} превышено Gном: {G_water_nominal1 * 3.6:.2f}")
else:
    TPower_1 = TPower_1 * 1.05
    print(f"Значение расхода ГЦН левой половины: {G_total_water_1 * 3.6:.2f} занижено Gном: {G_water_nominal1 * 3.6:.2f}")
if lower_bound2<=G_total_water_2<=upper_bound2:
    print(f"Значение расхода ГЦН правой половины: {G_total_water_2 * 3.6:.2f} находится в пределах Gном: {G_water_nominal2 * 3.6:.2f}")
elif G_total_water_2>=upper_bound1:
    TPower_2 = TPower_2 * 0.95
    print(f"Значение расхода ГЦН правой половины: {G_total_water_2 * 3.6:.2f} превышено Gном: {G_water_nominal2 * 3.6:.2f}")
else:
    TPower_2 = TPower_2 * 1.05
    print(f"Значение расхода ГЦН правой половины: {G_total_water_2 * 3.6:.2f} занижено Gном: {G_water_nominal2 * 3.6:.2f}")


# 1. Расчет давления на выходе из реактора (с учётом номинала)
p_out_reactor_1 = nominal_pressure * (G_total_water_1 / G_water_nominal1) * ((TPower_1 + 0.01)/3200e6)
T_out1 = 35.53483 * math.log(p_out_reactor_1/1e6) + 209.26655
T_out1 = max(T_out1,ambient_temp)
x_steam_1 = (TPower_1 * 4.767e-5) / 1e6 * 0.775 #Паросодержание, массовые доли (+ поправочный коэффициент)
p_out_reactor_2 = nominal_pressure * (G_total_water_2 / G_water_nominal2) * ((TPower_2 + 0.01)/3200e6)
T_out2 = 35.53483 * math.log(p_out_reactor_2/1e6) + 209.26655
T_out2 = max(T_out2,ambient_temp)
x_steam_2 = (TPower_2 * 4.767e-5) / 1e6 * 0.775 #Паросодержание, массовые доли (+ поправочный коэффициент)


# 2. Выход пароводяной смеси из реактора
rho_water_1, p_water1 = get_properties(T_out1, 'water')
rho_steam_1, p_steam1 = get_properties(T_out1, 'steam')
rho_mix_1 = (1 - x_steam_1) * rho_water_1 + x_steam_1 * rho_steam_1  # Плотность смеси
Q_mix_1 = G_total_water_1 / rho_mix_1  # Объемный расход смеси (м^3/с)
print(f"Температура ПВС-1 на выходе из реактора: {T_out1:.2f} °C")
print(f"Давление на выходе из реактора: {p_out_reactor_1 / 1e6:.2f} МПа")
rho_water_2, p_water2 = get_properties(T_out2, 'water')
rho_steam_2, p_steam2 = get_properties(T_out2, 'steam')
rho_mix_2 = (1 - x_steam_2) * rho_water_2 + x_steam_2 * rho_steam_2  # Плотность смеси
Q_mix_2 = G_total_water_2 / rho_mix_2  # Объемный расход смеси (м^3/с)
print(f"Температура ПВС-2 на выходе из реактора: {T_out2:.2f} °C")
print(f"Давление на выходе из реактора: {p_out_reactor_2 / 1e6:.2f} МПа")


# 3. Потери давления в трубах
v_mix1 = G_total_water_1 / rho_mix_1  # Скорость потока смеси (м/с)
L = 61  # Длина трубопровода (м)
D = 0.325  # Диаметр труб (м)
mu = 0.000183/(1 + 0.0337 * T_out1 + 0.000221 * T_out1**2) #Вязкость
Re = (rho_mix_1 * v_mix1 * D)/mu #Расчёт критерия Рейнольдса
#Расчёт коэффициента трения от критерия Рейнольдса
if Re==0:
    lambda_pipe = 0
elif Re<2300:
    lambda_pipe = 64/Re
elif Re>4000:
    lambda_pipe = 1/((-2*math.log10((0.01/(3.71 * D)) + (2.51/(Re * math.sqrt(mu)))))**2)
# Потери давления (добавить для цикла ДЭ-ПЭ-БС-ГЦН)
delta_p_pipe = lambda_pipe * (L / D) * (rho_mix_1 * v_mix1 ** 2) / 2
if delta_p_pipe>p_out_reactor_1:
    p_after_pipes1 = p_out_reactor_1
else:
    p_after_pipes1 = p_out_reactor_1 - delta_p_pipe  # Давление после труб
print(f"Давление смеси после труб: {p_after_pipes1 / 1e6:.2f} МПа")

v_mix2 = G_total_water_2 / rho_mix_2  # Скорость потока смеси (м/с)
L = 61  # Длина трубопровода (м)
D = 0.325  # Диаметр труб (м)
mu = 0.000183/(1 + 0.0337 * T_out2 + 0.000221 * T_out2**2) #Вязкость
Re = (rho_mix_2 * v_mix2 * D)/mu #Расчёт критерия Рейнольдса
#Расчёт коэффициента трения от критерия Рейнольдса
if Re==0:
    lambda_pipe = 0
elif Re<2300:
    lambda_pipe = 64/Re
elif Re>4000:
    lambda_pipe = 1/((-2*math.log10((0.01/(3.71 * D)) + (2.51/(Re * math.sqrt(mu)))))**2)
# Потери давления (добавить для цикла ДЭ-ПЭ-БС-ГЦН)
delta_p_pipe = lambda_pipe * (L / D) * (rho_mix_2 * v_mix2 ** 2) / 2
if delta_p_pipe>p_out_reactor_2:
    p_after_pipes2 = p_out_reactor_2
else:
    p_after_pipes2 = p_out_reactor_2 - delta_p_pipe  # Давление после труб
print(f"Давление смеси после труб: {p_after_pipes2 / 1e6:.2f} МПа")

# 4. Сепарация в барабан-сепараторе (давление принимаем равным после труб)
p_bs1 = p_after_pipes1
q_steam1 = x_steam_1 * G_total_water_1
# Проверка давления в барабан-сепараторе, оно не должно быть ниже номинального
#if p_bs < nominal_pressure:
#    print("qqq")
# Температура пара в барабан-сепараторе
T_steam1 = T_out1
print(f"Давление в барабане-сепараторе: {p_bs1 / 1e6:.2f} МПа")
print(f"Парообразование: {q_steam1:.2f} кг/с")
print(f"Температура пара в барабане-сепараторе: {T_steam1:.2f} °C")

p_bs2 = p_after_pipes2
q_steam2 = x_steam_2 * G_total_water_2
# Проверка давления в барабан-сепараторе, оно не должно быть ниже номинального
#if p_bs < nominal_pressure:
#    print("qqq")
# Температура пара в барабан-сепараторе
T_steam2 = T_out2
print(f"Давление в барабане-сепараторе: {p_bs2 / 1e6:.2f} МПа")
print(f"Парообразование: {q_steam2:.2f} кг/с")
print(f"Температура пара в барабане-сепараторе: {T_steam2:.2f} °C")

#Сепаратор-пароперегреватель (острый пар)
q_steam_SPP1 = 0.1 * q_steam1
q_steam1 = q_steam1 - q_steam_SPP1
print(f"Острый пар на СПП-1: {q_steam_SPP1:.2f} кг/с")
q_steam_SPP2 = 0.1 * q_steam2
q_steam2 = q_steam2 - q_steam_SPP2
print(f"Острый пар на СПП-2: {q_steam_SPP2:.2f} кг/с")


# 5. Поступление пара на ТГ
#ТГ-1
#Разгон ротора ТГ-1
DT = 14.87 #Просто пример, надо будет поменять
if RTG1 == True:
    v_rotor1 = alpha1 * DT
    #Частота ротора
    f1 = (v_rotor1*1)/60
else:
    pass
if RTG2 == True:
    v_rotor2 = alpha2 * DT
    #Частота ротора
    f2 = (v_rotor2*1)/60
else:
    pass
print(f"Обороты ротора ТГ-1:  {v_rotor1:.2f} об/мин")
print(f"Обороты ротора ТГ-2:  {v_rotor2:.2f} об/мин")
print(f"Частота ТГ-1:  {f1:.2f} Гц")
print(f"Частота ТГ-2:  {f2:.2f} Гц")

#ЦВД
A_steam_q_steam1_CVD = q_steam1 * 340000
A_steam_q_steam2_CVD = q_steam2 * 340000
#На перегрев в СПП-1
a1_steam_out_1 = 0.1 * q_steam1
#Для подогрев в деаэратор
a1_steam_out_2 = 0.05 * q_steam1
#На подогрев в ПНД-13,14
a1_steam_out_3 = 0.05 * q_steam1
a1_steam_out_4 = 0.05 * q_steam1
q_steam1 = q_steam1 - (a1_steam_out_1 + a1_steam_out_2 + a1_steam_out_3 + a1_steam_out_4)
#Pвыход ЦВД
P_CVD1 = 0.293 * p_bs1
T_CVD1 = 35.53483 * math.log(P_CVD1/1e6) + 209.26655

#На перегрев в СПП-2
a2_steam_out_1 = 0.1 * q_steam2
#Для подогрев в деаэратор
a2_steam_out_2 = 0.05 * q_steam2
#На подогрев в ПНД-23,24
a2_steam_out_3 = 0.05 * q_steam2
a2_steam_out_4 = 0.05 * q_steam2
q_steam2 = q_steam2 - (a2_steam_out_1 + a2_steam_out_2 + a2_steam_out_3 + a2_steam_out_4)
#Pвыход ЦВД
P_CVD2 = 0.293 * p_bs2
T_CVD2 = 35.53483 * math.log(P_CVD2/1e6) + 209.26655

#Вибрация подшипников
# Параметры турбины К-500-65/3000
m = 190000  # масса ротора, кг
k1 = 1e8*(1 - 210e-06*(T_CVD1 - 20)) # жёсткость системы, Н/м ТГ-1
k2 = 1e8*(1 - 210e-06*(T_CVD1 - 20)) # жёсткость системы, Н/м ТГ-2
c01 = 1e4*(1 - 0.05*(T_CVD1 - 20))*(1 + 1e-06*(P_CVD1 - nominal_pressure)) # начальный коэффициент демпфирования, Н/(м/с) ТГ-1
c02 = 1e4*(1 - 0.05*(T_CVD1 - 20))*(1 + 1e-06*(P_CVD1 - nominal_pressure)) # начальный коэффициент демпфирования, Н/(м/с) ТГ-2
c11 = 1e3*(1 - 0.001*(T_CVD1 - 20)) # нелинейный коэффициент демпфирования, Н/(м/с)^(n) ТГ-1
c12 = 1e3*(1 - 0.001*(T_CVD1 - 20)) # нелинейный коэффициент демпфирования, Н/(м/с)^(n) ТГ-2
if v_rotor1<1500:
    n = 2      # степень нелинейности
else:
    n = 3
F01 = 2.5e3*(1 + 0.001*(T_CVD1 - 20))*(1 + 0.95*(q_steam1/800)) # амплитуда внешней возмущающей силы, Н ТГ-1
F02 = 2.5e3*(1 + 0.001*(T_CVD1 - 20))*(1 + 0.95*(q_steam1/800)) # амплитуда внешней возмущающей силы, Н ТГ-2
omega_exc1 = 2 * math.pi * 50  # частота возмущающей силы, рад/с ТГ-1
omega_res1 = (k1/m)**(1/2)  # синхронная частота вращения ротора, рад/с ТГ-2
omega_exc2 = 2 * math.pi * 50  # частота возмущающей силы, рад/с ТГ-1
omega_res2 = (k2/m)**(1/2)  # синхронная частота вращения ротора, рад/с ТГ-2
# Дополнительные параметры
alpha_resonance1 = 1.5*(1 + 0.001*(T_CVD1 - 20))*(1 + 1e-07*(P_CVD1 - nominal_pressure))*(1 + 0.001*(q_steam1 - 800))    # усиление при приближении к резонансу ТГ-1
alpha_resonance2 = 1.5*(1 + 0.001*(T_CVD2 - 20))*(1 + 1e-07*(P_CVD2 - nominal_pressure))*(1 + 0.001*(q_steam2 - 800))    # усиление при приближении к резонансу ТГ-2
beta_turbulence1 = 1.1*(1 + 0.001*(T_CVD1 - 20))*(1 + 0.001*(q_steam1 - 800))    # коэффициент для учета турбулентности ТГ-1
beta_turbulence2 = 1.1*(1 + 0.001*(T_CVD2 - 20))*(1 + 0.001*(q_steam2 - 800))    # коэффициент для учета турбулентности ТГ-2
gamma_temp1 = 0.001*(1 + 0.001*(T_CVD1 - 20))       # температурный коэффициент для жесткости и демпфирования ТГ-1
gamma_temp2 = 0.001*(1 + 0.001*(T_CVD2 - 20))       # температурный коэффициент для жесткости и демпфирования ТГ-2
delta_lubrication1 = 0.7*(1 + 0.001*(T_CVD1 - 20))*(1 + 1e-07*(P_CVD1 - nominal_pressure))  # коэффициент ухудшения смазки ТГ-1
delta_lubrication2 = 0.7*(1 + 0.001*(T_CVD2 - 20))*(1 + 1e-07*(P_CVD2 - nominal_pressure))  # коэффициент ухудшения смазки ТГ-2
A_aero1 = 0.05*(1 + 0.01*(T_CVD1 - 20))*(1 + 1e-07*(P_CVD1 - nominal_pressure))*(1 + 0.001*(q_steam1 - 800))            # коэффициент для моделирования аэродинамических и гидродинамических сил ТГ-1
A_aero2 = 0.05*(1 + 0.01*(T_CVD2 - 20))*(1 + 1e-07*(P_CVD2 - nominal_pressure))*(1 + 0.001*(q_steam2 - 800))            # коэффициент для моделирования аэродинамических и гидродинамических сил ТГ-2
# Функция резонансного усиления
resonance_amplification1 = 1 + alpha_resonance1 * math.exp(-((omega_exc1 - omega_res1) / 10) ** 2)
resonance_amplification2 = 1 + alpha_resonance2 * math.exp(-((omega_exc2 - omega_res2) / 10) ** 2)
# Учет температурного эффекта на жесткость и демпфирование
temperature_effect1 = 1 + gamma_temp1 * T_CVD1
temperature_effect2 = 1 + gamma_temp2 * T_CVD2
# Дифференциальные уравнения для системы
# Дифференциальные уравнения для системы
def bearing_vibration(t, y, c0, c1, F0, k, delta_lubrication, temperature_effect, beta_turbulence, omega_exc, resonance_amplification, A_aero):
    x, x_dot = y
    # Модификация коэффициентов
    damping = (c0 + c1 * abs(x) ** n) * delta_lubrication * temperature_effect * beta_turbulence
    stiffness = k * temperature_effect
    # Внешняя сила с учетом резонанса
    F_ext = F0 * math.cos(omega_exc * t) * resonance_amplification
    # Аэродинамическая сила
    F_aero = A_aero * x_dot
    # Уравнение движения
    x_ddot = (F_ext + F_aero - damping * x_dot - stiffness * x) / m
    return [x_dot, x_ddot]
# Метод Рунге-Кутта 4-го порядка (RK4)
def runge_kutta_4(func, y0, t_eval, *args):
    y = np.zeros((len(t_eval), len(y0)))
    y[0] = y0
    dt = t_eval[1] - t_eval[0]
    for i in range(1, len(t_eval)):
        k1 = np.array(func(t_eval[i-1], y[i-1], *args)) * dt
        k2 = np.array(func(t_eval[i-1] + 0.5 * dt, y[i-1] + 0.5 * k1, *args)) * dt
        k3 = np.array(func(t_eval[i-1] + 0.5 * dt, y[i-1] + 0.5 * k2, *args)) * dt
        k4 = np.array(func(t_eval[i-1] + dt, y[i-1] + k3, *args)) * dt
        y[i] = y[i-1] + (k1 + 2*k2 + 2*k3 + k4) / 6
    return y
# Начальные условия
x0 = 0.005  # начальное смещение (м)
x_dot0 = 0.0  # начальная скорость (м/с)
y0 = [x0, x_dot0]
# Время моделирования
DT = 20  # примерное время моделирования
t_eval = np.linspace(0, DT, 1000)
# Решение системы с методом Рунге-Кутта 4-го порядка
sol1 = runge_kutta_4(bearing_vibration, y0, t_eval, c01, c11, F01, k1, delta_lubrication1, temperature_effect1, beta_turbulence1, omega_exc1, resonance_amplification1, A_aero1)
sol2 = runge_kutta_4(bearing_vibration, y0, t_eval, c02, c12, F02, k2, delta_lubrication2, temperature_effect2, beta_turbulence2, omega_exc2, resonance_amplification2, A_aero2)
# Получение результатов из sol1 и sol2
# Вычисления с использованием Рунге-Кутта
time = t_eval  # Время
displacement1 = sol1[:, 0]  # Смещение для первого набора параметров
velocity1 = sol1[:, 1]  # Скорость для первого набора параметров
displacement2 = sol2[:, 0]  # Смещение для второго набора параметров
velocity2 = sol2[:, 1]  # Скорость для второго набора параметров
# Вывод результатов для каждого целого времени
for t, d1, v1, d2, v2 in zip(time, displacement1, velocity1, displacement2, velocity2):
    if float(t).is_integer():  # Проверка, если t целое число (например, 1.0, 2.0 и т.д.)
        print(f"Время: {t:.2f} с, Смещение 1: {d1:.4f} м, Скорость 1: {v1:.4f} м/с, Смещение 2: {d2:.4f} м, Скорость 2: {v2:.4f} м/с")
# Графики результатов для тестов (очень красиво :З)
# График смещения
plt.subplot(2, 1, 1)  # 2 строки, 1 колонка, график 1
plt.plot(t_eval, sol1[:, 0], label='Смещение x(t)')
plt.xlabel('Время (с)')
plt.ylabel('Смещение (м)')
plt.legend()
plt.grid()
# График скорости
plt.subplot(2, 1, 2)  # 2 строки, 1 колонка, график 2
plt.plot(t_eval, sol1[:, 1], label='Скорость x\'(t)', color='orange')
plt.xlabel('Время (с)')
plt.ylabel('Скорость (м/с)')
plt.legend()
plt.grid()
plt.tight_layout()  # Для улучшения размещения графиков
plt.show()

#Сепаратор-пароперегреватель-1 (перегрев пара с ЦВД)
q_steam_SPP1_total = q_steam_SPP1 + a1_steam_out_1
#На деаэратор
q_mix_SPP1_1 = 2/3 * q_steam_SPP1_total
#На ПНД-3
q_mix_SPP1_2 = q_steam_SPP1_total - q_mix_SPP1_1
print(f"Расход пара через СПП-1: {q_steam_SPP1_total:.2f} кг/с")
#Сепаратор-пароперегреватель-2 (перегрев пара с ЦВД)
q_steam_SPP2_total = q_steam_SPP2 + a2_steam_out_1
#На деаэратор
q_mix_SPP2_1 = 2/3 * q_steam_SPP2_total
#На ПНД-3
q_mix_SPP2_2 = q_steam_SPP2_total - q_mix_SPP2_1
print(f"Расход пара через СПП-2: {q_steam_SPP2_total:.2f} кг/с")

#Pвыход ЦСД
P_CSD1 = 0.074 * p_bs1
T_CSD1 = 35.53483 * math.log(P_CSD1/1e6) + 209.26655
#Pвыход ЦСД
P_CSD2 = 0.074 * p_bs2
T_CSD2 = 35.53483 * math.log(P_CSD2/1e6) + 209.26655

#ЦНД
#На подогрев в ПНД-15,16,17
a1_steam_out_5 = 0.05 * q_steam1
a1_steam_out_6 = 0.05 * q_steam1
a1_steam_out_7 = 0.05 * q_steam1
q_steam1 = q_steam1 - (a1_steam_out_5 + a1_steam_out_6 + a1_steam_out_7)
#Pвыход ЦНД
P_CND1 = 0.0023 * p_bs1
T_CND1 = 35.53483 * math.log(P_CND1/1e6) + 209.26655
#ЦНД
#На подогрев в ПНД-25,26,27
a2_steam_out_5 = 0.05 * q_steam2
a2_steam_out_6 = 0.05 * q_steam2
a2_steam_out_7 = 0.05 * q_steam2
q_steam2 = q_steam2 - (a2_steam_out_5 + a2_steam_out_6 + a2_steam_out_7)
#Pвыход ЦНД
P_CND2 = 0.0023 * p_bs2
T_CND2 = 35.53483 * math.log(P_CND2/1e6) + 209.26655
A_steam_q_steam1_CND = q_steam1 * 575000
A_steam_q_steam2_CND = q_steam2 * 575000
A_total1 = A_steam_q_steam1_CVD + A_steam_q_steam1_CND
A_total2 = A_steam_q_steam2_CVD + A_steam_q_steam2_CND

if SK1_TG1 and SK2_TG1 and RTG1 == True:
    N_1 = 0.003*A_total1 + 6.88
    N_TG1 = (A_total1 - N_1)/1e6
else:
    N_TG1 = 0
if SK1_TG2 and SK2_TG2 and RTG2 == True:
    N_2 = 0.003*A_total2 + 6.88
    N_TG2 = (A_total2 - N_2)/1e6
else:
    N_TG2 = 0
print(f"Мощность ТГ-1:  {N_TG1:.2f}")
print(f"Мощность ТГ-2:  {N_TG2:.2f}")

# 6. Конденсация пара ТГ-1
#Подогреватели низкого давления
a1_q_PND_1 = a1_steam_out_7
a1_q_PND_2 = a1_steam_out_6
a1_q_PND_3 = a1_steam_out_5 + q_mix_SPP1_2
a1_q_PND_4 = a1_steam_out_4
a1_q_PND_5 = a1_steam_out_3
print(f"Расход ПНД-11 {a1_q_PND_1:.2f} кг/с")
print(f"Расход ПНД-12 {a1_q_PND_2:.2f} кг/с")
print(f"Расход ПНД-13 {a1_q_PND_3:.2f} кг/с")
print(f"Расход ПНД-14 {a1_q_PND_4:.2f} кг/с")
print(f"Расход ПНД-15 {a1_q_PND_5:.2f} кг/с")
#Подогреватели низкого давления
a2_q_PND_1 = a2_steam_out_7
a2_q_PND_2 = a2_steam_out_6
a2_q_PND_3 = a2_steam_out_5 + q_mix_SPP2_2
a2_q_PND_4 = a2_steam_out_4
a2_q_PND_5 = a2_steam_out_3
print(f"Расход ПНД-21 {a2_q_PND_1:.2f} кг/с")
print(f"Расход ПНД-22 {a2_q_PND_2:.2f} кг/с")
print(f"Расход ПНД-23 {a2_q_PND_3:.2f} кг/с")
print(f"Расход ПНД-24 {a2_q_PND_4:.2f} кг/с")
print(f"Расход ПНД-25 {a2_q_PND_5:.2f} кг/с")

#Расход на охладителе дренажа с ПНД
a1_q_OD = a1_q_PND_1 + a1_q_PND_2 + a1_q_PND_3 + a1_q_PND_4 + a1_q_PND_5
print(f"Расход ОД-1 {a1_q_OD:.2f} кг/с")
#Расход на охладителе дренажа с ПНД
a2_q_OD = a2_q_PND_1 + a2_q_PND_2 + a2_q_PND_3 + a2_q_PND_4 + a2_q_PND_5
print(f"Расход ОД-2 {a1_q_OD:.2f} кг/с")

T_cond1 = 0.121 * T_out1 # Температура на выходе из конденсатора
m_only_after_CND1 = q_steam1
m_cond1 = q_steam1 + a1_q_OD  # Масса сконденсированной воды
print(f"Масса воды после конденсата с ЦНД: {m_only_after_CND1:.2f} кг/с")
print(f"Масса воды перед КН11: {m_cond1:.2f} кг/с")
print(f"Температура конденсата: {T_cond1:.2f} °C")
T_cond2 = 0.121 * T_out2 # Температура на выходе из конденсатора
m_only_after_CND2 = q_steam2
m_cond2 = q_steam2 + a2_q_OD  # Масса сконденсированной воды
print(f"Масса воды после конденсата с ЦНД: {m_only_after_CND2:.2f} кг/с")
print(f"Масса воды перед КН21: {m_cond2:.2f} кг/с")
print(f"Температура конденсата: {T_cond2:.2f} °C")

#КН11
a1_q_KN1 = a1_q_KN2 = m_cond1
#Давление на выходе КН11
a1_p_KN1 = P_CND1 + a1_q_KN1 * 0.00419e6
print(f"Давление на выходе КН11: {a1_p_KN1/1e6:.2f} МПа")
#КН12
#Давление на выходе КН12
a1_p_KN2 = a1_p_KN1 + a1_q_KN2 * 0.00419e6
print(f"Давление на выходе КН12: {a1_p_KN2/1e6:.2f} МПа")
#КН21
a2_q_KN1 = a2_q_KN2 = m_cond2
#Давление на выходе КН21
a2_p_KN1 = P_CND2 + a2_q_KN1 * 0.00419e6
print(f"Давление на выходе КН21: {a2_p_KN1/1e6:.2f} МПа")
#КН22
#Давление на выходе КН2
a2_p_KN2 = a2_p_KN1 + a2_q_KN2 * 0.00419e6
print(f"Давление на выходе КН22: {a2_p_KN2/1e6:.2f} МПа")


#Потери давления в трубах от КН12 до ДЭ
a1_rho_water_KN2, a1_p_water1 = get_properties(T_cond1, 'water')
v_mix1 = a1_q_KN2 / a1_rho_water_KN2  # Скорость потока конденсата (м/с)
L = 61  # Длина трубопровода (м)
D = 0.325  # Диаметр труб (м)
mu = 0.000183/(1 + 0.0337 * T_cond1 + 0.000221 * T_cond1**2) #Вязкость
Re = (a1_rho_water_KN2 * v_mix1 * D)/mu #Расчёт критерия Рейнольдса
#Расчёт коэффициента трения от критерия Рейнольдса
if Re==0:
    lambda_pipe = 0
elif Re<2300:
    lambda_pipe = 64/Re
else:
    lambda_pipe = 1/((-2*math.log10((0.01/(3.71 * D)) + (2.51/(Re * math.sqrt(mu)))))**2)
delta_p_pipe = lambda_pipe * (L / D) * (a1_rho_water_KN2 * v_mix1 ** 2) / 2
if delta_p_pipe>a1_p_KN2:
    pass
else:
    a1_p_KN2 = a1_p_KN2 - delta_p_pipe  # Давление после труб
print(f"Давление смеси после КН12: {a1_p_KN2 / 1e6:.2f} МПа")
#Потери давления в трубах от КН22 до ДЭ
a2_rho_water_KN2, a2_p_water1 = get_properties(T_cond2, 'water')
v_mix2 = a2_q_KN2 / a2_rho_water_KN2  # Скорость потока конденсата (м/с)
L = 61  # Длина трубопровода (м)
D = 0.325  # Диаметр труб (м)
mu = 0.000183/(1 + 0.0337 * T_cond2 + 0.000221 * T_cond2**2) #Вязкость
Re = (a2_rho_water_KN2 * v_mix2 * D)/mu #Расчёт критерия Рейнольдса
#Расчёт коэффициента трения от критерия Рейнольдса
if Re==0:
    lambda_pipe = 0
elif Re<2300:
    lambda_pipe = 64/Re
else:
    lambda_pipe = 1/((-2*math.log10((0.01/(3.71 * D)) + (2.51/(Re * math.sqrt(mu)))))**2)
delta_p_pipe = lambda_pipe * (L / D) * (a2_rho_water_KN2 * v_mix2 ** 2) / 2
if delta_p_pipe>a2_p_KN2:
    pass
else:
    a2_p_KN2 = a2_p_KN2 - delta_p_pipe  # Давление после труб
print(f"Давление смеси после КН22: {a2_p_KN2 / 1e6:.2f} МПа")

#Нагрев ПНД
t11 = T_cond1
t12 = t11 * 1.162
t13 = t12 * 1.162
t14 = t13 * 1.162
t15 = t14 * 1.162
t16 = t15 * 1.162
t17 = t16 * 1.162
#Нагрев ПНД
t21 = T_cond2
t22 = t21 * 1.162
t23 = t22 * 1.162
t24 = t23 * 1.162
t25 = t24 * 1.162
t26 = t25 * 1.162
t27 = t26 * 1.162

#Деаэратор-1
q_water_deaerator1 = a1_q_KN2 + q_mix_SPP1_1 + a1_steam_out_2
p_deaerator1 = a1_p_KN2
T_water_before_deaerator1 = t17
print(f"Расход воды через деаэратор-1: {q_water_deaerator1:.2f} кг/c")
print(f"Температура воды на входе в деаэратор-1: {T_water_before_deaerator1:.2f} °C")
print(f"Давление в деаэраторе-2: {p_deaerator1/1e6:.2f} МПа")
#Деаэратор-2
q_water_deaerator2 = a2_q_KN2 + q_mix_SPP2_1 + a2_steam_out_2
p_deaerator2 = a2_p_KN2
T_water_before_deaerator2 = t27
print(f"Расход воды через деаэратор-2: {q_water_deaerator2:.2f} кг/c")
print(f"Температура воды на входе в деаэратор-2: {T_water_before_deaerator2:.2f} °C")
print(f"Давление в деаэраторе-2: {p_deaerator2/1e6:.2f} МПа")

#Питательные насосы
Q_water_PN = q_water_deaerator1 + q_water_deaerator2

if ZPN_1 and ZPN_2 and ZPN_3 and ZPN_4 and ZPN_5>0:
    #ПН-1
    m_PN1 = Q_water_PN/5 * ZPN_1
    if m_PN1>700:
        print('WARNING! Количество воды через ПЭН-1 на максимальном уровне!')
    #ПН-2
    m_PN2 = Q_water_PN/5 * ZPN_2
    if m_PN2>700:
        print('WARNING! Количество воды через ПЭН-2 на максимальном уровне!')
    #ПН-3
    m_PN3 = Q_water_PN/5 * ZPN_3
    if m_PN3>700:
        print('WARNING! Количество воды через ПЭН-3 на максимальном уровне!')
    #ПН-4
    m_PN4 = Q_water_PN/5 * ZPN_4
    if m_PN4>700:
        print('WARNING! Количество воды через ПЭН-4 на максимальном уровне!')
    #ПН-5
    m_PN5 = Q_water_PN/5 * ZPN_5
    if m_PN5>700:
        print('WARNING! Количество воды через ПЭН-5 на максимальном уровне!')
    m_PU_1 = (m_PN1 + m_PN2 + m_PN3 + m_PN4 + m_PN5)/2
    m_PU_2 = (m_PN1 + m_PN2 + m_PN3 + m_PN4 + m_PN5)/2
else:
    #ПН-1
    m_PN1 = Q_water_PN/4 * ZPN_1
    if m_PN1>700:
        print('WARNING! Количество воды через ПЭН-1 на максимальном уровне!')
    #ПН-2
    m_PN2 = Q_water_PN/4 * ZPN_2
    if m_PN2>700:
        print('WARNING! Количество воды через ПЭН-2 на максимальном уровне!')
    #ПН-3
    m_PN3 = Q_water_PN/4 * ZPN_3
    if m_PN3>700:
        print('WARNING! Количество воды через ПЭН-3 на максимальном уровне!')
    #ПН-4
    m_PN4 = Q_water_PN/4 * ZPN_4
    if m_PN4>700:
        print('WARNING! Количество воды через ПЭН-4 на максимальном уровне!')
    m_PU_1 = (m_PN1 + m_PN2 + m_PN3 + m_PN4)/2
    m_PU_2 = (m_PN1 + m_PN2 + m_PN3 + m_PN4)/2
    
#Питательный узел (ПУ-1)
if ZPU_11 and ZPU_12 and ZPU_13>0:
    m_water_nitka_PU_11 = m_PU_1/3 * ZPU_11
    if m_water_nitka_PU_11>500:
        print('WARNING! Количество воды через нитку 11 ПУ-1 на максимальном уровне!')
    m_water_nitka_PU_12 = m_PU_1/3 * ZPU_12
    if m_water_nitka_PU_12>500:
        print('WARNING! Количество воды через нитку 12 ПУ-1 на максимальном уровне!')
    m_water_nitka_PU_13 = m_PU_1/3 * ZPU_13
    if m_water_nitka_PU_13>500:
        print('WARNING! Количество воды через нитку 13 ПУ-1 на максимальном уровне!')
    m_feedwater_1 = m_water_nitka_PU_11 + m_water_nitka_PU_12 + m_water_nitka_PU_13
else:
    m_water_nitka_PU_11 = m_PU_1/2 * ZPU_11
    if m_water_nitka_PU_11>500:
        print('WARNING! Количество воды через нитку 11 ПУ-1 на максимальном уровне!')
    m_water_nitka_PU_12 = m_PU_1/2 * ZPU_12
    if m_water_nitka_PU_12>500:
        print('WARNING! Количество воды через нитку 12 ПУ-1 на максимальном уровне!')
    m_feedwater_1 = m_water_nitka_PU_11 + m_water_nitka_PU_12
#Питательный узел (ПУ-2)
if ZPU_21 and ZPU_22 and ZPU_23>0:
    m_water_nitka_PU_21 = m_PU_2/3 * ZPU_21
    if m_water_nitka_PU_21>500:
        print('WARNING! Количество воды через нитку 11 ПУ-2 на максимальном уровне!')
    m_water_nitka_PU_22 = m_PU_2/3 * ZPU_22
    if m_water_nitka_PU_22>500:
        print('WARNING! Количество воды через нитку 12 ПУ-2 на максимальном уровне!')
    m_water_nitka_PU_23 = m_PU_2/3 * ZPU_23
    if m_water_nitka_PU_23>500:
        print('WARNING! Количество воды через нитку 13 ПУ-2 на максимальном уровне!')
    m_feedwater_2 = m_water_nitka_PU_21 + m_water_nitka_PU_22 + m_water_nitka_PU_23
else:
    m_water_nitka_PU_21 = m_PU_2/2 * ZPU_21
    if m_water_nitka_PU_21>500:
        print('WARNING! Количество воды через нитку 11 ПУ-2 на максимальном уровне!')
    m_water_nitka_PU_22 = m_PU_2/2 * ZPU_22
    if m_water_nitka_PU_22>500:
        print('WARNING! Количество воды через нитку 12 ПУ-2 на максимальном уровне!')
    m_feedwater_2 = m_water_nitka_PU_21 + m_water_nitka_PU_22
    
#Потери давления в трубах от ПН-1 до БС-1
a1_rho_water_PN, a1_p_water1 = get_properties(T_water_before_deaerator1, 'water')
v_mix1 = m_feedwater_1 / a1_rho_water_PN  # Скорость потока конденсата (м/с)
L = 61  # Длина трубопровода (м)
D = 0.325  # Диаметр труб (м)
mu = 0.000183/(1 + 0.0337 * T_water_before_deaerator1 + 0.000221 * T_water_before_deaerator1**2) #Вязкость
Re = (a1_rho_water_PN * v_mix1 * D)/mu #Расчёт критерия Рейнольдса
#Расчёт коэффициента трения от критерия Рейнольдса
if Re==0:
    lambda_pipe = 0
elif Re<2300:
    lambda_pipe = 64/Re
else:
    lambda_pipe = 1/((-2*math.log10((0.01/(3.71 * D)) + (2.51/(Re * math.sqrt(mu)))))**2)
delta_p_pipe = lambda_pipe * (L / D) * (a1_rho_water_PN * v_mix1 ** 2) / 2
if delta_p_pipe>p_deaerator1:
    a1_P_after_PN = p_deaerator1
else:
    a1_P_after_PN = p_deaerator1 - delta_p_pipe  # Давление после труб
print(f"Давление смеси после ПН: {a1_P_after_PN / 1e6:.2f} МПа")
#Потери давления в трубах от ПН-2 до БС-2
a2_rho_water_PN, a2_p_water1 = get_properties(T_water_before_deaerator2, 'water')
v_mix2 = m_feedwater_2 / a2_rho_water_PN  # Скорость потока конденсата (м/с)
L = 61  # Длина трубопровода (м)
D = 0.325  # Диаметр труб (м)
mu = 0.000183/(1 + 0.0337 * T_water_before_deaerator2 + 0.000221 * T_water_before_deaerator2**2) #Вязкость
Re = (a2_rho_water_PN * v_mix2 * D)/mu #Расчёт критерия Рейнольдса
#Расчёт коэффициента трения от критерия Рейнольдса
if Re==0:
    lambda_pipe = 0
elif Re<2300:
    lambda_pipe = 64/Re
else:
    lambda_pipe = 1/((-2*math.log10((0.01/(3.71 * D)) + (2.51/(Re * math.sqrt(mu)))))**2)
delta_p_pipe = lambda_pipe * (L / D) * (a2_rho_water_PN * v_mix2 ** 2) / 2
if delta_p_pipe>p_deaerator2:
    a2_P_after_PN = p_deaerator2
else:
    a2_P_after_PN = p_deaerator2 - delta_p_pipe  # Давление после труб
print(f"Давление смеси после ПН: {a2_P_after_PN / 1e6:.2f} МПа")


#Возвращение питательной воды в БС-1
m_water_after_BS1 = G_total_water_1 * (1 - x_steam_1) + m_feedwater_1
T_feedwater_BS1 = 35.53483 * math.log(a1_P_after_PN/1e6) + 209.26655
#Возвращение питательной воды в БС-2
m_water_after_BS2 = G_total_water_2 * (1 - x_steam_2) + m_feedwater_2
T_feedwater_BS2 = 35.53483 * math.log(a2_P_after_PN/1e6) + 209.26655

#Потери давления в трубах от БС-1 до ГЦН-1
rho_water_GCN1, a1_p_water1 = get_properties(T_feedwater_BS1, 'water')
v_mix1 = m_water_after_BS1 / rho_water_GCN1  # Скорость потока конденсата (м/с)
L = 61  # Длина трубопровода (м)
D = 0.325  # Диаметр труб (м)
mu = 0.000183/(1 + 0.0337 * T_feedwater_BS1 + 0.000221 * T_feedwater_BS1**2) #Вязкость
Re = (rho_water_GCN1 * v_mix1 * D)/mu #Расчёт критерия Рейнольдса
#Расчёт коэффициента трения от критерия Рейнольдса
if Re==0:
    lambda_pipe = 0
elif Re<2300:
    lambda_pipe = 64/Re
else:
    lambda_pipe = 1/((-2*math.log10((0.01/(3.71 * D)) + (2.51/(Re * math.sqrt(mu)))))**2)
delta_p_pipe = lambda_pipe * (L / D) * (rho_water_GCN1 * v_mix1 ** 2) / 2
if delta_p_pipe>a1_P_after_PN:
    P_after_BS1 = a1_P_after_PN
else:
    P_after_BS1 = a1_P_after_PN - delta_p_pipe  # Давление после труб
print(f"Давление смеси после БС: {P_after_BS1 / 1e6:.2f} МПа")
# 7. Возвращение воды через ГЦН
P_after_GCN1 = p_out_reactor_2 * 1.057
T_in1 = 35.53483 * math.log(P_after_GCN1/1e6) + 209.26655 - 10
T_in1 = max(T_in1,ambient_temp)
print(f"Расход воды через ГЦН-1: {m_water_after_BS1 * 3.6:.2f} т/ч")
print(f"Температура воды на входе в реактора: {T_in1:.2f} °C")
print(f"Давление воды на входе в реактора: {P_after_GCN1/1e6:.2f} МПа")
#Потери давления в трубах от БС-2 до ГЦН-2
rho_water_GCN2, a2_p_water1 = get_properties(T_feedwater_BS2, 'water')
v_mix2 = m_water_after_BS2 / rho_water_GCN2  # Скорость потока конденсата (м/с)
L = 61  # Длина трубопровода (м)
D = 0.325  # Диаметр труб (м)
mu = 0.000183/(1 + 0.0337 * T_feedwater_BS2 + 0.000221 * T_feedwater_BS2**2) #Вязкость
Re = (rho_water_GCN2 * v_mix1 * D)/mu #Расчёт критерия Рейнольдса
#Расчёт коэффициента трения от критерия Рейнольдса
if Re==0:
    lambda_pipe = 0
elif Re<2300:
    lambda_pipe = 64/Re
else:
    lambda_pipe = 1/((-2*math.log10((0.01/(3.71 * D)) + (2.51/(Re * math.sqrt(mu)))))**2)
delta_p_pipe = lambda_pipe * (L / D) * (rho_water_GCN2 * v_mix2 ** 2) / 2
if delta_p_pipe>a2_P_after_PN:
    P_after_BS2 = a2_P_after_PN
else:
    P_after_BS2 = a2_P_after_PN - delta_p_pipe  # Давление после труб
print(f"Давление смеси после БС: {P_after_BS2 / 1e6:.2f} МПа")
# 7. Возвращение воды через ГЦН
P_after_GCN2 = p_out_reactor_2 * 1.057
T_in2 = 35.53483 * math.log(P_after_GCN2/1e6) + 209.26655 - 10
T_in2 = max(T_in2,ambient_temp)
print(f"Расход воды через ГЦН-2: {m_water_after_BS2 * 3.6:.2f} т/ч")
print(f"Температура воды на входе в реактора: {T_in2:.2f} °C")
print(f"Давление воды на входе в реактора: {P_after_GCN2/1e6:.2f} МПа")
