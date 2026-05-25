from __future__ import annotations

import os
import pygame

from pirider.apps import AppEntry, get_available_apps


class GameCenter:
    def __init__(self) -> None:
        self.screen = None
        self.clock = None
        self.font = None
        self.running = True
        self.selected_index = 0
        self.apps = get_available_apps() + [AppEntry("Quit", self._quit)]
        self._init_display()

    def _init_display(self) -> None:
        pygame.init()
        pygame.display.set_caption("PiRider Game Center")
        flags = pygame.FULLSCREEN
        if os.environ.get("PIRIDER_WINDOWED") == "1":
            flags = 0
        self.screen = pygame.display.set_mode((0, 0), flags)
        self.clock = pygame.time.Clock()
        self.font = pygame.font.SysFont(None, 48)

    def _quit(self) -> None:
        self.running = False

    def run(self) -> None:
        while self.running:
            self._handle_events()
            self._render()
            self.clock.tick(60)
        pygame.quit()

    def _handle_events(self) -> None:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.running = False
                elif event.key == pygame.K_UP:
                    self.selected_index = (self.selected_index - 1) % len(self.apps)
                elif event.key == pygame.K_DOWN:
                    self.selected_index = (self.selected_index + 1) % len(self.apps)
                elif event.key in (pygame.K_RETURN, pygame.K_KP_ENTER, pygame.K_SPACE):
                    self.apps[self.selected_index].launch()
            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                self._click_menu(event.pos)

    def _click_menu(self, pos: tuple[int, int]) -> None:
        width, height = self.screen.get_size()
        start_y = height // 4
        spacing = 80
        for index, app in enumerate(self.apps):
            text_surface = self.font.render(app.name, True, (255, 255, 255))
            text_rect = text_surface.get_rect(center=(width // 2, start_y + index * spacing))
            if text_rect.collidepoint(pos):
                self.selected_index = index
                app.launch()
                break

    def _render(self) -> None:
        width, height = self.screen.get_size()
        self.screen.fill((15, 18, 40))

        title = self.font.render("PiRider Game Center", True, (255, 215, 120))
        title_rect = title.get_rect(center=(width // 2, height // 8))
        self.screen.blit(title, title_rect)

        for index, app in enumerate(self.apps):
            color = (200, 230, 255) if index == self.selected_index else (140, 160, 190)
            text = self.font.render(app.name, True, color)
            text_rect = text.get_rect(center=(width // 2, height // 4 + index * 80))
            self.screen.blit(text, text_rect)

        hint = pygame.font.SysFont(None, 28).render("Use Arrow keys or click. Enter to launch.", True, (180, 180, 180))
        hint_rect = hint.get_rect(center=(width // 2, height - 60))
        self.screen.blit(hint, hint_rect)

        pygame.display.flip()


if __name__ == "__main__":
    GameCenter().run()
