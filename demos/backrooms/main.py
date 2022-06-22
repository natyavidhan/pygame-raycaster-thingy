import raycaster

def person_handler(person):
    pass

player = raycaster.Player(0, 0)
person = raycaster.Entity(10, 10, "assets/person.png", person_handler)

raycaster = raycaster.Raycaster(
    (1200, 700),
    "assets/map.png",
    player,
    background="assets/background.png",
    entities=[person],
)


raycaster.loadMap()
raycaster.run()
