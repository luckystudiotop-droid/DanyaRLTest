import pygame
from settings import TILE_SIZE, WHITE, YELLOW, SCREEN_WIDTH, SCREEN_HEIGHT

class UI:
    def __init__(self):
        # Инициализация шрифта
        pygame.font.init()
        self.font = pygame.font.SysFont("arial", 18, bold=True)

    def draw_score(self, screen, score):
        """Отрисовка текущего счёта вверху слева"""
        text_surface = self.font.render(f"SCORE: {score}", True, WHITE)
        screen.blit(text_surface, (10, 5))

    def draw_lives(self, screen, lives):
        """Отрисовка жизней в виде иконок Пакмана вверху справа"""
        text_surface = self.font.render("LIVES:", True, WHITE)
        text_x = SCREEN_WIDTH - 120
        screen.blit(text_surface, (text_x, 5))

        # Рисуем кружочки-жизни правее текста
        radius = 8
        for i in range(lives):
            circle_x = text_x + 75 + (i * 18)
            circle_y = 14
            pygame.draw.circle(screen, YELLOW, (circle_x, circle_y), radius)

    def draw(self, screen, score, lives):
        self.draw_score(screen, score)
        self.draw_lives(screen, lives)