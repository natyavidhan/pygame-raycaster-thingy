from raycaster import Raycaster, Player


raycaster = Raycaster("map.png")
player = Player(320, 320, raycaster)

raycaster.loadMap()
raycaster.run(player)