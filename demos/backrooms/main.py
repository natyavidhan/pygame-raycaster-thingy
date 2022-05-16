import raycaster

player = raycaster.Player(0, 0)
raycaster = raycaster.Raycaster((1200, 700), "demos/backrooms/map.png", player, background="demos/backrooms/background.png")
raycaster.casted_rays = 120
raycaster.loadMap()
raycaster.run()