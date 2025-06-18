for _,m in ipairs(workspace:GetDescendants()) do
	pcall(function()
		if m.Hair.MeshId == "rbxassetid://9028722301" then
			m:Destroy()
		end
	end)
end

