from __future__ import annotations

import pygame
from pygame.event import Event
from typing import Iterable, Tuple

from .track import Track


class InputHandler:
    def __init__(self, track: Track) -> None:
        self.track = track
        self.drawing = False
        self.dragging = False
        self.drag_last_pos: tuple[int, int] | None = None
        self.line_start: tuple[int, int] | None = None
        self.line_preview: tuple[int, int] | None = None

    def process(
        self,
        events: Iterable[Event],
        offset: Tuple[float, float] = (0.0, 0.0),
        active_tool: str = "draw",
    ) -> tuple[set[str], tuple[float, float] | None]:
        actions: set[str] = set()
        drag_delta: tuple[float, float] | None = None

        for event in events:
            if event.type == pygame.QUIT:
                actions.add("quit")

            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    actions.add("quit")
                elif event.key == pygame.K_SPACE:
                    actions.add("toggle_pause")
                elif event.key == pygame.K_r:
                    actions.add("reset")
                elif event.key == pygame.K_c:
                    actions.add("clear")
                elif event.key == pygame.K_s:
                    actions.add("save")
                elif event.key == pygame.K_l:
                    actions.add("load")
                elif event.key == pygame.K_1:
                    actions.add("tool_draw")
                elif event.key == pygame.K_2:
                    actions.add("tool_line")
                elif event.key == pygame.K_3:
                    actions.add("tool_drag")

            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                if active_tool == "draw":
                    self.drawing = True
                    self.track.start_stroke(self._screen_to_world(event.pos, offset))
                elif active_tool == "line":
                    self.drawing = True
                    self.line_start = self._screen_to_world(event.pos, offset)
                    self.line_preview = self.line_start
                elif active_tool == "drag":
                    self.dragging = True
                    self.drag_last_pos = event.pos

            elif event.type == pygame.MOUSEBUTTONUP and event.button == 1:
                if active_tool == "draw":
                    self.drawing = False
                    self.track.end_stroke()
                elif active_tool == "line":
                    if self.drawing and self.line_start is not None:
                        end_point = self._screen_to_world(event.pos, offset)
                        if end_point != self.line_start:
                            self.track.start_stroke(self.line_start)
                            self.track.add_point(end_point)
                            self.track.end_stroke()
                    self.drawing = False
                    self.line_start = None
                    self.line_preview = None
                elif active_tool == "drag":
                    self.dragging = False
                    self.drag_last_pos = None

            elif event.type == pygame.MOUSEMOTION:
                if active_tool == "draw" and self.drawing:
                    self.track.add_point(self._screen_to_world(event.pos, offset))
                elif active_tool == "line" and self.drawing and self.line_start is not None:
                    self.line_preview = self._screen_to_world(event.pos, offset)
                elif active_tool == "drag" and self.dragging and self.drag_last_pos is not None:
                    dx = event.pos[0] - self.drag_last_pos[0]
                    dy = event.pos[1] - self.drag_last_pos[1]
                    drag_delta = (-dx, -dy)
                    self.drag_last_pos = event.pos

        return actions, drag_delta

    @staticmethod
    def _screen_to_world(point: Tuple[int, int], offset: Tuple[float, float]) -> Tuple[int, int]:
        return (int(point[0] + offset[0]), int(point[1] + offset[1]))
