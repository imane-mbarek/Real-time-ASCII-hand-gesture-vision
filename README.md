```
 █████╗ ███████╗ ██████╗██╗██╗    ██╗██╗███████╗██╗ ██████╗ ███╗   ██╗
██╔══██╗██╔════╝██╔════╝██║██║    ██║██║██╔════╝██║██╔═══██╗████╗  ██║
███████║███████╗██║     ██║██║    ██║██║███████╗██║██║   ██║██╔██╗ ██║
██╔══██║╚════██║██║     ██║╚██╗  ██╔╝██║╚════██║██║██║   ██║██║╚██╗██║
██║  ██║███████║╚██████╗██║ ╚████╔╝ ██║███████║██║╚██████╔╝██║ ╚████║
╚═╝  ╚═╝╚══════╝ ╚═════╝╚═╝  ╚═══╝  ╚═╝╚══════╝╚═╝ ╚═════╝ ╚═╝  ╚═══╝
```

<div align="center">

**Your face. In characters. Controlled by your hands.**

![Python](https://img.shields.io/badge/Python-3.8+-blue?style=flat-square&logo=python)
![OpenCV](https://img.shields.io/badge/OpenCV-4.x-green?style=flat-square&logo=opencv)
![MediaPipe](https://img.shields.io/badge/MediaPipe-0.10-orange?style=flat-square)
![License](https://img.shields.io/badge/License-MIT-purple?style=flat-square)

</div>

---

## What is this ?

A real-time webcam feed transformed into ASCII art — pixel by pixel, character by character.  
No buttons. No keyboard. Just your hand.

```
normal camera  ──[ fist 1s ]──►  ASCII mode
ASCII mode     ──[ fist 2s ]──►  normal camera
```

---

## How it works

Every frame from the webcam goes through this pipeline :

```
webcam frame (640×480)
       │
       ▼
shrink to grid (e.g. 60×30)
       │
       ▼
each pixel → gray value (0–255)
       │
       ▼
gray value → index in charset
       │
       ▼
draw each character on black image
       │
       ▼
overlay hand skeleton on top
       │
       ▼
display
```

The charset goes from dense to light :

```
@ & % W Q N M 0 g B $ # D R 8 m ... - ' ` (space)
▲                                           ▲
dark pixels                          bright pixels
```

---

## Gesture controls

| Gesture | Action |
|---|---|
| Hold fist **1 second** | Activate ASCII mode |
| Move thumb and index apart | Increase resolution (more columns) |
| Move thumb and index close | Decrease resolution (less columns) |
| Hold fist **2 seconds** | Return to normal camera |

> Resolution range : **15 columns** (abstract) to **130 columns** (detailed)

---

## Hand skeleton

A stylized skeleton is drawn on top of the ASCII art in real time :

- **Joints** — golden glowing dots
- **Fingertips** — cyan outlined circles
- **Connections** — dark halo + bright gold line on top

---

## Installation

```bash
# Clone the repo
git clone https://github.com/your-username/ascii-vision.git
cd ascii-vision

# Install dependencies
pip install opencv-python mediapipe numpy

# Run
python ascii_convert.py
```

> Requires Python 3.8+ and a working webcam.

---

## Project structure

```
ascii-vision/
│
├── ascii_convert.py      # main file — everything is here
└── README.md
```

---

## Built step by step

This project was built from scratch, one concept at a time :

```
step 1  →  open webcam
step 2  →  convert to grayscale
step 3  →  shrink frame into a grid
step 4  →  map each pixel to a character
step 5  →  draw characters on black image
step 6  →  add MediaPipe hand detection
step 7  →  detect fist gesture
step 8  →  control resolution with finger distance
step 9  →  IDLE / ASCII state machine
step 10 →  real pixel colors per character
bonus   →  stylized hand skeleton overlay
```

---

## Key concept

The core idea in one line :

```python
idx  = int(gray_value / 255 * (len(charset) - 1))
char = charset[idx]
```

A pixel with brightness 200/255 maps to index ~78 in the charset — a medium-density character.  
A dark pixel becomes `@`. A bright pixel becomes a space.

---

<div align="center">

Made with OpenCV · MediaPipe · ASCII

</div>
