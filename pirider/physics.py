from __future__ import annotations

import math
from typing import List, Tuple

from .config import GRAVITY, RIDER_RADIUS, SURFACE_FRICTION
from .track import Track

Point = Tuple[int, int]


class Rider:
    def __init__(self, spawn: Point) -> None:
        self.spawn: Point = spawn
        self.reset()

    def reset(self) -> None:
        self.position = [float(self.spawn[0]), float(self.spawn[1])]
        self.velocity = [0.0, 0.0]
        self.on_ground = False


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
            next_position, self.rider.velocity, self.rider.on_ground = self._resolve_collisions(
                next_position, self.rider.velocity, track.segments, dt
            )
        else:
            self.rider.on_ground = False

        self.rider.position = next_position

    def _resolve_collisions(
        self,
        position: List[float],
        velocity: List[float],
        segments: List[tuple[Point, Point]],
        dt: float,
    ) -> tuple[List[float], List[float], bool]:
        on_ground = False
        for start, end in segments:
            closest = self._closest_point_on_segment(position, start, end)
            dx = position[0] - closest[0]
            dy = position[1] - closest[1]
            distance = math.hypot(dx, dy)

            if distance <= RIDER_RADIUS:
                normal = [0.0, 0.0]
                if distance > 0.0:
                    normal = [dx / distance, dy / distance]
                else:
                    segment_dx = end[0] - start[0]
                    segment_dy = end[1] - start[1]
                    length = math.hypot(segment_dx, segment_dy)
                    if length == 0.0:
                        continue
                    tangent = [segment_dx / length, segment_dy / length]
                    normal = [-tangent[1], tangent[0]]
                    if velocity[0] * normal[0] + velocity[1] * normal[1] < 0:
                        normal = [-normal[0], -normal[1]]
                    position[0] = closest[0] + normal[0] * RIDER_RADIUS
                    position[1] = closest[1] + normal[1] * RIDER_RADIUS

                if distance > 0.0:
                    position[0] = closest[0] + normal[0] * RIDER_RADIUS
                    position[1] = closest[1] + normal[1] * RIDER_RADIUS

                tangent = [-normal[1], normal[0]]
                velocity_normal = velocity[0] * normal[0] + velocity[1] * normal[1]
                velocity_tangent = velocity[0] * tangent[0] + velocity[1] * tangent[1]

                if velocity_normal < 0.0:
                    velocity_normal = 0.0

                damping = pow(SURFACE_FRICTION, dt * 60.0)
                velocity_tangent *= damping

                velocity = [
                    tangent[0] * velocity_tangent + normal[0] * velocity_normal,
                    tangent[1] * velocity_tangent + normal[1] * velocity_normal,
                ]

                if abs(velocity_tangent) < 5.0 and velocity_normal == 0.0:
                    velocity = [0.0, 0.0]

                on_ground = True

        return position, velocity, on_ground

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
