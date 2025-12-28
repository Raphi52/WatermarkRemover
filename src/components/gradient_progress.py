"""
GradientProgressBar - Animated progress bar with gradient fill
"""

from PySide6.QtWidgets import QProgressBar, QGraphicsDropShadowEffect, QWidget, QHBoxLayout, QLabel
from PySide6.QtCore import Qt, QPropertyAnimation, QEasingCurve, Property, QTimer
from PySide6.QtGui import QColor, QPainter, QLinearGradient, QBrush, QPen

from ..styles.colors import Colors


class GradientProgressBar(QProgressBar):
    """
    Custom progress bar with:
    - Orange gradient fill
    - Animated shimmer effect
    - Rounded ends
    - Glow effect when active
    """

    def __init__(self, parent=None):
        super().__init__(parent)

        self._shimmer_offset = 0
        self._glow_intensity = 0
        self._is_animating = False

        self._setup_style()
        self._setup_animations()

    def _setup_style(self):
        """Apply progress bar styling"""
        self.setObjectName("gradientProgress")
        self.setTextVisible(False)
        self.setMinimumHeight(12)
        self.setMaximumHeight(12)

        self.setStyleSheet(f"""
            #gradientProgress {{
                background-color: rgba(26, 26, 46, 0.5);
                border: 1px solid rgba(255, 255, 255, 0.1);
                border-radius: 6px;
            }}
            #gradientProgress::chunk {{
                background: {Colors.get_gradient_css()};
                border-radius: 5px;
            }}
        """)

    def _setup_animations(self):
        """Setup shimmer animation"""
        self._shimmer_timer = QTimer(self)
        self._shimmer_timer.timeout.connect(self._update_shimmer)

        # Glow animation
        self._glow_anim = QPropertyAnimation(self, b"glowIntensity")
        self._glow_anim.setDuration(300)
        self._glow_anim.setEasingCurve(QEasingCurve.OutCubic)

    def _update_shimmer(self):
        """Update shimmer position"""
        self._shimmer_offset = (self._shimmer_offset + 5) % 200
        self.update()

    # Property for glow intensity
    def _get_glow_intensity(self) -> float:
        return self._glow_intensity

    def _set_glow_intensity(self, value: float):
        self._glow_intensity = value
        self.update()

    glowIntensity = Property(float, _get_glow_intensity, _set_glow_intensity)

    def setValue(self, value: int):
        """Override setValue to trigger animations"""
        old_value = self.value()
        super().setValue(value)

        # Start/stop shimmer based on progress
        if value > 0 and value < self.maximum():
            if not self._shimmer_timer.isActive():
                self._shimmer_timer.start(50)
                self._glow_anim.setStartValue(0)
                self._glow_anim.setEndValue(15)
                self._glow_anim.start()
        else:
            if self._shimmer_timer.isActive():
                self._shimmer_timer.stop()
                self._glow_anim.setStartValue(self._glow_intensity)
                self._glow_anim.setEndValue(0)
                self._glow_anim.start()


class ProgressWithLabel(QWidget):
    """Progress bar with status label"""

    def __init__(self, parent=None):
        super().__init__(parent)

        self._progress = GradientProgressBar(self)
        self._label = QLabel("Ready", self)
        self._label.setObjectName("progressLabel")
        self._label.setStyleSheet(f"""
            #progressLabel {{
                color: {Colors.TEXT_TERTIARY};
                font-size: 12px;
            }}
        """)

        layout = QHBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(12)
        layout.addWidget(self._progress, 1)
        layout.addWidget(self._label)

    def setValue(self, value: int):
        self._progress.setValue(value)

    def setMaximum(self, value: int):
        self._progress.setMaximum(value)

    def setStatus(self, text: str):
        self._label.setText(text)

    def setProgress(self, current: int, total: int, status: str = None):
        """Convenience method to set progress and status"""
        self._progress.setMaximum(total)
        self._progress.setValue(current)
        if status:
            self._label.setText(status)
        else:
            percent = int(current / total * 100) if total > 0 else 0
            self._label.setText(f"{percent}%")


class LoadingSpinner(QWidget):
    """Animated loading spinner with pulsing glow"""

    def __init__(self, parent=None, size: int = 40):
        super().__init__(parent)

        self._size = size
        self._angle = 0
        self._glow = 10

        self.setFixedSize(size, size)

        self._timer = QTimer(self)
        self._timer.timeout.connect(self._animate)

        self._glow_anim = QPropertyAnimation(self, b"glowRadius")
        self._glow_anim.setDuration(1000)
        self._glow_anim.setLoopCount(-1)
        self._glow_anim.setStartValue(8)
        self._glow_anim.setEndValue(20)

    def start(self):
        """Start the spinner animation"""
        self._timer.start(16)  # ~60fps
        self._glow_anim.start()
        self.show()

    def stop(self):
        """Stop the spinner animation"""
        self._timer.stop()
        self._glow_anim.stop()
        self.hide()

    def _animate(self):
        self._angle = (self._angle + 6) % 360
        self.update()

    def _get_glow_radius(self) -> float:
        return self._glow

    def _set_glow_radius(self, value: float):
        self._glow = value
        self.update()

    glowRadius = Property(float, _get_glow_radius, _set_glow_radius)

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)

        center = self._size // 2
        radius = self._size // 2 - 4

        # Draw glow
        glow_color = QColor(255, 107, 53, 50)
        for i in range(int(self._glow)):
            painter.setPen(QPen(glow_color, 3))
            painter.drawArc(
                center - radius - i, center - radius - i,
                (radius + i) * 2, (radius + i) * 2,
                self._angle * 16, 90 * 16
            )

        # Draw arc
        gradient = QLinearGradient(0, 0, self._size, self._size)
        gradient.setColorAt(0, QColor(255, 107, 53))
        gradient.setColorAt(1, QColor(247, 147, 30))

        pen = QPen(QBrush(gradient), 4)
        pen.setCapStyle(Qt.RoundCap)
        painter.setPen(pen)

        painter.drawArc(
            center - radius, center - radius,
            radius * 2, radius * 2,
            self._angle * 16, 90 * 16
        )
