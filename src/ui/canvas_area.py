"""
CanvasArea - Video display and drawing canvas
"""

import cv2
import numpy as np
from typing import Optional, Tuple, List

from PySide6.QtWidgets import QWidget, QVBoxLayout, QLabel, QGraphicsDropShadowEffect
from PySide6.QtCore import Qt, Signal, QPoint, QRect
from PySide6.QtGui import QPixmap, QImage, QPainter, QColor, QPen, QBrush, QFont

from ..styles.colors import Colors
from ..components.glass_panel import GlassPanel


class VideoCanvas(QWidget):
    """
    Canvas widget for video display with zone drawing capability.

    Features:
    - Video frame display
    - Mouse-based rectangle drawing
    - Zone overlay visualization
    """

    # Signals
    zone_drawn = Signal(tuple)  # (x1, y1, x2, y2) in video coordinates

    def __init__(self, parent=None):
        super().__init__(parent)

        # State
        self._current_pixmap: Optional[QPixmap] = None
        self._video_size: Tuple[int, int] = (0, 0)  # Original video dimensions
        self._display_scale: float = 1.0
        self._display_offset: Tuple[int, int] = (0, 0)  # Offset for centering

        # Drawing state
        self._drawing = False
        self._start_point: Optional[QPoint] = None
        self._current_point: Optional[QPoint] = None

        # Zone overlay
        self._zones: List[Tuple[int, int, int, int]] = []
        self._show_overlay = True

        self._setup_ui()

    def _setup_ui(self):
        """Setup the canvas"""
        self.setMinimumSize(400, 300)
        self.setStyleSheet(f"background-color: {Colors.CANVAS};")
        self.setCursor(Qt.CrossCursor)
        self.setMouseTracking(True)

    def set_frame(self, frame: np.ndarray, zones: List[Tuple[int, int, int, int]] = None):
        """
        Display a video frame.

        Args:
            frame: RGB numpy array
            zones: List of zone coordinates to overlay
        """
        if frame is None:
            return

        self._video_size = (frame.shape[1], frame.shape[0])
        self._zones = zones or []

        # Calculate display scale and offset
        self._calculate_display_params()

        # Resize frame for display
        display_width = int(self._video_size[0] * self._display_scale)
        display_height = int(self._video_size[1] * self._display_scale)
        display_frame = cv2.resize(frame, (display_width, display_height))

        # Draw zone overlay if enabled
        if self._show_overlay and self._zones:
            display_frame = self._draw_zones_on_frame(display_frame)

        # Convert to QPixmap
        height, width, channel = display_frame.shape
        bytes_per_line = 3 * width
        q_image = QImage(
            display_frame.data,
            width, height,
            bytes_per_line,
            QImage.Format_RGB888
        )
        self._current_pixmap = QPixmap.fromImage(q_image)

        self.update()

    def _calculate_display_params(self):
        """Calculate scale and offset for display"""
        if self._video_size[0] == 0 or self._video_size[1] == 0:
            return

        canvas_width = self.width()
        canvas_height = self.height()

        scale_x = canvas_width / self._video_size[0]
        scale_y = canvas_height / self._video_size[1]
        self._display_scale = min(scale_x, scale_y, 1.0)

        display_width = int(self._video_size[0] * self._display_scale)
        display_height = int(self._video_size[1] * self._display_scale)

        self._display_offset = (
            (canvas_width - display_width) // 2,
            (canvas_height - display_height) // 2
        )

    def _draw_zones_on_frame(self, frame: np.ndarray) -> np.ndarray:
        """Draw zone overlays on the frame"""
        for zone in self._zones:
            x1, y1, x2, y2 = zone
            # Scale coordinates
            sx1 = int(x1 * self._display_scale)
            sy1 = int(y1 * self._display_scale)
            sx2 = int(x2 * self._display_scale)
            sy2 = int(y2 * self._display_scale)

            # Draw semi-transparent orange rectangle
            overlay = frame.copy()
            cv2.rectangle(overlay, (sx1, sy1), (sx2, sy2), (255, 107, 53), -1)
            cv2.addWeighted(overlay, 0.3, frame, 0.7, 0, frame)
            cv2.rectangle(frame, (sx1, sy1), (sx2, sy2), (255, 107, 53), 2)

        return frame

    def _canvas_to_video_coords(self, point: QPoint) -> Tuple[int, int]:
        """Convert canvas coordinates to video coordinates"""
        x = int((point.x() - self._display_offset[0]) / self._display_scale)
        y = int((point.y() - self._display_offset[1]) / self._display_scale)

        # Clamp to video bounds
        x = max(0, min(x, self._video_size[0]))
        y = max(0, min(y, self._video_size[1]))

        return x, y

    def set_overlay_visible(self, visible: bool):
        """Toggle zone overlay visibility"""
        self._show_overlay = visible
        self.update()

    def paintEvent(self, event):
        """Paint the canvas"""
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)
        painter.setRenderHint(QPainter.SmoothPixmapTransform)

        # Draw background
        painter.fillRect(self.rect(), QColor(Colors.CANVAS))

        # Draw video frame
        if self._current_pixmap:
            painter.drawPixmap(
                self._display_offset[0],
                self._display_offset[1],
                self._current_pixmap
            )

        # Draw current drawing rectangle
        if self._drawing and self._start_point and self._current_point:
            pen = QPen(QColor(255, 107, 53), 2, Qt.SolidLine)
            painter.setPen(pen)
            brush = QBrush(QColor(255, 107, 53, 50))
            painter.setBrush(brush)

            rect = QRect(self._start_point, self._current_point).normalized()
            painter.drawRect(rect)

        # Draw "No video" message if no frame
        if not self._current_pixmap:
            painter.setPen(QColor(Colors.TEXT_TERTIARY))
            font = QFont()
            font.setPointSize(14)
            painter.setFont(font)
            painter.drawText(self.rect(), Qt.AlignCenter, "No video loaded\nOpen a video to start")

    def mousePressEvent(self, event):
        """Start drawing rectangle"""
        if event.button() == Qt.LeftButton and self._current_pixmap:
            self._drawing = True
            self._start_point = event.pos()
            self._current_point = event.pos()

    def mouseMoveEvent(self, event):
        """Update drawing rectangle"""
        if self._drawing:
            self._current_point = event.pos()
            self.update()

    def mouseReleaseEvent(self, event):
        """Finish drawing rectangle"""
        if event.button() == Qt.LeftButton and self._drawing:
            self._drawing = False

            if self._start_point and self._current_point:
                # Convert to video coordinates
                x1, y1 = self._canvas_to_video_coords(self._start_point)
                x2, y2 = self._canvas_to_video_coords(self._current_point)

                # Ensure x1 < x2 and y1 < y2
                x1, x2 = min(x1, x2), max(x1, x2)
                y1, y2 = min(y1, y2), max(y1, y2)

                # Only emit if rectangle is valid size
                if abs(x2 - x1) > 5 and abs(y2 - y1) > 5:
                    self.zone_drawn.emit((x1, y1, x2, y2))

            self._start_point = None
            self._current_point = None
            self.update()

    def resizeEvent(self, event):
        """Handle resize"""
        super().resizeEvent(event)
        self._calculate_display_params()


