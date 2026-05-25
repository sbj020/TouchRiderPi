from __future__ import annotations

from dataclasses import dataclass
from typing import Callable

import pygame

from .app import App as PiRiderApp
from .demo_app import DemoApp


@dataclass
class AppEntry:
    name: str
    launch: Callable[[], None]


def launch_pirider() -> None:
    pygame.quit()
    PiRiderApp().run()


def launch_demo_app() -> None:
    pygame.quit()
    DemoApp().run()


def get_available_apps() -> list[AppEntry]:
    return [
        AppEntry("PiRider", launch_pirider),
        AppEntry("Demo App", launch_demo_app),
    ]
