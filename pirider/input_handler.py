from __future__ import annotations

import pygame
from pygame.event import Event
from typing import Iterable

from .track import Track


class InputHandler:
    def __init__(self, track: Track) -> None:
        self.track = track
        self.drawing = False

    def process(self, events: Iterable[Event]) -> set[str]:
        actions: set[str] = set()

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

            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                self.drawing = True
                self.track.add_point(event.pos)

            elif event.type == pygame.MOUSEBUTTONUP and event.button == 1:
                self.drawing = False

            elif event.type == pygame.MOUSEMOTION and self.drawing:
                self.track.add_point(event.pos)

        return actions
