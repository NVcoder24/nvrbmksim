for _,i in ipairs(workspace:GetDescendants()) do
	local isbtn = false
	pcall(function()
		isbtn = i.Body1.MeshId == "rbxassetid://18202550731"
	end)
	if isbtn then
		pcall(function()
			i.button_unpressed:Destroy()
		end)
		pcall(function()
			i.button_pressed:Destroy()
		end)
		pcall(function()
			i.Script:Destroy()
		end)
		local ns1 = workspace.prefabs.kerem.ke011on:Clone()
		local ns2 = workspace.prefabs.kerem.ke011off:Clone()
		local ns3 = workspace.prefabs.kerem.Script:Clone()
		
		ns1.Parent = i
		ns2.Parent = i
		ns3.Parent = i
	end
end