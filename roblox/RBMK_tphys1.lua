local TweenService = game:GetService("TweenService")

local BASE_NEUTR = 1
local NEUTR_MUL = 1

local lvl_h = {0.5, 1.5, 2.5, 3.5, 4.5, 5.5, 6.5}
local lvl_bottoms = {0.0, 1.0, 2.0, 3.0, 4.0, 5.0, 6.0}
local lvl_tops = {1.0, 2.0, 3.0, 4.0, 5.0, 6.0, 7.0}

local waterlvl = 0
local neutr = 0

local shitnumber  = 33205451668000 * 3200

local amb_temp = 11

local ch_all_num = 1677
local ch_1_num = 835
local ch_2_num = 842

local az_ch_V = 0.039792438
local az_graf_V = 0.356856353

local c_graf = 709
local graf_nom_t = 650
local m_graf = 2230 * az_graf_V

local nom_water_x = 0.88

local rem_Q = 160 * 1000000 / ch_all_num

local nom_output = 13055.556 -- пароводяная смесь (кг/c)
local ch_nom_output = nom_output / 1677

local nom_pressure = 7.53 -- номинальное давление в МПа

function tablesum(tbl)
	local s = 0
	for i=1,#tbl do
		s += tbl[i]
	end
	return s
end

function tablesum7(tbl)
	return tbl[1]+tbl[2]+tbl[3]+tbl[4]+tbl[5]+tbl[6]+tbl[7]
end

local demo_neutr = shitnumber * 3200 / ch_all_num / 7