class CanvasArea(GlassPanel):
    """
    Container for video canvas with info label.
    """

    # Expose canvas signals
    zone_drawn = Signal(tuple)

    def __init__(self, parent=None):
        super().__init__(parent, hover_effect=False)

        self._setup_ui()

    def _setup_ui(self):
        """Build the canvas area UI"""
        layout = QVBoxLayout(self)
        layout.setContentsMargins(12, 12, 12, 12)
        layout.setSpacing(12)

        # Video canvas
        self.canvas = VideoCanvas()
        self.canvas.zone_drawn.connect(self.zone_drawn.emit)

        # Add glow border effect
        shadow = QGraphicsDropShadowEffect()
        shadow.setBlurRadius(20)
        shadow.setColor(QColor(255, 107, 53, 30))
        shadow.setOffset(0, 0)
        self.canvas.setGraphicsEffect(shadow)

        layout.addWidget(self.canvas, 1)

        # Video info label
        self.info_label = QLabel("No video loaded")
        self.info_label.setAlignment(Qt.AlignCenter)
        self.info_label.setStyleSheet(f"""
            color: {Colors.TEXT_TERTIARY};
            font-size: 12px;
            padding: 4px;
        """)
        layout.addWidget(self.info_label)

    def set_frame(self, frame: np.ndarray, zones: list = None):
        """Display a video frame"""
        self.canvas.set_frame(frame, zones)

    def set_info(self, info: str):
        """Update the info label"""
        self.info_label.setText(info)
        self.info_label.setStyleSheet(f"""
            color: {Colors.TEXT_SECONDARY if info != "No video loaded" else Colors.TEXT_TERTIARY};
            font-size: 12px;
            padding: 4px;
        """)

    def set_overlay_visible(self, visible: bool):
        """Toggle zone overlay"""
        self.canvas.set_overlay_visible(visible)
