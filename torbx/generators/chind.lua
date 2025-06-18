for _,i in ipairs(workspace:GetDescendants())  do
	if i:IsA("MeshPart") then
		if i.MeshId == "rbxassetid://18720886059" then
			local nc = workspace.prefabs.newmtkind.Body1:Clone()
			nc.Parent = i.Parent
			nc.Material = i.Material
			nc.MaterialVariant = i.MaterialVariant
			pcall(function()
				i.SurfaceGui.Parent = nc
			end)
			pcall(function()
				i.l.Parent = nc
			end)
			nc.Size = i.Size
			nc.CFrame = i.CFrame
			nc.Color = i.Color
			i:Destroy()
		end
	end
end