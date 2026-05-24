from __future__ import annotations

import pygame

from .config import FPS, TRACK_SAVE_FILE, WINDOW_FLAGS
from .input_handler import InputHandler
from .physics import PhysicsEngine
from .renderer import Renderer
from .track import Track


class App:
    def __init__(self) -> None:
        pygame.init()
        pygame.display.set_caption("PiRider")
        self.screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN | WINDOW_FLAGS)
        self.clock = pygame.time.Clock()
        self.track = Track()
        self.input_handler = InputHandler(self.track)
        spawn = self._calculate_spawn_point()
        self.physics_engine = PhysicsEngine(spawn)
        self.renderer = Renderer(self.screen)
        self.running = True
        self.paused = True

    def _calculate_spawn_point(self) -> tuple[int, int]:
        width, height = self.screen.get_size()
        return (width // 4, height // 4)

    def run(self) -> None:
        while self.running:
            events = pygame.event.get()
            actions = self.input_handler.process(events)
            self._apply_actions(actions)

            dt = self.clock.get_time() / 1000.0
            self.physics_engine.update(dt, self.track, not self.paused)
            self.renderer.render(self.track, self.physics_engine.rider, self.paused, str(TRACK_SAVE_FILE))
            self.clock.tick(FPS)

        pygame.quit()

    def _apply_actions(self, actions: set[str]) -> None:
        if "quit" in actions:
            self.running = False

        if "toggle_pause" in actions:
            self.paused = not self.paused

        if "reset" in actions:
            self.physics_engine.reset()

        if "clear" in actions:
            self.track.clear()
            self.physics_engine.reset()

        if "save" in actions:
            self.track.save(TRACK_SAVE_FILE)

        if "load" in actions:
            if self.track.load(TRACK_SAVE_FILE):
                self.physics_engine.reset()
