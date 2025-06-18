for _,m in ipairs(workspace.devices.mnemo:GetDescendants()) do
	if m.Name == "Decal" then
		m.Transparency = 1
	end
	if m.Name == "Body1" then
		m.Material = Enum.Material.Metal
		m.MaterialVariant = "aluminum"
		m.Color = Color3.fromRGB(98, 97, 99)
	end
	if m.Name == "Body2" then
		m.Material = Enum.Material.Plastic
		m.MaterialVariant = "glossyplastic"
		m.Color = Color3.fromRGB(97, 107, 100)
	end
end