local last_time = time()
function simtick()
	local old_neutr = _G.rbmkdata.neutr
	
	local dbgnum = 0
	
	local neutr_h = {0,0,0,0,0,0,0}
	
	-- make a RBMK-1000 simulation tick
	local DT = time() - last_time
	last_time = time()
	local new_neutr = 0
	
	local wateradd_1 = workspace.RBMKSIM.kmpcdata.kmpc_out.M_water_1.Value / ch_1_num * DT
	local wateradd_2 = workspace.RBMKSIM.kmpcdata.kmpc_out.M_water_2.Value / ch_2_num * DT
	
	local loop1_power = 0
	local loop2_power = 0
	
	local loop1_g_sum = 0
	local loop1_water_x_sum = 0
	local loop1_temp_sum = 0
	local loop1_pressure_sum = 0
	local loop1_div = 0
	
	local loop2_g_sum = 0
	local loop2_water_x_sum = 0
	local loop2_temp_sum = 0
	local loop2_pressure_sum = 0
	local loop2_div = 0

	for rodi = 1, #_G.rbmkdata.fuel do
		local x = _G.rbmkdata.fuel[rodi][1] + 1
		local y = _G.rbmkdata.fuel[rodi][2] + 1
		
		local wateradd = wateradd_2
		local waterinT = workspace.RBMKSIM.kmpcdata.kmpc_out.T_in_2.Value
		if x < 25 then
			wateradd = wateradd_1
			waterinT = workspace.RBMKSIM.kmpcdata.kmpc_out.T_in_1.Value
		end
		
		-- новая температура и масса воды (shocked)
		_G.rbmkdata.reactor[y][x]["T_water"] = (_G.rbmkdata.reactor[y][x]["T_water"] * _G.rbmkdata.reactor[y][x]["M_water"] +
						wateradd * waterinT) /
						(_G.rbmkdata.reactor[y][x]["M_water"] + wateradd)
		_G.rbmkdata.reactor[y][x]["M_water"] = _G.rbmkdata.reactor[y][x]["M_water"] + wateradd
		
		local MWt = tablesum7(_G.rbmkdata.neutr[y][x]) / shitnumber
		
		-- нормис номинал давление 75,3 кгс/см2 = 7,53 мпа
		local water_q = 1000 + 100 * (_G.rbmkdata.reactor[y][x]["pressure"] / nom_pressure)
		local water_c = 4200 + 200 * (_G.rbmkdata.reactor[y][x]["pressure"] / nom_pressure)
		local water_L = 2300000 + 500000 * (_G.rbmkdata.reactor[y][x]["pressure"] / nom_pressure)
		local water_lvl = _G.rbmkdata.reactor[y][x]["M_water"] / water_q / az_ch_V * 7
		
		local gall = 0
		
		for lvl = 1, 7 do
			local Kcoef = 1
			local block_coefs = {}
			local sum_div = 0
			
			local water_infl = math.max(math.min(water_lvl - (lvl - 1), 1), 0)
			
			for infli = 1, #_G.rbmkdata.reactor[y][x]["infl"] do
				local infl = _G.rbmkdata.reactor[y][x]["infl"][infli]
				local rod = _G.rbmkdata.reactor[infl[2] + 1][infl[1] + 1]
				local i = infl[3]
				sum_div = sum_div + i
				
				local rod_bottom_out = rod["bottom_pos"]
				local rod_top_out = rod["bottom_pos"] + rod["block_len"]
				if rod["bottom_pos"] > 1 then
					dbgnum += 1
				end
				if rod_bottom_out < lvl_bottoms[lvl] and rod_top_out > lvl_tops[lvl] then
					table.insert(block_coefs, 1 * i)
				elseif rod_bottom_out > lvl_tops[lvl] or rod_top_out < lvl_bottoms[lvl] then
					table.insert(block_coefs, 0)
				elseif  lvl_bottoms[lvl] < rod_top_out and rod_top_out < lvl_tops[lvl] then
					table.insert(block_coefs, (rod_top_out - lvl_bottoms[lvl]) / 1 * i)
				else
					table.insert(block_coefs, (lvl_tops[lvl] - rod_bottom_out) / 1 * i)
				end
			end
			local rod_block_coef = tablesum(block_coefs) / sum_div

			if workspace.RBMKSIM.REACTORDEMO.Value then
				Kcoef = 1

				_G.rbmkdata.reactor[y][x]["k"][lvl] = Kcoef

				_G.rbmkdata.neutr[y][x][lvl] = demo_neutr

				new_neutr = new_neutr + _G.rbmkdata.neutr[y][x][lvl]
				neutr_h[lvl] = neutr_h[lvl] + _G.rbmkdata.neutr[y][x][lvl]
			else
				Kcoef = 1 + .1 - rod_block_coef * .4 - water_infl * .05 * (water_q / 1100)

				_G.rbmkdata.reactor[y][x]["k"][lvl] = Kcoef

				_G.rbmkdata.neutr[y][x][lvl] = _G.rbmkdata.neutr[y][x][lvl] + (_G.rbmkdata.neutr[y][x][lvl] + BASE_NEUTR) * (Kcoef - 1) * NEUTR_MUL * DT
				if _G.rbmkdata.neutr[y][x][lvl] < 0 then
					_G.rbmkdata.neutr[y][x][lvl] = 0
				end

				new_neutr = new_neutr + _G.rbmkdata.neutr[y][x][lvl]
				neutr_h[lvl] = neutr_h[lvl] + _G.rbmkdata.neutr[y][x][lvl]
			end
		end
		
		-- тепловуха
		local MWt = tablesum7(_G.rbmkdata.neutr[y][x]) / shitnumber
		
		local power1_water = MWt * 1000000 * 2/3
		local power1_graf = MWt * 1000000 * 1/3
		
		local boiling_temp = 100 + 184.5 * (_G.rbmkdata.reactor[y][x]["pressure"] / nom_pressure)
		
		-- потери
		local Q_loss_water = rem_Q / 2
		local Q_loss_graf = rem_Q / 2
		
		_G.rbmkdata.reactor[y][x]["T_water"] = _G.rbmkdata.reactor[y][x]["T_water"] - Q_loss_water / (water_c * _G.rbmkdata.reactor[y][x]["M_water"])
		_G.rbmkdata.reactor[y][x]["T_graf"] = _G.rbmkdata.reactor[y][x]["T_graf"] - Q_loss_water / (c_graf * m_graf)
		
		_G.rbmkdata.reactor[y][x]["T_water"] = math.max(amb_temp, _G.rbmkdata.reactor[y][x]["T_water"])
		_G.rbmkdata.reactor[y][x]["T_graf"] = math.max(amb_temp, _G.rbmkdata.reactor[y][x]["T_graf"])
		
		-- нагрев графита до T ном
		local Q_to_heat_graf_to_nom = math.max(0, (graf_nom_t - _G.rbmkdata.reactor[y][x]["T_graf"]) * c_graf * m_graf)
		local Q_heat_graf = math.min(power1_graf, Q_to_heat_graf_to_nom)
		power1_graf = power1_graf - Q_heat_graf
		_G.rbmkdata.reactor[y][x]["T_graf"] = _G.rbmkdata.reactor[y][x]["T_graf"] + Q_heat_graf / (c_graf * m_graf)
		
		-- передача теплоты воде от графита
		power1_water = power1_water + power1_graf
		
		-- нагрев воды до Т кипения
		local Q_to_heat_water_to_boil = math.max(0, (boiling_temp - _G.rbmkdata.reactor[y][x]["T_water"]) * water_c * _G.rbmkdata.reactor[y][x]["M_water"])
		local Q_to_water = math.min(Q_to_heat_water_to_boil, power1_water)
		_G.rbmkdata.reactor[y][x]["T_water"] = _G.rbmkdata.reactor[y][x]["T_water"] + Q_to_water / (water_c * _G.rbmkdata.reactor[y][x]["M_water"])
		_G.rbmkdata.reactor[y][x]["T_water"] = math.max(amb_temp, _G.rbmkdata.reactor[y][x]["T_water"])
		power1_water = power1_water - Q_to_water
		
		-- испарение воды
		local Q_to_evaporate_water = math.min(power1_water, water_L * _G.rbmkdata.reactor[y][x]["M_water"])
		_G.rbmkdata.reactor[y][x]["G_water"] = Q_to_evaporate_water / water_L
		_G.rbmkdata.reactor[y][x]["M_water"] = _G.rbmkdata.reactor[y][x]["M_water"] - _G.rbmkdata.reactor[y][x]["G_water"]
		power1_water = power1_water - power1_water
		_G.rbmkdata.reactor[y][x]["G_water"] = _G.rbmkdata.reactor[y][x]["G_water"] / DT
		
		-- новое давление
		_G.rbmkdata.reactor[y][x]["pressure"] = _G.rbmkdata.reactor[y][x]["G_water"] / ch_nom_output * nom_pressure
		
		-- передача энергии графиту от воды
		power1_graf = power1_graf + power1_water
		
		-- нагрев графита 2
		_G.rbmkdata.reactor[y][x]["T_graf"] = _G.rbmkdata.reactor[y][x]["T_graf"] + power1_graf / (c_graf * m_graf)
		
		-- выхлоп
		local ch_mix_output = _G.rbmkdata.reactor[y][x]["G_water"] / DT
		local ch_mix_temp = boiling_temp
		local ch_mix_pressure = _G.rbmkdata.reactor[y][x]["pressure"]
		local ch_mix_water_x = math.min(nom_water_x * (_G.rbmkdata.reactor[y][x]["G_water"] / ch_nom_output), .90)
		
		gall = gall + ch_mix_output
		
		--[[
		local loop1_g_sum = 0
	local loop1_water_x_sum = 0
	local loop1_temp_sum = 0
	local loop1_pressure_sum = 0
	local loop1_div = 0
		]]
		
		-- распределения
		if x < 25 then
			loop1_g_sum = loop1_g_sum + ch_mix_output
			loop1_water_x_sum = loop1_water_x_sum + ch_mix_water_x * ch_mix_output
			loop1_temp_sum = loop1_temp_sum + ch_mix_temp * ch_mix_output
			loop1_pressure_sum = loop1_pressure_sum + ch_mix_pressure
			loop1_div = loop1_div + ch_mix_output
			loop1_power = loop1_power + MWt
		else
			loop2_g_sum = loop2_g_sum + ch_mix_output
			loop2_water_x_sum = loop2_water_x_sum + ch_mix_water_x * ch_mix_output
			loop2_temp_sum = loop2_temp_sum + ch_mix_temp * ch_mix_output
			loop2_pressure_sum = loop2_pressure_sum + ch_mix_pressure
			loop2_div = loop2_div + ch_mix_output
			loop2_power = loop2_power + MWt
		end
	end
	
	loop1_pressure_sum = math.min(1, loop1_pressure_sum)
	loop2_pressure_sum = math.min(1, loop2_pressure_sum)
	
	local loop1_g = 0
	local loop1_water_x = 0
	local loop1_temp = amb_temp
	local loop1_pressure = 0
	
	if loop1_div > 0 then
		loop1_g = loop1_g_sum
		loop1_water_x = loop1_water_x_sum / loop1_div
		loop1_temp = loop1_temp_sum / loop1_div
		loop1_pressure = loop1_pressure_sum
	end
	
	local loop2_g = 0
	local loop2_water_x = 0
	local loop2_temp = amb_temp
	local loop2_pressure = 0
	
	if loop2_div > 0 then
		loop2_g = loop2_g_sum
		loop2_water_x = loop2_water_x_sum / loop2_div
		loop2_temp = loop2_temp_sum / loop2_div
		loop2_pressure = loop2_pressure_sum
	end
	
	workspace.RBMKSIM.kmpcdata.kmpc_in.M_mix_1.Value = loop1_g
	workspace.RBMKSIM.kmpcdata.kmpc_in.X_water_1.Value = loop1_water_x
	workspace.RBMKSIM.kmpcdata.kmpc_in.T_out_1.Value = loop1_temp
	workspace.RBMKSIM.kmpcdata.kmpc_in.P_out_reac_1.Value = loop1_pressure
	workspace.RBMKSIM.kmpcdata.kmpc_in.TPower1.Value = loop1_power
	
	workspace.RBMKSIM.kmpcdata.kmpc_in.M_mix_2.Value = loop2_g
	workspace.RBMKSIM.kmpcdata.kmpc_in.X_water_2.Value = loop2_water_x
	workspace.RBMKSIM.kmpcdata.kmpc_in.T_out_2.Value = loop2_temp
	workspace.RBMKSIM.kmpcdata.kmpc_in.P_out_reac_2.Value = loop2_pressure
	workspace.RBMKSIM.kmpcdata.kmpc_in.TPower2.Value = loop2_power
	
	new_neutr = math.floor(new_neutr)

	local K = 1 -- K за 1 такт
	if neutr > 0 then
		K = new_neutr / neutr
	end
	
	local Kpersec = math.pow(K, 1 / DT) -- K за 1 секунду
	
	local sfkre = new_neutr / shitnumber -- Тепловая мощность по палате
	
	neutr = new_neutr
	
	local R = (K - 1) / K -- Реактивность
	
	local period = 2.7 / (Kpersec - 1) -- За сколько секунд кол-во нейтронов увел. в e (экспонент прим. 2.7) раз
	if period < 0 then
		period = 1/0
	end
	
	local tweenInfo = TweenInfo.new(DT, Enum.EasingStyle.Quad, Enum.EasingDirection.InOut)
	
	workspace.reactdbg.SurfaceGui.N.Text = "N="..tostring(math.round(sfkre)).." МВт"
	workspace.reactdbg.SurfaceGui.K.Text = "K="..tostring(K)
	workspace.reactdbg.SurfaceGui.R.Text = "R="..tostring(R)
	workspace.reactdbg.SurfaceGui.DT.Text = "DT="..tostring(DT)
	workspace.reactdbg.SurfaceGui.DBG.Text = tostring(new_neutr) .. "\n" .. tostring(33205451668000 * 3200)
	
	TweenService:Create(workspace.RBMKSYS.viur.sfkre_m1830.sfkre_r.rel, tweenInfo, { Value = math.min(neutr / shitnumber / 4000, 1) }):Play()
	
	TweenService:Create(workspace.RBMKSYS.viur.sfkre_m1830.sfkre_h_1.rel, tweenInfo, { Value = math.min(neutr_h[7] / shitnumber / 4000 * 7, 1) }):Play()
	TweenService:Create(workspace.RBMKSYS.viur.sfkre_m1830.sfkre_h_2.rel, tweenInfo, { Value = math.min(neutr_h[6] / shitnumber / 4000 * 7, 1) }):Play()
	TweenService:Create(workspace.RBMKSYS.viur.sfkre_m1830.sfkre_h_3.rel, tweenInfo, { Value = math.min(neutr_h[5] / shitnumber / 4000 * 7, 1) }):Play()
	TweenService:Create(workspace.RBMKSYS.viur.sfkre_m1830.sfkre_h_4.rel, tweenInfo, { Value = math.min(neutr_h[4] / shitnumber / 4000 * 7, 1) }):Play()
	TweenService:Create(workspace.RBMKSYS.viur.sfkre_m1830.sfkre_h_5.rel, tweenInfo, { Value = math.min(neutr_h[3] / shitnumber / 4000 * 7, 1) }):Play()
	TweenService:Create(workspace.RBMKSYS.viur.sfkre_m1830.sfkre_h_6.rel, tweenInfo, { Value = math.min(neutr_h[2] / shitnumber / 4000 * 7, 1) }):Play()
	TweenService:Create(workspace.RBMKSYS.viur.sfkre_m1830.sfkre_h_7.rel, tweenInfo, { Value = math.min(neutr_h[1] / shitnumber / 4000 * 7, 1) }):Play()
	
	TweenService:Create(workspace.RBMKSYS.viur.pult_period.p3.rel, tweenInfo, { Value = math.max(math.min(17.485 * math.pow(period, -0.985), 1), 0) }):Play()
	TweenService:Create(workspace.RBMKSYS.viur.pult_period.p2.rel, tweenInfo, { Value = math.max(math.min(17.485 * math.pow(period, -0.985), 1), 0) }):Play()
	TweenService:Create(workspace.RBMKSYS.viur.pult_period.p1.rel, tweenInfo, { Value = math.max(math.min(17.485 * math.pow(period, -0.985), 1), 0) }):Play()

	
	script.Parent.values.rbmk_k.Value = K
	script.Parent.values.sfkre.Value = sfkre
	
	
	-- here
	local p = 0
	if neutr > 0 then
		p = (K - 1) / K
	else 
		workspace.reactdbg.SurfaceGui.R.Text = "R="..tostring(-1)
	end
	
	local l = 868
	local Beff = 0.00636
	local lam = 0.008
	
	
	local T = 0
	local Rel = 0
	if p > 0 then
		T = 2.7 / (math.pow(K, 1/DT) - 1)
		Rel = 17.485 * math.pow(T, -0.985)
		TweenService:Create(workspace.RBMKSYS.viur.pult_period.p3.rel, tweenInfo, { Value = math.min(Rel, 1) }):Play()
	else
		TweenService:Create(workspace.RBMKSYS.viur.pult_period.p3.rel, tweenInfo, { Value = 0 }):Play()
	end
	
	print(math.log10(sfkre))
		
	local lgm = 0
	local flg = 0
	local Bn = 2.862505 * 10^-16
	if neutr > 0 then
		lgm = math.log10(neutr * Bn) * 0.35
		flg = (lgm + 8) / 16
		print(flg)
		workspace.reactdbg.SurfaceGui.R.Text = "R="..tostring(lgm)
		--TweenService:Create(workspace.RBMKSYS.viur.pult_logM.p1.rel, tweenInfo, { Value = math.min(flg, 1) }):Play()
	else
		--TweenService:Create(workspace.RBMKSYS.viur.pult_logM.p1.rel, tweenInfo, { Value = 0 }):Play()
	end
end

while not script.Parent.rbmkdataloaded.Value do
	task.wait()
end

task.wait(1)

while true do
	simtick()
	task.wait(.5)
end
