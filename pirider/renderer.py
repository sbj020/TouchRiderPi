from __future__ import annotations

import pygame

from .config import BACKGROUND_COLOR, HUD_COLOR, LINE_COLOR, LINE_WIDTH, RIDER_COLOR, RIDER_RADIUS
from .track import Track
from .physics import Rider


class Renderer:
    def __init__(self, screen: pygame.Surface) -> None:
        self.screen = screen
        self.font = pygame.font.Font(None, 24)

    def render(self, track: Track, rider: Rider, paused: bool, save_file: str) -> None:
        self.screen.fill(BACKGROUND_COLOR)

        if len(track.points) > 1:
            pygame.draw.lines(self.screen, LINE_COLOR, False, track.points, LINE_WIDTH)

        pygame.draw.circle(
            self.screen,
            RIDER_COLOR,
            (int(rider.position[0]), int(rider.position[1])),
            RIDER_RADIUS,
        )

        self._draw_hud(paused, save_file)
        pygame.display.flip()

    def _draw_hud(self, paused: bool, save_file: str) -> None:
        status = "Paused" if paused else "Running"
        lines = [
            f"{status}  |  Space: start/pause  R: reset  C: clear",
            f"S: save  L: load  Esc: quit",
            f"Saved track: {save_file}",
        ]

        for index, text in enumerate(lines):
            surface = self.font.render(text, True, HUD_COLOR)
            self.screen.blit(surface, (12, 12 + index * 26))
