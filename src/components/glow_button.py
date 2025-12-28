"""
GlowButton - Animated button with glow effect
"""

from PySide6.QtWidgets import QPushButton, QGraphicsDropShadowEffect
from PySide6.QtCore import Qt, QPropertyAnimation, QEasingCurve, Property, QSize
from PySide6.QtGui import QColor, QFont

from ..styles.colors import Colors


class GlowButton(QPushButton):
    """
    Modern button with:
    - Orange gradient background
    - Animated glow on hover
    - Press scale animation
    - Smooth color transitions
    """

    def __init__(self, text: str, parent=None, primary: bool = True):
        super().__init__(text, parent)

        self._primary = primary
        self._glow_radius = 0
        self._scale = 1.0

        self._setup_style()
        self._setup_shadow()
        self._setup_animations()

    def _setup_style(self):
        """Apply button styling"""
        self.setObjectName("glowButton")
        self.setCursor(Qt.PointingHandCursor)
        self.setMinimumHeight(44)
        self.setMinimumWidth(80)

        font = self.font()
        font.setWeight(QFont.DemiBold)
        font.setPointSize(11)
        self.setFont(font)

        if self._primary:
            self.setStyleSheet(f"""
                #glowButton {{
                    background: {Colors.get_gradient_css()};
                    border: none;
                    border-radius: {Colors.BORDER_RADIUS_SM + 2}px;
                    color: white;
                    padding: 12px 24px;
                }}
                #glowButton:hover {{
                    background: {Colors.get_hover_gradient_css()};
                }}
                #glowButton:pressed {{
                    background: {Colors.get_pressed_gradient_css()};
                }}
                #glowButton:disabled {{
                    background: rgba(255, 107, 53, 0.3);
                    color: rgba(255, 255, 255, 0.5);
                }}
            """)
        else:
            self.setStyleSheet(f"""
                #glowButton {{
                    background-color: rgba(255, 255, 255, 0.08);
                    border: 1px solid rgba(255, 255, 255, 0.12);
                    border-radius: {Colors.BORDER_RADIUS_SM + 2}px;
                    color: white;
                    padding: 12px 24px;
                }}
                #glowButton:hover {{
                    background-color: rgba(255, 255, 255, 0.12);
                    border: 1px solid rgba(255, 255, 255, 0.18);
                }}
                #glowButton:pressed {{
                    background-color: rgba(255, 255, 255, 0.06);
                }}
            """)

    def _setup_shadow(self):
        """Setup glow shadow effect"""
        self._shadow = QGraphicsDropShadowEffect(self)
        self._shadow.setBlurRadius(0)
        self._shadow.setColor(QColor(255, 107, 53, 150))
        self._shadow.setOffset(0, 0)
        self.setGraphicsEffect(self._shadow)

    def _setup_animations(self):
        """Setup hover and press animations"""
        # Glow animation
        self._glow_anim = QPropertyAnimation(self, b"glowRadius")
        self._glow_anim.setDuration(Colors.ANIM_NORMAL)
        self._glow_anim.setEasingCurve(QEasingCurve.OutCubic)

    # Property for animating glow
    def _get_glow_radius(self) -> float:
        return self._glow_radius

    def _set_glow_radius(self, value: float):
        self._glow_radius = value
        if hasattr(self, '_shadow'):
            self._shadow.setBlurRadius(value)

    glowRadius = Property(float, _get_glow_radius, _set_glow_radius)

    def enterEvent(self, event):
        """Mouse enter - grow glow"""
        if self._primary:
            self._glow_anim.stop()
            self._glow_anim.setStartValue(self._glow_radius)
            self._glow_anim.setEndValue(25)
            self._glow_anim.start()
        super().enterEvent(event)

    def leaveEvent(self, event):
        """Mouse leave - shrink glow"""
        if self._primary:
            self._glow_anim.stop()
            self._glow_anim.setStartValue(self._glow_radius)
            self._glow_anim.setEndValue(0)
            self._glow_anim.start()
        super().leaveEvent(event)


class DangerButton(QPushButton):
    """Red danger button for destructive actions"""

    def __init__(self, text: str, parent=None):
        super().__init__(text, parent)
        self._setup_style()

    def _setup_style(self):
        self.setObjectName("dangerButton")
        self.setCursor(Qt.PointingHandCursor)
        self.setMinimumHeight(40)

        self.setStyleSheet(f"""
            #dangerButton {{
                background-color: {Colors.ERROR_BG};
                border: 1px solid rgba(239, 68, 68, 0.3);
                border-radius: {Colors.BORDER_RADIUS_SM + 2}px;
                color: {Colors.ERROR};
                padding: 10px 20px;
                font-weight: 500;
            }}
            #dangerButton:hover {{
                background-color: rgba(239, 68, 68, 0.25);
                border: 1px solid rgba(239, 68, 68, 0.4);
            }}
            #dangerButton:pressed {{
                background-color: rgba(239, 68, 68, 0.35);
            }}
        """)


class SuccessButton(GlowButton):
    """Green success button"""

    def __init__(self, text: str, parent=None):
        super().__init__(text, parent, primary=True)
        self._setup_success_style()

    def _setup_success_style(self):
        self._shadow.setColor(QColor(74, 222, 128, 150))
        self.setStyleSheet(f"""
            #glowButton {{
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                    stop:0 #22c55e, stop:1 #4ade80);
                border: none;
                border-radius: {Colors.BORDER_RADIUS_SM + 2}px;
                color: white;
                padding: 12px 24px;
            }}
            #glowButton:hover {{
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                    stop:0 #16a34a, stop:1 #22c55e);
            }}
            #glowButton:pressed {{
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                    stop:0 #15803d, stop:1 #16a34a);
            }}
        """)
