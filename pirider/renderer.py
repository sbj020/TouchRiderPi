from __future__ import annotations

import pygame

from .config import (
    BACKGROUND_COLOR,
    HUD_COLOR,
    LINE_COLOR,
    LINE_WIDTH,
    RIDER_COLOR,
    RIDER_RADIUS,
    TOOL_BUTTON_ACTIVE,
    TOOL_BUTTON_BG,
    TOOL_BUTTON_INACTIVE,
    TOOL_BUTTON_SIZE,
)
from .track import Track
from .physics import Rider


tool_label_map = {
    "draw": "Draw",
    "line": "Line",
    "drag": "Drag",
}


class Renderer:
    def __init__(self, screen: pygame.Surface) -> None:
        self.screen = screen
        self.font = pygame.font.Font(None, 24)
        self.label_font = pygame.font.Font(None, 18)

    def _world_to_screen(self, point: tuple[int, int], offset: tuple[float, float]) -> tuple[int, int]:
        return (
            int(point[0] - offset[0]),
            int(point[1] - offset[1]),
        )

    def render(
        self,
        track: Track,
        rider: Rider,
        paused: bool,
        save_file: str,
        offset: tuple[float, float],
        active_tool: str,
        tool_buttons: list[tuple[str, pygame.Rect]],
        line_start: tuple[int, int] | None,
        line_preview: tuple[int, int] | None,
    ) -> None:
        self.screen.fill(BACKGROUND_COLOR)

        for stroke in track.strokes:
            if len(stroke) > 1:
                points = [self._world_to_screen(point, offset) for point in stroke]
                pygame.draw.lines(self.screen, LINE_COLOR, False, points, LINE_WIDTH)

        if line_start is not None and line_preview is not None and active_tool == "line":
            start = self._world_to_screen(line_start, offset)
            end = self._world_to_screen(line_preview, offset)
            pygame.draw.line(self.screen, LINE_COLOR, start, end, LINE_WIDTH)

        rider_pos = self._world_to_screen((int(rider.position[0]), int(rider.position[1])), offset)
        pygame.draw.circle(
            self.screen,
            RIDER_COLOR,
            rider_pos,
            RIDER_RADIUS,
        )

        self._draw_tool_buttons(active_tool, tool_buttons)
        self._draw_hud(paused, save_file, active_tool)
        pygame.display.flip()

    def _draw_tool_buttons(self, active_tool: str, tool_buttons: list[tuple[str, pygame.Rect]]) -> None:
        for tool, rect in tool_buttons:
            color = TOOL_BUTTON_ACTIVE if tool == active_tool else TOOL_BUTTON_INACTIVE
            pygame.draw.rect(self.screen, color, rect, border_radius=8)
            pygame.draw.rect(self.screen, TOOL_BUTTON_BG, rect.inflate(-4, -4), border_radius=6)
            self._draw_tool_icon(tool, rect)

            label_text = tool_label_map.get(tool, tool.capitalize())
            label_surface = self.label_font.render(label_text, True, HUD_COLOR)
            label_rect = label_surface.get_rect(center=(rect.centerx, rect.bottom + 12))
            self.screen.blit(label_surface, label_rect)

    def _draw_tool_icon(self, tool: str, rect: pygame.Rect) -> None:
        center = rect.center
        if tool == "draw":
            points = [
                (center[0] - 8, center[1] + 6),
                (center[0] + 8, center[1] - 6),
                (center[0] + 6, center[1] - 8),
                (center[0] - 6, center[1] + 6),
            ]
            pygame.draw.lines(self.screen, LINE_COLOR, False, points, 3)
        elif tool == "line":
            start = (center[0] - 10, center[1] + 6)
            end = (center[0] + 10, center[1] - 6)
            pygame.draw.line(self.screen, LINE_COLOR, start, end, 3)
        elif tool == "drag":
            offset = 6
            arms = [
                ((center[0], center[1] - offset), (center[0], center[1] + offset)),
                ((center[0] - offset, center[1]), (center[0] + offset, center[1])),
            ]
            for line in arms:
                pygame.draw.line(self.screen, LINE_COLOR, line[0], line[1], 3)
            pygame.draw.circle(self.screen, LINE_COLOR, center, 3)

    def _draw_hud(self, paused: bool, save_file: str, active_tool: str) -> None:
        status = "Paused" if paused else "Running"
        tool_name = active_tool.capitalize()
        mode_hint = "Paused: draw/drag freely" if paused else "Playing: camera follows rider"
        lines = [
            f"{status}  |  Tool: {tool_name}",
            f"{mode_hint}",
            f"Space: start/pause  R: reset  C: clear",
            f"S: save  L: load  Esc: quit",
            f"T: tool click 1/2/3: draw, line, drag",
            f"Saved track: {save_file}",
        ]

        for index, text in enumerate(lines):
            surface = self.font.render(text, True, HUD_COLOR)
            self.screen.blit(surface, (12, 12 + index * 26))
