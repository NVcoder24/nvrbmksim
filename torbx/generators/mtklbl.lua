function dofunny(p:Folder)
	for _,i in ipairs(p:GetDescendants()) do
		if i.Name == "Part" then
			local cpy = workspace.prefabs.mtklbl:Clone()
			cpy.Parent = i
			cpy.ImageLabel.Image = i.Texture.Texture
			cpy.ImageLabel.ImageColor3 = i.Texture.Color3
			i.Texture:Destroy()
		end
	end
end

dofunny(workspace.devices.lplace.p1)
dofunny(workspace.devices.lplace.p2)
dofunny(workspace.devices.lplace.p7)
dofunny(workspace.devices.lplace.p8)