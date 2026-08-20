from pygame import *
from settings import *
from map import Map

init()


screen = display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
display.set_caption("Pacman")

clock = time.Clock()
game_map = Map()
running = True
while running:
    for e in event.get():
        if e.type == QUIT:
            running = False

    screen.fill(BLACK)
    game_map.draw(screen)


    display.flip()

    clock.tick(FPS)


quit()