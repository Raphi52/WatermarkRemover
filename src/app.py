"""
WatermarkRemover Application - Main orchestration class
"""

import os
import sys
import threading
from pathlib import Path
from typing import Optional, List

from PySide6.QtWidgets import QApplication, QFileDialog, QVBoxLayout, QWidget
from PySide6.QtCore import QObject, Signal, Slot, QThread, Qt
from PySide6.QtGui import QFont

# Handle both direct execution and module import
if __name__ == "__main__" and __package__ is None:
    # Running as script - add parent to path and use absolute imports
    sys.path.insert(0, str(Path(__file__).parent.parent))
    from src.core.video_player import VideoPlayer
    from src.core.keyframe_manager import KeyframeManager
    from src.ui.main_window import MainWindow
    from src.ui.sidebar import Sidebar
    from src.ui.canvas_area import CanvasArea
    from src.ui.timeline import Timeline
    from src.styles.colors import Colors
else:
    # Running as module - use relative imports
    from .core.video_player import VideoPlayer
    from .core.keyframe_manager import KeyframeManager
    from .ui.main_window import MainWindow
    from .ui.sidebar import Sidebar
    from .ui.canvas_area import CanvasArea
    from .ui.timeline import Timeline
    from .styles.colors import Colors


class ProcessingWorker(QObject):
    """Worker for background video processing"""

    progress = Signal(int, int)  # current, total
    finished = Signal(str)  # output path
    error = Signal(str)  # error message

    def __init__(self, video_path: str, output_path: str, keyframes: dict):
        super().__init__()
        self.video_path = video_path
        self.output_path = output_path
        self.keyframes = keyframes
        self._cancelled = False

    def cancel(self):
        self._cancelled = True

    @Slot()
    def run(self):
        """Process the video"""
        try:
            # Import ProPainter processing
            from propainter import process_video

            def progress_callback(current, total):
                if self._cancelled:
                    raise InterruptedError("Processing cancelled")
                self.progress.emit(current, total)

            process_video(
                self.video_path,
                self.output_path,
                self.keyframes,
                progress_callback
            )

            self.finished.emit(self.output_path)

        except ImportError:
            self.error.emit("ProPainter module not found.\nRun: python download_model.py")
        except InterruptedError:
            self.error.emit("Processing cancelled")
        except Exception as e:
            self.error.emit(str(e))


