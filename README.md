# WatermarkRemover

A desktop application for removing watermarks from videos using AI-powered inpainting (ProPainter), with a modern glassmorphism UI.

## Features

- **Video Loading** — Support for MP4, AVI, MOV, MKV, WebM with frame-by-frame navigation
- **Zone Drawing** — Draw rectangular watermark zones directly on the video canvas
- **Keyframe System** — Define different zones at different points in the video with automatic interpolation
- **AI Inpainting** — ProPainter-based intelligent watermark removal
- **Batch Processing** — Queue multiple videos for sequential processing
- **Save/Load Zones** — Persist zone configurations as JSON files
- **Modern UI** — Glassmorphism design with Windows Acrylic/Mica effects

## Workflow

1. **Load** a video file
2. **Navigate** through frames using the timeline slider
3. **Draw** rectangles over watermark areas
4. **Add keyframes** if the watermark moves across the video
5. **Process** — ProPainter inpaints the marked zones
6. **Output** — Clean video saved as `clean_{original_name}.mp4`

## Tech Stack

| Technology | Purpose |
|-----------|---------|
| PySide6 | Qt UI framework |
| PySide6-Fluent-Widgets | Modern fluent design components |
| qframelesswindow | Windows Acrylic/Mica effects |
| PyTorch (>=2.0) | Deep learning backend |
| OpenCV (>=4.8) | Video/image manipulation |
| ProPainter | AI inpainting model |
| NumPy | Numerical computation |
| Pillow | Image processing |

## Project Structure

```
WatermarkRemover/
├── main.py                    # Entry point
├── requirements.txt           # Dependencies
├── src/
│   ├── app.py                 # Main orchestrator
│   ├── core/
│   │   ├── video_player.py    # Video loading & frame extraction
│   │   └── keyframe_manager.py # Zone & keyframe management
│   ├── ui/
│   │   ├── main_window.py     # Frameless window with Acrylic
│   │   ├── sidebar.py         # Control panel
│   │   ├── canvas_area.py     # Video display + zone drawing
│   │   └── timeline.py        # Frame navigation
│   ├── components/
│   │   ├── glass_panel.py     # Glassmorphism container
│   │   ├── glow_button.py     # Glow effect button
│   │   ├── gradient_progress.py # Orange gradient progress bar
│   │   └── icon_button.py     # Icon buttons
│   └── styles/
│       ├── stylesheet.qss     # Global stylesheet
│       └── colors.py          # Color palette
├── propainter/                # ProPainter inpainting module
└── output/                    # Processed videos
```

## Design

- **Theme:** Deep Space + Vibrant Orange Glow
- **Background:** `#0f0f1e` → `#1a1a2e`
- **Accent:** `#ff6b35` → `#f7931e`
- **Effects:** Glassmorphism, Windows Acrylic/Mica, glow animations

## Install

```bash
pip install -r requirements.txt
```

## Run

```bash
python main.py
```

## Prerequisites

- Python 3.9+
- Windows 10/11 (for Acrylic/Mica effects, falls back gracefully on other platforms)
- CUDA-compatible GPU recommended for ProPainter processing
