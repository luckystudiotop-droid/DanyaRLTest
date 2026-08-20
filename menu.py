import pygame
from settings import SCREEN_WIDTH, SCREEN_HEIGHT, WHITE, YELLOW, BLUE, BLACK


class Menu:
    def __init__(self):
        pygame.font.init()
        self.title_font = pygame.font.SysFont("arial", 48, bold=True)
        self.button_font = pygame.font.SysFont("arial", 28, bold=True)

        # Состояние меню: "MAIN" или "SETTINGS"
        self.state = "MAIN"

        # Настройки по умолчанию
        self.volume = 50  # Громкость от 0 до 100
        self.fps_options = [30, 60, 90]
        self.fps_index = 1  # По умолчанию 60 FPS (индекс 1)

    @property
    def current_fps(self):
        return self.fps_options[self.fps_index]

    def draw_button(self, screen, text, rect, is_hovered):
        """Вспомогательная функция для отрисовки красивых кнопок"""
        color = YELLOW if is_hovered else BLUE
        text_color = BLACK if is_hovered else WHITE

        pygame.draw.rect(screen, color, rect, border_radius=8)
        pygame.draw.rect(screen, WHITE, rect, width=2, border_radius=8)

        text_surface = self.button_font.render(text, True, text_color)
        text_rect = text_surface.get_rect(center=rect.center)
        screen.blit(text_surface, text_rect)

    def draw_main_menu(self, screen, mouse_pos):
        # Заголовок
        title = self.title_font.render("PACMAN", True, YELLOW)
        title_rect = title.get_rect(center=(SCREEN_WIDTH // 2, 120))
        screen.blit(title, title_rect)

        # Прямоугольники кнопок
        play_rect = pygame.Rect(SCREEN_WIDTH // 2 - 120, 240, 240, 50)
        settings_rect = pygame.Rect(SCREEN_WIDTH // 2 - 120, 320, 240, 50)
        quit_rect = pygame.Rect(SCREEN_WIDTH // 2 - 120, 400, 240, 50)

        # Отрисовка кнопок
        self.draw_button(screen, "Грати", play_rect, play_rect.collidepoint(mouse_pos))
        self.draw_button(screen, "Налаштування", settings_rect, settings_rect.collidepoint(mouse_pos))
        self.draw_button(screen, "Вийти", quit_rect, quit_rect.collidepoint(mouse_pos))

        return play_rect, settings_rect, quit_rect

    def draw_settings(self, screen, mouse_pos):
        # Заголовок настроек
        title = self.title_font.render("НАЛАШТУВАННЯ", True, YELLOW)
        title_rect = title.get_rect(center=(SCREEN_WIDTH // 2, 100))
        screen.blit(title, title_rect)

        # Кнопки изменения громкости (-) и (+)
        vol_down_rect = pygame.Rect(SCREEN_WIDTH // 2 - 120, 200, 40, 40)
        vol_up_rect = pygame.Rect(SCREEN_WIDTH // 2 + 80, 200, 40, 40)

        # Текст громкости
        vol_text = self.button_font.render(f"Гучність: {self.volume}%", True, WHITE)
        screen.blit(vol_text, (SCREEN_WIDTH // 2 - 70, 205))

        self.draw_button(screen, "-", vol_down_rect, vol_down_rect.collidepoint(mouse_pos))
        self.draw_button(screen, "+", vol_up_rect, vol_up_rect.collidepoint(mouse_pos))

        # Кнопка смены FPS
        fps_rect = pygame.Rect(SCREEN_WIDTH // 2 - 120, 280, 240, 50)
        fps_text = f"FPS: {self.current_fps}"
        self.draw_button(screen, fps_text, fps_rect, fps_rect.collidepoint(mouse_pos))

        # Кнопка "Назад"
        back_rect = pygame.Rect(SCREEN_WIDTH // 2 - 120, 380, 240, 50)
        self.draw_button(screen, "Назад", back_rect, back_rect.collidepoint(mouse_pos))

        return vol_down_rect, vol_up_rect, fps_rect, back_rect

    def handle_click(self, mouse_pos):
        """Обработка кликов мыши в зависимости от открытого экрана"""
        if self.state == "MAIN":
            play_rect, settings_rect, quit_rect = self.draw_main_menu(pygame.display.get_surface(), mouse_pos)

            if play_rect.collidepoint(mouse_pos):
                return "PLAY"
            elif settings_rect.collidepoint(mouse_pos):
                self.state = "SETTINGS"
            elif quit_rect.collidepoint(mouse_pos):
                return "QUIT"

        elif self.state == "SETTINGS":
            vol_down, vol_up, fps_rect, back_rect = self.draw_settings(pygame.display.get_surface(), mouse_pos)

            if vol_down.collidepoint(mouse_pos):
                self.volume = max(0, self.volume - 10)
            elif vol_up.collidepoint(mouse_pos):
                self.volume = min(100, self.volume + 10)
            elif fps_rect.collidepoint(mouse_pos):
                # Переключение FPS по кругу (30 -> 60 -> 90 -> 30)
                self.fps_index = (self.fps_index + 1) % len(self.fps_options)
            elif back_rect.collidepoint(mouse_pos):
                self.state = "MAIN"

        return None

    def draw(self, screen):
        screen.fill(BLACK)
        mouse_pos = pygame.mouse.get_pos()

        if self.state == "MAIN":
            self.draw_main_menu(screen, mouse_pos)
        elif self.state == "SETTINGS":
            self.draw_settings(screen, mouse_pos)