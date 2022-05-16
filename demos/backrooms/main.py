import raycaster

player = raycaster.Player(0, 0)
raycaster = raycaster.Raycaster("demos/backrooms/map.png", player, background="demos/backrooms/background.png")

raycaster.loadMap()
raycaster.run()