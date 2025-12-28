"""
IconButton - Button with icon and hover animation
"""

from PySide6.QtWidgets import QPushButton, QGraphicsDropShadowEffect
from PySide6.QtCore import Qt, QPropertyAnimation, QEasingCurve, Property, QSize
from PySide6.QtGui import QColor, QIcon, QPainter, QPen, QBrush
from PySide6.QtSvg import QSvgRenderer

from ..styles.colors import Colors


class IconButton(QPushButton):
    """
    Circular icon button with:
    - Transparent background
    - Hover highlight
    - Optional glow effect
    """

    def __init__(self, icon_path: str = None, tooltip: str = "", parent=None, size: int = 44):
        super().__init__(parent)

        self._size = size
        self._bg_opacity = 0

        self.setFixedSize(size, size)
        self.setToolTip(tooltip)
        self.setCursor(Qt.PointingHandCursor)

        if icon_path:
            self.setIcon(QIcon(icon_path))
            self.setIconSize(QSize(size - 16, size - 16))

        self._setup_style()
        self._setup_animations()

    def _setup_style(self):
        """Apply button styling"""
        self.setObjectName("iconButton")
        self.setStyleSheet(f"""
            #iconButton {{
                background-color: transparent;
                border: none;
                border-radius: {self._size // 2}px;
            }}
            #iconButton:hover {{
                background-color: rgba(255, 255, 255, 0.1);
            }}
            #iconButton:pressed {{
                background-color: rgba(255, 255, 255, 0.05);
            }}
        """)

    def _setup_animations(self):
        """Setup hover animation"""
        self._bg_anim = QPropertyAnimation(self, b"bgOpacity")
        self._bg_anim.setDuration(Colors.ANIM_FAST)
        self._bg_anim.setEasingCurve(QEasingCurve.OutCubic)

    # Property for background opacity animation
    def _get_bg_opacity(self) -> float:
        return self._bg_opacity

    def _set_bg_opacity(self, value: float):
        self._bg_opacity = value
        self.update()

    bgOpacity = Property(float, _get_bg_opacity, _set_bg_opacity)

    def enterEvent(self, event):
        self._bg_anim.stop()
        self._bg_anim.setStartValue(self._bg_opacity)
        self._bg_anim.setEndValue(0.1)
        self._bg_anim.start()
        super().enterEvent(event)

    def leaveEvent(self, event):
        self._bg_anim.stop()
        self._bg_anim.setStartValue(self._bg_opacity)
        self._bg_anim.setEndValue(0)
        self._bg_anim.start()
        super().leaveEvent(event)


class NavigationButton(QPushButton):
    """Navigation button for timeline controls"""

    def __init__(self, text: str, parent=None):
        super().__init__(text, parent)
        self._setup_style()

    def _setup_style(self):
        self.setObjectName("navButton")
        self.setCursor(Qt.PointingHandCursor)
        self.setMinimumWidth(50)
        self.setMinimumHeight(36)

        self.setStyleSheet(f"""
            #navButton {{
                background-color: rgba(255, 255, 255, 0.08);
                border: 1px solid rgba(255, 255, 255, 0.1);
                border-radius: 8px;
                color: white;
                font-weight: 500;
                font-size: 12px;
                padding: 8px 12px;
            }}
            #navButton:hover {{
                background-color: rgba(255, 255, 255, 0.12);
                border: 1px solid rgba(255, 255, 255, 0.15);
            }}
            #navButton:pressed {{
                background-color: rgba(255, 107, 53, 0.2);
                border: 1px solid rgba(255, 107, 53, 0.3);
            }}
        """)


class FloatingActionButton(QPushButton):
    """
    Large floating action button (FAB) for primary actions
    """

    def __init__(self, text: str, parent=None):
        super().__init__(text, parent)

        self._glow_radius = 0

        self._setup_style()
        self._setup_shadow()
        self._setup_animations()

    def _setup_style(self):
        self.setObjectName("fab")
        self.setCursor(Qt.PointingHandCursor)
        self.setMinimumHeight(56)
        self.setMinimumWidth(200)

        self.setStyleSheet(f"""
            #fab {{
                background: {Colors.get_gradient_css()};
                border: none;
                border-radius: 28px;
                color: white;
                font-weight: 700;
                font-size: 15px;
                padding: 16px 32px;
            }}
            #fab:hover {{
                background: {Colors.get_hover_gradient_css()};
            }}
            #fab:pressed {{
                background: {Colors.get_pressed_gradient_css()};
            }}
            #fab:disabled {{
                background: rgba(255, 107, 53, 0.3);
                color: rgba(255, 255, 255, 0.5);
            }}
        """)

    def _setup_shadow(self):
        self._shadow = QGraphicsDropShadowEffect(self)
        self._shadow.setBlurRadius(20)
        self._shadow.setColor(QColor(255, 107, 53, 100))
        self._shadow.setOffset(0, 4)
        self.setGraphicsEffect(self._shadow)

    def _setup_animations(self):
        self._glow_anim = QPropertyAnimation(self, b"glowRadius")
        self._glow_anim.setDuration(Colors.ANIM_NORMAL)
        self._glow_anim.setEasingCurve(QEasingCurve.OutCubic)

    def _get_glow_radius(self) -> float:
        return self._glow_radius

    def _set_glow_radius(self, value: float):
        self._glow_radius = value
        if hasattr(self, '_shadow'):
            self._shadow.setBlurRadius(20 + value)

    glowRadius = Property(float, _get_glow_radius, _set_glow_radius)

    def enterEvent(self, event):
        self._glow_anim.stop()
        self._glow_anim.setStartValue(self._glow_radius)
        self._glow_anim.setEndValue(15)
        self._glow_anim.start()
        super().enterEvent(event)

    def leaveEvent(self, event):
        self._glow_anim.stop()
        self._glow_anim.setStartValue(self._glow_radius)
        self._glow_anim.setEndValue(0)
        self._glow_anim.start()
        super().leaveEvent(event)
