from pygame import *
from settings import *
from map import Map
from player import Player
from ghost import Ghost
from ui import UI
from menu import Menu
init()

screen = display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
display.set_caption("Pacman")

clock = time.Clock()

menu = Menu()
game_map = Map()
player = Player(start_x=1, start_y=1)
ui = UI()
START_PACMAN_POS = (1, 1)
START_GHOST_POS = [(16, 13), (17, 13), (18, 13), (19, 13)]


def reset_game():
    """Полный сброс карты и игрока для новой игры"""
    global game_map, player, ghosts
    game_map = Map()
    player = Player(start_x=START_PACMAN_POS[0], start_y=START_PACMAN_POS[1])
    ghosts = [
        Ghost(START_GHOST_POS[0][0], START_GHOST_POS[0][1], RED),
        Ghost(START_GHOST_POS[1][0], START_GHOST_POS[1][1], PINK),
        Ghost(START_GHOST_POS[2][0], START_GHOST_POS[2][1], CYAN),
        Ghost(START_GHOST_POS[3][0], START_GHOST_POS[3][1], ORANGE)
    ]
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
ghosts = []
reset_game()

# Текущее состояние программы: "MENU" или "GAME"
game_state = "MENU"

running = True
while running:
    for e in event.get():
        if e.type == QUIT:
            running = False

        if e.type == MOUSEBUTTONDOWN and e.button == 1:
            if game_state == "MENU":
                action = menu.handle_click(e.pos)
                if action == "PLAY":
                    reset_game()
                    game_state = "GAME"
                elif action == "QUIT":
                    running = False

        if e.type == KEYDOWN and e.key == K_ESCAPE:
            if game_state == "GAME":
                game_state = "MENU"

    # Отрисовка и логика в зависимости от состояния
    if game_state == "MENU":
        menu.draw(screen)

    elif game_state == "GAME":
        # Логика игры
        prev_score = player.score
        player.update(game_map)

        if player.score - prev_score == 50:
            for ghost in ghosts:
                ghost.make_scared(POWER_PELLET_TIME)

        for ghost in ghosts:
            ghost.update(game_map, player)

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
                        game_state = "MENU"
                    else:
                        reset_positions()

        # Отрисовка игры
        screen.fill(BLACK)
        game_map.draw(screen)
        player.draw(screen)
        for ghost in ghosts:
            ghost.draw(screen)
        ui.draw(screen, player.score, player.lives)

    display.flip()
    # Берем динамический FPS из меню настроек
    clock.tick(menu.current_fps)

quit()