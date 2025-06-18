for _,i in ipairs(workspace.devices.ksp2:GetChildren()) do
	local is1 = (i.Body2.MeshId == "rbxassetid://18200780256")
	local img = ""
	pcall(function()
		img = i.Model.Body5.Decal.Texture
	end)
	local pivot = i:GetPivot()
	local tocpy = workspace.prefabs.ksp2
	if is1 then
		tocpy = workspace.prefabs.ksp2_1
	end
	local cpy = tocpy:Clone()
	cpy.Parent = workspace.devices.ksp2
	cpy:PivotTo(pivot)
	cpy.Model.Body5.Decal.Texture = img
	cpy.Name = i.Name
	i:Destroy()
end