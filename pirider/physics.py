from __future__ import annotations

import math
from typing import List, Tuple

from .config import FRICTION, GRAVITY, RIDER_RADIUS
from .track import Track

Point = Tuple[int, int]


class Rider:
    def __init__(self, spawn: Point) -> None:
        self.spawn: Point = spawn
        self.reset()

    def reset(self) -> None:
        self.position = [float(self.spawn[0]), float(self.spawn[1])]
        self.velocity = [0.0, 0.0]


class PhysicsEngine:
    def __init__(self, spawn: Point) -> None:
        self.rider = Rider(spawn)

    def reset(self) -> None:
        self.rider.reset()

    def update(self, dt: float, track: Track, active: bool) -> None:
        if not active:
            return

        self.rider.velocity[1] += GRAVITY * dt
        next_x = self.rider.position[0] + self.rider.velocity[0] * dt
        next_y = self.rider.position[1] + self.rider.velocity[1] * dt
        next_position = [next_x, next_y]

        if not track.is_empty():
            next_position, self.rider.velocity = self._resolve_collisions(
                next_position, self.rider.velocity, track.segments
            )

        self.rider.position = next_position

    def _resolve_collisions(
        self,
        position: List[float],
        velocity: List[float],
        segments: List[tuple[Point, Point]],
    ) -> tuple[List[float], List[float]]:
        for start, end in segments:
            closest = self._closest_point_on_segment(position, start, end)
            dx = position[0] - closest[0]
            dy = position[1] - closest[1]
            distance = math.hypot(dx, dy)

            if distance < RIDER_RADIUS and distance > 0.0:
                normal = [dx / distance, dy / distance]
                position[0] = closest[0] + normal[0] * RIDER_RADIUS
                position[1] = closest[1] + normal[1] * RIDER_RADIUS

                tangent = [-normal[1], normal[0]]
                velocity_along_tangent = velocity[0] * tangent[0] + velocity[1] * tangent[1]
                velocity = [tangent[0] * velocity_along_tangent * FRICTION,
                            tangent[1] * velocity_along_tangent * FRICTION]

        return position, velocity

    @staticmethod
    def _closest_point_on_segment(
        point: List[float], start: Point, end: Point
    ) -> List[float]:
        sx, sy = start
        ex, ey = end
        px, py = point
        dx = ex - sx
        dy = ey - sy
        if dx == 0 and dy == 0:
            return [float(sx), float(sy)]

        t = ((px - sx) * dx + (py - sy) * dy) / (dx * dx + dy * dy)
        t = max(0.0, min(1.0, t))
        return [sx + dx * t, sy + dy * t]
