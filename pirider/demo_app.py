from __future__ import annotations

import os
import pygame

from .config import FPS


class DemoApp:
    def __init__(self) -> None:
        pygame.init()
        pygame.display.set_caption("PiRider Demo App")
        flags = pygame.FULLSCREEN
        if os.environ.get("PIRIDER_WINDOWED") == "1":
            flags = 0

        self.screen = pygame.display.set_mode((0, 0), flags)
        self.clock = pygame.time.Clock()
        self.font = pygame.font.SysFont(None, 40)
        self.running = True
        self.ball_position = [150.0, 150.0]
        self.ball_velocity = [240.0, 180.0]
        self.ball_radius = 28

    def run(self) -> None:
        while self.running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                elif event.type == pygame.KEYDOWN:
                    if event.key in (pygame.K_ESCAPE, pygame.K_SPACE):
                        self.running = False
                elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    self.running = False

            self._update()
            self._render()
            self.clock.tick(FPS)

        pygame.quit()

    def _update(self) -> None:
        width, height = self.screen.get_size()
        self.ball_position[0] += self.ball_velocity[0] * (1.0 / FPS)
        self.ball_position[1] += self.ball_velocity[1] * (1.0 / FPS)

        if self.ball_position[0] - self.ball_radius < 0 or self.ball_position[0] + self.ball_radius > width:
            self.ball_velocity[0] *= -1
        if self.ball_position[1] - self.ball_radius < 0 or self.ball_position[1] + self.ball_radius > height:
            self.ball_velocity[1] *= -1

    def _render(self) -> None:
        width, height = self.screen.get_size()
        self.screen.fill((18, 22, 46))

        pygame.draw.circle(self.screen, (255, 180, 60), [int(self.ball_position[0]), int(self.ball_position[1])], self.ball_radius)
        pygame.draw.line(self.screen, (120, 200, 255), (0, height - 64), (width, height - 64), 4)

        title = self.font.render("Demo App", True, (230, 230, 255))
        title_rect = title.get_rect(center=(width // 2, 80))
        self.screen.blit(title, title_rect)

        hint = self.font.render("Press ESC / SPACE or click to return", True, (180, 180, 200))
        hint_rect = hint.get_rect(center=(width // 2, height - 80))
        self.screen.blit(hint, hint_rect)

        pygame.display.flip()
