import pygame
import random
from settings import (
    TILE_SIZE, RED, PINK, CYAN, ORANGE,
    SCARED_BLUE, GHOST_SPEED
)


class Ghost:
    def __init__(self, start_x, start_y, color=RED):
        self.grid_x = start_x
        self.grid_y = start_y

        self.x = start_x * TILE_SIZE + TILE_SIZE // 2
        self.y = start_y * TILE_SIZE + TILE_SIZE // 2

        self.color = color
        self.original_color = color

        self.direction = (0, -1)
        self.is_scared = False
        self.scared_timer = 0

    def get_possible_directions(self, game_map):
        """Возвращает список доступных направлений без прямого разворота на 180°"""
        possible = []
        directions = [(0, -1), (0, 1), (-1, 0), (1, 0)]
        opposite_dir = (-self.direction[0], -self.direction[1])

        for dx, dy in directions:
            next_x = self.grid_x + dx
            next_y = self.grid_y + dy

            if not game_map.is_wall(next_x, next_y):
                possible.append((dx, dy))

        if len(possible) > 1 and opposite_dir in possible:
            possible.remove(opposite_dir)

        return possible

    def get_target_tile(self, player):
        """Определяет целевую ячейку в зависимости от роли (цвета) призрака"""
        if self.color == RED:
            # Красный: целенаправленно преследует игрока
            return (player.grid_x, player.grid_y)

        elif self.color == PINK:
            # Розовый: целится на 4 ячейки перед Пакманом (засада)
            target_x = player.grid_x + player.direction[0] * 4
            target_y = player.grid_y + player.direction[1] * 4
            return (target_x, target_y)

        else:
            # Синий и Оранжевый: случайный выбор для хаотичности
            if random.random() < 0.5:
                return (player.grid_x, player.grid_y)
            else:
                return (random.randint(0, 35), random.randint(0, 27))

    def choose_best_direction(self, possible_dirs, target_tile, game_map):
        """Выбирает направление, приближающее (или отдаляющее) призрака к цели"""
        best_dir = possible_dirs[0]

        # Если испуган — ищем максимальное расстояние, если нет — минимальное
        best_distance = -1 if self.is_scared else float('inf')

        target_x, target_y = target_tile

        for dx, dy in possible_dirs:
            next_x = self.grid_x + dx
            next_y = self.grid_y + dy

            # Манхэттенское расстояние: |x1 - x2| + |y1 - y2|
            distance = abs(next_x - target_x) + abs(next_y - target_y)

            if self.is_scared:
                if distance > best_distance:
                    best_distance = distance
                    best_dir = (dx, dy)
            else:
                if distance < best_distance:
                    best_distance = distance
                    best_dir = (dx, dy)

        return best_dir

    def make_scared(self, duration_ms):
        self.is_scared = True
        self.scared_timer = pygame.time.get_ticks() + duration_ms

    def update(self, game_map, player):
        if self.is_scared and pygame.time.get_ticks() > self.scared_timer:
            self.is_scared = False

        center_x = self.grid_x * TILE_SIZE + TILE_SIZE // 2
        center_y = self.grid_y * TILE_SIZE + TILE_SIZE // 2

        # Выбор направления происходит в центре ячейки (на развилках)
        if abs(self.x - center_x) < GHOST_SPEED and abs(self.y - center_y) < GHOST_SPEED:
            possible_dirs = self.get_possible_directions(game_map)

            if possible_dirs:
                target_tile = (player.grid_x, player.grid_y) if self.is_scared else self.get_target_tile(player)
                self.direction = self.choose_best_direction(possible_dirs, target_tile, game_map)
                self.x, self.y = center_x, center_y
            else:
                self.direction = (0, 0)

        current_speed = GHOST_SPEED // 2 if self.is_scared else GHOST_SPEED

        self.x += self.direction[0] * current_speed
        self.y += self.direction[1] * current_speed

        self.grid_x = int(self.x // TILE_SIZE)
        self.grid_y = int(self.y // TILE_SIZE)

        # Обработка туннелей
        if self.grid_x < 0:
            self.x = (game_map.cols - 1) * TILE_SIZE + TILE_SIZE // 2
        elif self.grid_x >= game_map.cols:
            self.x = TILE_SIZE // 2

    def draw(self, screen):
        radius = TILE_SIZE // 2 - 2
        draw_color = SCARED_BLUE if self.is_scared else self.original_color
        pygame.draw.circle(screen, draw_color, (int(self.x), int(self.y)), radius)