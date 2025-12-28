"""
GlassPanel - Glassmorphism styled container widget
"""

from PySide6.QtWidgets import QFrame, QVBoxLayout, QGraphicsDropShadowEffect
from PySide6.QtCore import Qt, QPropertyAnimation, QEasingCurve, Property
from PySide6.QtGui import QColor

from ..styles.colors import Colors


class GlassPanel(QFrame):
    """
    A glassmorphism styled panel with:
    - Semi-transparent background
    - Subtle border glow
    - Rounded corners
    - Hover animation (lift effect)
    """

    def __init__(self, parent=None, hover_effect: bool = True, border_radius: int = None):
        super().__init__(parent)

        self._hover_effect = hover_effect
        self._border_radius = border_radius or Colors.BORDER_RADIUS_LG
        self._shadow_blur = 0

        self._setup_style()
        if hover_effect:
            self._setup_shadow()
            self._setup_animations()

    def _setup_style(self):
        """Apply glassmorphism styling"""
        self.setObjectName("glassPanel")
        self.setStyleSheet(f"""
            #glassPanel {{
                background-color: {Colors.GLASS_BG};
                border: 1px solid {Colors.GLASS_BORDER};
                border-radius: {self._border_radius}px;
            }}
            #glassPanel:hover {{
                background-color: {Colors.GLASS_BG_HOVER};
                border: 1px solid {Colors.GLASS_BORDER_HOVER};
            }}
        """)

    def _setup_shadow(self):
        """Setup drop shadow effect for hover"""
        self._shadow = QGraphicsDropShadowEffect(self)
        self._shadow.setBlurRadius(0)
        self._shadow.setColor(QColor(0, 0, 0, 50))
        self._shadow.setOffset(0, 0)
        self.setGraphicsEffect(self._shadow)

    def _setup_animations(self):
        """Setup hover animations"""
        self._shadow_anim = QPropertyAnimation(self, b"shadowBlur")
        self._shadow_anim.setDuration(Colors.ANIM_NORMAL)
        self._shadow_anim.setEasingCurve(QEasingCurve.OutCubic)

    # Property for animating shadow blur
    def _get_shadow_blur(self) -> float:
        return self._shadow_blur

    def _set_shadow_blur(self, value: float):
        self._shadow_blur = value
        if hasattr(self, '_shadow'):
            self._shadow.setBlurRadius(value)
            self._shadow.setOffset(0, value / 4)

    shadowBlur = Property(float, _get_shadow_blur, _set_shadow_blur)

    def enterEvent(self, event):
        """Mouse enter - lift effect"""
        if self._hover_effect and hasattr(self, '_shadow_anim'):
            self._shadow_anim.stop()
            self._shadow_anim.setStartValue(self._shadow_blur)
            self._shadow_anim.setEndValue(20)
            self._shadow_anim.start()
        super().enterEvent(event)

    def leaveEvent(self, event):
        """Mouse leave - lower effect"""
        if self._hover_effect and hasattr(self, '_shadow_anim'):
            self._shadow_anim.stop()
            self._shadow_anim.setStartValue(self._shadow_blur)
            self._shadow_anim.setEndValue(0)
            self._shadow_anim.start()
        super().leaveEvent(event)


class GlassCard(GlassPanel):
    """
    Smaller variant of GlassPanel for card-like containers
    """

    def __init__(self, parent=None, hover_effect: bool = True):
        super().__init__(
            parent,
            hover_effect=hover_effect,
            border_radius=Colors.BORDER_RADIUS_MD
        )
        self._setup_card_style()

    def _setup_card_style(self):
        """Apply card-specific styling"""
        self.setObjectName("glassCard")
        self.setStyleSheet(f"""
            #glassCard {{
                background-color: rgba(31, 31, 58, 0.6);
                border: 1px solid rgba(255, 255, 255, 0.08);
                border-radius: {Colors.BORDER_RADIUS_MD}px;
            }}
            #glassCard:hover {{
                background-color: rgba(31, 31, 58, 0.8);
                border: 1px solid rgba(255, 255, 255, 0.12);
            }}
        """)
