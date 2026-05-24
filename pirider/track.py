from __future__ import annotations

import json
from pathlib import Path
from typing import Iterable, List, Tuple

Point = Tuple[int, int]


class Track:
    def __init__(self) -> None:
        self.points: List[Point] = []

    def add_point(self, point: Point) -> None:
        if not self.points or self.points[-1] != point:
            self.points.append(point)

    def clear(self) -> None:
        self.points.clear()

    def is_empty(self) -> bool:
        return len(self.points) < 2

    @property
    def segments(self) -> List[tuple[Point, Point]]:
        return [
            (self.points[i], self.points[i + 1])
            for i in range(len(self.points) - 1)
        ]

    def save(self, path: Path) -> None:
        payload = {"points": self.points}
        with open(path, "w", encoding="utf-8") as handle:
            json.dump(payload, handle, indent=2)

    def load(self, path: Path) -> bool:
        if not path.exists():
            return False

        with open(path, "r", encoding="utf-8") as handle:
            payload = json.load(handle)

        raw_points = payload.get("points", [])
        if not isinstance(raw_points, list):
            return False

        points: List[Point] = []
        for item in raw_points:
            if (
                isinstance(item, list)
                and len(item) == 2
                and isinstance(item[0], int)
                and isinstance(item[1], int)
            ):
                points.append((item[0], item[1]))

        self.points = points
        return True
