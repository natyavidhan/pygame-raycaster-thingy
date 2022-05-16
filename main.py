from raycaster import Raycaster, Player


player = Player(320, 320)
raycaster = Raycaster("map2.png", player)

raycaster.loadMap()
raycaster.run()