#!/usr/bin/env python3
"""
WatermarkRemover - Modern Glassmorphism Video Watermark Removal Tool
Using ProPainter for high-quality video inpainting

A beautiful, modern UI for removing watermarks from videos.
"""

import sys
import os
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent))


def main():
    """Main entry point"""
    # Import PySide6 first to set up Qt
    from PySide6.QtWidgets import QApplication
    from PySide6.QtCore import Qt
    from PySide6.QtGui import QFont

    # Enable high DPI scaling
    QApplication.setHighDpiScaleFactorRoundingPolicy(
        Qt.HighDpiScaleFactorRoundingPolicy.PassThrough
    )

    # Create application
    app = QApplication(sys.argv)

    # Set application info
    app.setApplicationName("WatermarkRemover")
    app.setApplicationVersion("2.0.0")
    app.setOrganizationName("WatermarkRemover")

    # Set default font
    font = QFont("Segoe UI", 10)
    app.setFont(font)

    # Load stylesheet
    stylesheet_path = Path(__file__).parent / "src" / "styles" / "stylesheet.qss"
    if stylesheet_path.exists():
        with open(stylesheet_path, "r", encoding="utf-8") as f:
            app.setStyleSheet(f.read())

    # Create and run application
    from src.app import WatermarkRemoverApp

    watermark_app = WatermarkRemoverApp()
    watermark_app.run()

    # Run event loop
    sys.exit(app.exec())


if __name__ == "__main__":
    main()