class WatermarkRemoverApp:
    """
    Main application class that coordinates all components.
    """

    def __init__(self):
        # Core components
        self.video = VideoPlayer()
        self.keyframes = KeyframeManager()

        # State
        self.output_dir = os.path.join(os.path.dirname(__file__), "..", "output")
        self.batch_files: List[str] = []
        self._processing = False
        self._worker: Optional[ProcessingWorker] = None
        self._worker_thread: Optional[QThread] = None

        # UI components
        self.window = MainWindow()
        self.sidebar = Sidebar()
        self.canvas_area = CanvasArea()
        self.timeline = Timeline()

        self._setup_layout()
        self._connect_signals()

    def _setup_layout(self):
        """Setup the main layout"""
        # Create content area (canvas + timeline)
        content = QWidget()
        content_layout = QVBoxLayout(content)
        content_layout.setContentsMargins(0, 0, 0, 0)
        content_layout.setSpacing(16)

        content_layout.addWidget(self.canvas_area, 1)
        content_layout.addWidget(self.timeline)

        # Add to main window
        self.window.add_sidebar(self.sidebar)
        self.window.add_content(content)

    def _connect_signals(self):
        """Connect all signals"""
        # Sidebar signals
        self.sidebar.open_video_clicked.connect(self._open_video)
        self.sidebar.open_batch_clicked.connect(self._open_batch)
        self.sidebar.add_zone_clicked.connect(self._show_add_zone_info)
        self.sidebar.clear_all_clicked.connect(self._clear_keyframes)
        self.sidebar.save_keyframes_clicked.connect(self._save_keyframes)
        self.sidebar.select_output_clicked.connect(self._select_output)
        self.sidebar.process_clicked.connect(self._start_processing)
        self.sidebar.preview_toggled.connect(self._toggle_preview)

        # Canvas signals
        self.canvas_area.zone_drawn.connect(self._on_zone_drawn)

        # Timeline signals
        self.timeline.frame_changed.connect(self._on_frame_change)
        self.timeline.keyframe_selected.connect(self._jump_to_keyframe)

    def run(self):
        """Start the application"""
        self.window.show()

    # ─────────────────────────────────────────────────────────────────
    # Video handling
    # ─────────────────────────────────────────────────────────────────

    def _open_video(self):
        """Open a video file"""
        path, _ = QFileDialog.getOpenFileName(
            self.window,
            "Select Video",
            "",
            "Video files (*.mp4 *.avi *.mov *.mkv *.webm);;All files (*.*)"
        )
        if path:
            self._load_video(path)

    def _load_video(self, path: str):
        """Load a video file"""
        if self.video.load(path):
            # Update UI
            self.sidebar.set_file_name(self.video.get_filename())
            self.canvas_area.set_info(self.video.get_info_string())
            self.timeline.set_total_frames(self.video.total_frames)
            self.timeline.set_current_frame(0)

            # Clear existing keyframes
            self.keyframes.clear()
            self._update_keyframe_list()

            # Try to load saved keyframes
            if self.keyframes.load_from_file(path):
                self._update_keyframe_list()

            # Display first frame
            self._update_display(0)
        else:
            self.window.show_message("Error", f"Could not load video: {path}", is_error=True)

    def _open_batch(self):
        """Open multiple videos for batch processing"""
        paths, _ = QFileDialog.getOpenFileNames(
            self.window,
            "Select Videos for Batch Processing",
            "",
            "Video files (*.mp4 *.avi *.mov *.mkv *.webm);;All files (*.*)"
        )
        if paths:
            self.batch_files = list(paths)
            self.window.show_message(
                "Batch",
                f"Added {len(self.batch_files)} videos to batch queue"
            )

    # ─────────────────────────────────────────────────────────────────
    # Display and navigation
    # ─────────────────────────────────────────────────────────────────

    def _update_display(self, frame_num: int = None):
        """Update the video display"""
        if not self.video.is_loaded:
            return

        if frame_num is None:
            frame_num = self.video.current_frame

        frame = self.video.get_frame(frame_num)
        if frame is not None:
            zones = self.keyframes.get_zones_at_frame(frame_num)
            self.canvas_area.set_frame(frame, zones)
            self.timeline.set_current_frame(frame_num)

    def _on_frame_change(self, frame: int):
        """Handle frame change from timeline"""
        self._update_display(frame)

    def _jump_to_keyframe(self, frame: int):
        """Jump to a keyframe"""
        self._update_display(frame)

    def _toggle_preview(self, visible: bool):
        """Toggle zone overlay visibility"""
        self.canvas_area.set_overlay_visible(visible)
        self._update_display()

    # ─────────────────────────────────────────────────────────────────
    # Zone management
    # ─────────────────────────────────────────────────────────────────

    def _on_zone_drawn(self, zone: tuple):
        """Handle a new zone being drawn"""
        self.keyframes.add_zone(self.video.current_frame, zone)
        self._update_keyframe_list()
        self._update_display()

    def _show_add_zone_info(self):
        """Show info about adding zones"""
        self.window.show_message(
            "Add Zone",
            "Draw a rectangle on the video to mark the watermark area.\n\n"
            "The zone will be applied from the current frame onwards until the next keyframe."
        )

    def _clear_keyframes(self):
        """Clear all keyframes"""
        if self.keyframes.is_empty:
            return

        if self.window.confirm_action("Clear All", "Remove all keyframe zones?"):
            self.keyframes.clear()
            self._update_keyframe_list()
            self._update_display()

    def _save_keyframes(self):
        """Save keyframes to file"""
        if not self.video.video_path:
            return

        save_path = self.keyframes.save_to_file(self.video.video_path)
        self.window.show_message("Saved", f"Keyframes saved to:\n{save_path}")

    def _update_keyframe_list(self):
        """Update the keyframe list display"""
        self.sidebar.set_keyframe_list(self.keyframes.get_summary())
        self.timeline.set_keyframes(self.keyframes.get_all_keyframe_numbers())

    # ─────────────────────────────────────────────────────────────────
    # Output and processing
    # ─────────────────────────────────────────────────────────────────

    def _select_output(self):
        """Select output folder"""
        path = QFileDialog.getExistingDirectory(
            self.window,
            "Select Output Folder",
            self.output_dir
        )
        if path:
            self.output_dir = path
            self.sidebar.set_output_path(path)

    def _start_processing(self):
        """Start video processing"""
        if not self.video.video_path:
            self.window.show_message("Error", "No video loaded", is_error=True)
            return

        if self.keyframes.is_empty:
            self.window.show_message(
                "Error",
                "No watermark zones defined.\nDraw rectangles on the watermark areas first.",
                is_error=True
            )
            return

        if self._processing:
            return

        # Create output directory
        os.makedirs(self.output_dir, exist_ok=True)

        # Generate output path
        output_path = os.path.join(
            self.output_dir,
            "clean_" + os.path.basename(self.video.video_path)
        )

        # Start processing
        self._processing = True
        self.sidebar.set_processing_enabled(False)
        self.sidebar.set_status("Processing...")

        # Create worker and thread
        self._worker = ProcessingWorker(
            self.video.video_path,
            output_path,
            self.keyframes.to_dict()
        )
        self._worker_thread = QThread()

        self._worker.moveToThread(self._worker_thread)
        self._worker_thread.started.connect(self._worker.run)
        self._worker.progress.connect(self._on_processing_progress)
        self._worker.finished.connect(self._on_processing_finished)
        self._worker.error.connect(self._on_processing_error)

        self._worker_thread.start()

    def _on_processing_progress(self, current: int, total: int):
        """Update processing progress"""
        self.sidebar.set_progress(current, total)
        self.sidebar.set_status(f"Processing frame {current}/{total}")

    def _on_processing_finished(self, output_path: str):
        """Handle processing completion"""
        self._cleanup_worker()
        self._processing = False
        self.sidebar.set_processing_enabled(True)
        self.sidebar.set_status(f"Done!")
        self.sidebar.set_progress(100, 100)
        self.window.show_message("Complete", f"Video saved to:\n{output_path}")

    def _on_processing_error(self, error: str):
        """Handle processing error"""
        self._cleanup_worker()
        self._processing = False
        self.sidebar.set_processing_enabled(True)
        self.sidebar.set_status(f"Error: {error}")
        self.window.show_message("Error", error, is_error=True)

    def _cleanup_worker(self):
        """Clean up worker thread"""
        if self._worker_thread:
            self._worker_thread.quit()
            self._worker_thread.wait()
            self._worker_thread = None
            self._worker = None


def main():
    """Main entry point when running as script"""
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
    stylesheet_path = Path(__file__).parent / "styles" / "stylesheet.qss"
    if stylesheet_path.exists():
        with open(stylesheet_path, "r", encoding="utf-8") as f:
            app.setStyleSheet(f.read())

    # Create and run application
    watermark_app = WatermarkRemoverApp()
    watermark_app.run()

    # Run event loop
    sys.exit(app.exec())


if __name__ == "__main__":
    main()
