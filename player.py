import pygame
from settings import TILE_SIZE, YELLOW, PACMAN_SPEED, DOT, POWER_PELLET


class Player:
    def __init__(self, start_x, start_y):
        # Стартовые позиции в сетке (grid coordinates)
        self.grid_x = start_x
        self.grid_y = start_y

        # Пиксельные координаты (центр ячейки)
        self.x = start_x * TILE_SIZE + TILE_SIZE // 2
        self.y = start_y * TILE_SIZE + TILE_SIZE // 2

        # Текущее движение: (dx, dy)
        self.direction = (0, 0)
        # Запланированное направление (буфер для плавной смены вектора)
        self.next_direction = (0, 0)

        self.score = 0

        self.lives = 3

    def handle_input(self):
        """Считывание нажатий клавиш"""
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT] or keys[pygame.K_a]:
            self.next_direction = (-1, 0)
        elif keys[pygame.K_RIGHT] or keys[pygame.K_d]:
            self.next_direction = (1, 0)
        elif keys[pygame.K_UP] or keys[pygame.K_w]:
            self.next_direction = (0, -1)
        elif keys[pygame.K_DOWN] or keys[pygame.K_s]:
            self.next_direction = (0, 1)

    def can_move(self, direction, game_map):
        """Проверка, свободна ли следующая ячейка от стены"""
        dx, dy = direction
        next_grid_x = self.grid_x + dx
        next_grid_y = self.grid_y + dy
        return not game_map.is_wall(next_grid_x, next_grid_y)

    def update(self, game_map):
        self.handle_input()

        # Находим текущий центр ячейки
        center_x = self.grid_x * TILE_SIZE + TILE_SIZE // 2
        center_y = self.grid_y * TILE_SIZE + TILE_SIZE // 2

        # Пакман меняет направление только когда он близко к центру ячейки
        if abs(self.x - center_x) < PACMAN_SPEED and abs(self.y - center_y) < PACMAN_SPEED:
            # Если можно повернуть в запланированную сторону — поворачиваем
            if self.next_direction != (0, 0) and self.can_move(self.next_direction, game_map):
                self.direction = self.next_direction
                self.x, self.y = center_x, center_y  # Ровняем точно по центру

            # Если в текущем направлении стена — останавливаемся
            if not self.can_move(self.direction, game_map):
                self.direction = (0, 0)
                self.x, self.y = center_x, center_y

        # Движение
        self.x += self.direction[0] * PACMAN_SPEED
        self.y += self.direction[1] * PACMAN_SPEED

        # Обновление координат сетки
        self.grid_x = int(self.x // TILE_SIZE)
        self.grid_y = int(self.y // TILE_SIZE)

        # Телепортация через боковые туннели
        if self.grid_x < 0:
            self.x = (game_map.cols - 1) * TILE_SIZE + TILE_SIZE // 2
        elif self.grid_x >= game_map.cols:
            self.x = TILE_SIZE // 2

        # Поедание точек
        eaten = game_map.eat_dot(self.grid_x, self.grid_y)
        if eaten == DOT:
            self.score += 10
        elif eaten == POWER_PELLET:
            self.score += 50

    def draw(self, screen):
        """Отрисовка Пакмана (пока что просто жёлтый круг)"""
        radius = TILE_SIZE // 2 - 2
        pygame.draw.circle(screen, YELLOW, (int(self.x), int(self.y)), radius)