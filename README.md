# PiRider

Minimal Line-Rider–style prototype built with pygame.

This repository is now organized as a modular **Game Center** launcher with PiRider and a second demo app as selectable entries.

Run `main.py` to start the launcher, then select PiRider or Demo App from the menu.

## Features

- Modular boot launcher for multiple apps
- PiRider game with draw/line/drag controls
- A second demo app as a placeholder for future expansion
- Save / load tracks (`saved_track.json`)
- Pause/play with camera follow behavior in PiRider

## Requirements

- Python 3.9+ (3.11 recommended)
- pygame (>=2.0)

## Quick start (recommended)

1. Create and activate a virtual environment:

```bash
python3 -m venv venv
source venv/bin/activate
```

2. Upgrade pip and install dependencies:

```bash
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
```

3. Run the launcher:

```bash
PIRIDER_WINDOWED=1 python3 main.py
```

This starts the Game Center menu. Select PiRider or Demo App to run that app.

## Available apps

- `PiRider` — the Line Rider–style game
- `Demo App` — a simple bouncing-ball demo placeholder

## Raspberry Pi notes

This project runs on Raspberry Pi OS but pygame may require system libraries before pip can build wheels. On a Raspberry Pi (4/5 recommended), run:

```bash
sudo apt update
sudo apt install -y python3-pip python3-venv \
  libsdl2-dev libsdl2-image-dev libsdl2-mixer-dev libsdl2-ttf-dev \
  libportmidi-dev libfreetype6-dev libavformat-dev libavcodec-dev libswscale-dev pkg-config

python3 -m venv venv
source venv/bin/activate
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
```

If `pip install -r requirements.txt` fails for `pygame`, try:

```bash
python -m pip install --upgrade pygame --user
```

or consult the pygame documentation for Raspberry Pi-specific build instructions.

Hardware tips:
- Use Raspberry Pi 4/5 for best performance.
- Use a desktop environment (X11/Wayland) with GPU acceleration enabled.
- For a touchscreen, you may need to map touch events or add finger-event handling (future work).

### Apt packages (explicit)

For Raspberry Pi OS Desktop (Bullseye/Bookworm), these packages are commonly needed to build or run `pygame` from source or when wheels are unavailable:

```bash
sudo apt update
sudo apt install -y \
  build-essential python3-dev python3-pip python3-venv \
  libsdl2-dev libsdl2-image-dev libsdl2-mixer-dev libsdl2-ttf-dev \
  libportmidi-dev libfreetype6-dev libavformat-dev libavcodec-dev libswscale-dev pkg-config
```

If you run Raspberry Pi OS Lite, you'll need an X server or an alternative display system for pygame.

## Controls

- Mouse left-click + drag: tool-specific actions in PiRider
  - Draw tool (1): freehand stroke while dragging
  - Line tool (2): click-drag to preview and place a straight segment
  - Drag tool (3): pan camera (horizontal pan is inverted intentionally)
- Toolbar: bottom-left clickable tool buttons
- Keyboard shortcuts in PiRider:
  - `1` — Draw tool
  - `2` — Line tool
  - `3` — Drag tool
  - `Space` — Pause / Play (camera follows only when playing)
  - `R` — Reset rider
  - `C` — Clear track
  - `S` — Save track
  - `L` — Load track

## Saving

Tracks are saved to and loaded from `saved_track.json` in the project directory using the in‑game Save/Load controls or the `S`/`L` keys.

## Performance tuning

If you see low framerate on a Pi:
- Reduce `FPS` in `pirider/config.py` (try `30`).
- Reduce stroke point density (simplify strokes before saving).
- Run in windowed mode if fullscreen GPU drivers cause issues.

## Troubleshooting

- ModuleNotFoundError: No module named 'pygame'
  - Ensure you're running the same Python interpreter where you installed `pygame` (check `python -m pip show pygame`).
  - Use a venv or `--user` install as shown above.

- If the program starts but input feels off, verify the camera-follow and screen->world mapping; the project uses an offset-based camera so drawing uses world coordinates.

## Architecture

- `main.py` — launcher entrypoint for the Game Center
- `game_center.py` — modular app selector and boot menu
- `pirider/apps.py` — app registry for available apps
- `pirider/demo_app.py` — second app placeholder
- `pirider/` — the PiRider game package

### Adding new apps

To add a new app, register it in `pirider/apps.py` with a name and a launch callback. Each app can be a separate package or module.

## Development

- Code lives in the `pirider/` package.
  - `app.py` — main loop and camera
  - `input_handler.py` — input handling and tool behaviors
  - `renderer.py` — rendering and HUD
  - `track.py` — stroke storage and save/load
  - `physics.py` — rider physics and collisions
  - `config.py` — constants

- Run quick syntax checks:

```bash
python3 -m py_compile main.py game_center.py pirider/*.py
```

## Optional: run PiRider as a kiosk (systemd)

Create a systemd service to start the launcher at boot on Raspberry Pi OS (Desktop). Example `/etc/systemd/system/pirider.service`:

```
[Unit]
Description=PiRider Game Center
After=graphical.target

[Service]
User=pi
Environment=DISPLAY=:0
WorkingDirectory=/home/pi/PiRider
ExecStart=/home/pi/PiRider/venv/bin/python /home/pi/PiRider/main.py
Restart=on-failure

[Install]
WantedBy=graphical.target
```

Enable and start:

```bash
sudo systemctl daemon-reload
sudo systemctl enable --now pirider.service
```

Adjust paths and user as appropriate.

## Next steps / TODO

- Add touch/finger input handling for touchscreen play.
- Reduce stroke density and add smoothing for better physics performance.
- Add on-device packaging / systemd service for kiosk-style startup on Raspberry Pi.
- Add more apps to the Game Center menu.

---

If you'd like, I can also:
- Commit the launcher and README changes,
- Add a simple `Makefile` or `pyproject.toml`,
- Or build another demo app for the menu.
