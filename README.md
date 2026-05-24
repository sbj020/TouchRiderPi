# PiRider

A minimal Line Rider-style prototype built with `pygame`.
This version is an MVP focused on mouse track drawing and a simple rider physics system.

## Requirements

- Python 3.10+
- `pygame`

## Install

```bash
python3 -m pip install -r requirements.txt
```

## Run

```bash
python3 main.py
```

## Controls

- Left mouse button: draw track
- Space: start / pause simulation
- R: reset rider to spawn point
- C: clear current track
- S: save current track to `saved_track.json`
- L: load track from `saved_track.json`
- Esc: quit

## Notes

- The track is stored as a sequence of connected points.
- The rider is a simple circle affected by gravity.
- Collision is approximated by pushing the rider out of nearby track segments and keeping velocity along the slope.

## TODO

- Add touchscreen input support as a separate input handler.
- Improve collision handling for fast slopes and gaps.
- Add a visual start point and restart animation.
- Add sound and visual polish for Raspberry Pi display.
