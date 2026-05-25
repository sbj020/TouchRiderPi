from __future__ import annotations

import os
import math
import pygame

from .config import CAMERA_DEADZONE, CAMERA_SMOOTHING, FPS, TRACK_SAVE_FILE, TOOL_BUTTON_SIZE
from .input_handler import InputHandler
from .physics import PhysicsEngine
from .renderer import Renderer
from .track import Track


class App:
    def __init__(self) -> None:
        pygame.init()
        pygame.display.set_caption("PiRider")
        flags = pygame.FULLSCREEN
        if os.environ.get("PIRIDER_WINDOWED") == "1":
            flags = 0

        self.screen = pygame.display.set_mode((0, 0), flags)
        self.clock = pygame.time.Clock()
        self.track = Track()
        self.input_handler = InputHandler(self.track)
        spawn = self._calculate_spawn_point()
        self.physics_engine = PhysicsEngine(spawn)
        self.renderer = Renderer(self.screen)
        self.running = True
        self.paused = True
        self.camera_offset = [0.0, 0.0]
        self._center_camera_on_point(spawn, instant=True)
        self.active_tool = "draw"
        self.tool_buttons = self._create_tool_buttons()
        self.line_start = None
        self.line_preview = None

    def _create_tool_buttons(self) -> list[tuple[str, pygame.Rect]]:
        width, height = self.screen.get_size()
        x = 12
        y = height - TOOL_BUTTON_SIZE[1] - 12
        buttons = []
        for tool in ["draw", "line", "drag"]:
            buttons.append((tool, pygame.Rect(x, y, TOOL_BUTTON_SIZE[0], TOOL_BUTTON_SIZE[1])))
            x += TOOL_BUTTON_SIZE[0] + 10
        return buttons

    def _calculate_spawn_point(self) -> tuple[int, int]:
        width, height = self.screen.get_size()
        return (width // 4, height // 4)

    def _center_camera_on_point(self, point: tuple[int, int], instant: bool = False) -> None:
        width, height = self.screen.get_size()
        target_x = point[0] - width / 2
        target_y = point[1] - height / 2
        if instant:
            self.camera_offset[0] = target_x
            self.camera_offset[1] = target_y
        else:
            self.camera_offset[0] += target_x - self.camera_offset[0]
            self.camera_offset[1] += target_y - self.camera_offset[1]

    def _update_camera(self, dt: float) -> None:
        speed = math.hypot(*self.physics_engine.rider.velocity)
        if speed < 20.0:
            return

        width, height = self.screen.get_size()
        target_x = self.physics_engine.rider.position[0] - width / 2
        target_y = self.physics_engine.rider.position[1] - height / 2

        dx = target_x - self.camera_offset[0]
        dy = target_y - self.camera_offset[1]
        distance = math.hypot(dx, dy)

        if distance < CAMERA_DEADZONE:
            return

        factor = min(1.0, CAMERA_SMOOTHING * dt)
        self.camera_offset[0] += dx * factor
        self.camera_offset[1] += dy * factor

    def _handle_toolbar_clicks(self, events: list[pygame.event.Event]) -> list[pygame.event.Event]:
        filtered_events: list[pygame.event.Event] = []
        for event in events:
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                if any(rect.collidepoint(event.pos) for _, rect in self.tool_buttons):
                    for tool, rect in self.tool_buttons:
                        if rect.collidepoint(event.pos):
                            self.active_tool = tool
                            self.line_start = None
                            self.line_preview = None
                            self.input_handler.drawing = False
                            self.input_handler.dragging = False
                            self.input_handler.drag_last_pos = None
                            break
                    continue
            filtered_events.append(event)
        return filtered_events

    def run(self) -> None:
        while self.running:
            events = pygame.event.get()
            events = self._handle_toolbar_clicks(events)
            actions, drag_delta = self.input_handler.process(events, tuple(self.camera_offset), self.active_tool)
            self._apply_actions(actions)

            dt = self.clock.tick(FPS) / 1000.0
            self.physics_engine.update(dt, self.track, not self.paused)
            if drag_delta is not None:
                self.camera_offset[0] += drag_delta[0]
                self.camera_offset[1] += drag_delta[1]
            if not self.paused:
                self._update_camera(dt)
            self.line_start = self.input_handler.line_start
            self.line_preview = self.input_handler.line_preview
            self.renderer.render(
                self.track,
                self.physics_engine.rider,
                self.paused,
                str(TRACK_SAVE_FILE),
                tuple(self.camera_offset),
                self.active_tool,
                self.tool_buttons,
                self.line_start,
                self.line_preview,
            )

        pygame.quit()

    def _apply_actions(self, actions: set[str]) -> None:
        if "quit" in actions:
            self.running = False

        if "toggle_pause" in actions:
            was_paused = self.paused
            self.paused = not self.paused
            if was_paused and not self.paused:
                self._center_camera_on_point(tuple(self.physics_engine.rider.position), instant=True)

        if "reset" in actions:
            self.physics_engine.reset()
            self._center_camera_on_point(tuple(self.physics_engine.rider.position), instant=True)

        if "clear" in actions:
            self.track.clear()
            self.physics_engine.reset()
            self._center_camera_on_point(tuple(self.physics_engine.rider.position), instant=True)

        if "save" in actions:
            self.track.save(TRACK_SAVE_FILE)

        if "load" in actions:
            if self.track.load(TRACK_SAVE_FILE):
                self.physics_engine.reset()
                self._center_camera_on_point(tuple(self.physics_engine.rider.position), instant=True)

        if "tool_draw" in actions:
            self.active_tool = "draw"

        if "tool_line" in actions:
            self.active_tool = "line"

        if "tool_drag" in actions:
            self.active_tool = "drag"
