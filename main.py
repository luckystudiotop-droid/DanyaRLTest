from pygame import *
from settings import *
from map import Map
from player import Player
from ghost import Ghost
from ui import UI
init()

screen = display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
display.set_caption("Pacman")

clock = time.Clock()

game_map = Map()
player = Player(start_x=1, start_y=1)
ui = UI()
START_PACMAN_POS = (1, 1)
START_GHOST_POS = [(16, 13), (17, 13), (18, 13), (19, 13)]

def reset_positions():
    """Сброс позиций Пакмана и призраков при потере жизни"""
    player.x = START_PACMAN_POS[0] * TILE_SIZE + TILE_SIZE // 2
    player.y = START_PACMAN_POS[1] * TILE_SIZE + TILE_SIZE // 2
    player.grid_x, player.grid_y = START_PACMAN_POS
    player.direction = (0, 0)
    player.next_direction = (0, 0)

    for i, ghost in enumerate(ghosts):
        ghost.x = START_GHOST_POS[i][0] * TILE_SIZE + TILE_SIZE // 2
        ghost.y = START_GHOST_POS[i][1] * TILE_SIZE + TILE_SIZE // 2
        ghost.grid_x, ghost.grid_y = START_GHOST_POS[i]
        ghost.is_scared = False
# Спавним 4 призрака в домике (по координатам сетки)
ghosts = [
    Ghost(16, 13, RED),
    Ghost(17, 13, PINK),
    Ghost(18, 13, CYAN),
    Ghost(19, 13, ORANGE)
]

running = True
while running:
    for e in event.get():
        if e.type == QUIT:
            running = False

    # Логика игрока
    prev_score = player.score
    player.update(game_map)

    # Режим испуга при съедании энергетика
    if player.score - prev_score == 50:
        for ghost in ghosts:
            ghost.make_scared(POWER_PELLET_TIME)

    # Логика и коллизии призраков
    for ghost in ghosts:
        # ПЕРЕДАЕМ player В МЕТОД update
        ghost.update(game_map, player)

        # Проверка столкновения
        if player.grid_x == ghost.grid_x and player.grid_y == ghost.grid_y:
            if ghost.is_scared:
                player.score += SCORE_GHOST
                ghost.is_scared = False
                ghost.x = 17 * TILE_SIZE + TILE_SIZE // 2
                ghost.y = 13 * TILE_SIZE + TILE_SIZE // 2
                ghost.grid_x, ghost.grid_y = 17, 13
            else:
                player.lives -= 1
                if player.lives <= 0:
                    print("Game Over! Score:", player.score)
                    running = False
                else:
                    reset_positions()

    # Отрисовка
    screen.fill(BLACK)
    game_map.draw(screen)
    player.draw(screen)
    for ghost in ghosts:
        ghost.draw(screen)

    # Отрисовываем UI
    ui.draw(screen, player.score, player.lives)

    display.flip()
    clock.tick(FPS)

quit()