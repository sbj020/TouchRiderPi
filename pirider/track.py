from __future__ import annotations

import json
from pathlib import Path
from typing import List, Tuple

Point = Tuple[int, int]


class Track:
    def __init__(self) -> None:
        self.strokes: List[List[Point]] = []
        self.current_stroke: List[Point] | None = None

    def start_stroke(self, point: Point) -> None:
        self.current_stroke = [point]
        self.strokes.append(self.current_stroke)

    def add_point(self, point: Point) -> None:
        if self.current_stroke is None:
            self.start_stroke(point)
            return

        if not self.current_stroke or self.current_stroke[-1] != point:
            self.current_stroke.append(point)

    def end_stroke(self) -> None:
        if self.current_stroke is None:
            return

        if len(self.current_stroke) < 2:
            self.strokes.pop()
        self.current_stroke = None

    def clear(self) -> None:
        self.strokes.clear()
        self.current_stroke = None

    def is_empty(self) -> bool:
        return len(self.segments) == 0

    @property
    def segments(self) -> List[tuple[Point, Point]]:
        result: List[tuple[Point, Point]] = []
        for stroke in self.strokes:
            result.extend(
                (stroke[i], stroke[i + 1])
                for i in range(len(stroke) - 1)
            )
        return result

    def save(self, path: Path) -> None:
        payload = {"strokes": self.strokes}
        with open(path, "w", encoding="utf-8") as handle:
            json.dump(payload, handle, indent=2)

    def load(self, path: Path) -> bool:
        if not path.exists():
            return False

        with open(path, "r", encoding="utf-8") as handle:
            payload = json.load(handle)

        if not isinstance(payload, dict):
            return False

        strokes = self._load_strokes(payload)
        if strokes is None:
            return False

        self.strokes = strokes
        self.current_stroke = None
        return True

    @staticmethod
    def _load_strokes(payload: dict) -> List[List[Point]] | None:
        raw_strokes = payload.get("strokes")
        if isinstance(raw_strokes, list):
            strokes: List[List[Point]] = []
            for raw_stroke in raw_strokes:
                if not isinstance(raw_stroke, list):
                    return None
                stroke: List[Point] = []
                for item in raw_stroke:
                    if (
                        isinstance(item, list)
                        and len(item) == 2
                        and isinstance(item[0], int)
                        and isinstance(item[1], int)
                    ):
                        stroke.append((item[0], item[1]))
                    else:
                        return None
                if stroke:
                    strokes.append(stroke)
            return strokes

        raw_points = payload.get("points")
        if isinstance(raw_points, list):
            points: List[Point] = []
            for item in raw_points:
                if (
                    isinstance(item, list)
                    and len(item) == 2
                    and isinstance(item[0], int)
                    and isinstance(item[1], int)
                ):
                    points.append((item[0], item[1]))
                else:
                    return None
            return [points] if points else []

        return None
