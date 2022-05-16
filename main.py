from raycaster.raycaster import Raycaster, Player


player = Player(75, 75)
raycaster = Raycaster((1024, 576), "map.png", player)

raycaster.loadMap()
raycaster.run()