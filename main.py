from raycaster import Raycaster, Player


player = Player(320, 320)
raycaster = Raycaster("map.png", player)

raycaster.loadMap()
raycaster.run()