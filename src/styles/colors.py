"""
Color System - Glassmorphism Dark Theme with Orange Accents
"""

class Colors:
    """Design tokens for the glassmorphism UI"""

    # ═══════════════════════════════════════════════════════════════
    # BASE COLORS (Dark Grays)
    # ═══════════════════════════════════════════════════════════════
    BG_PRIMARY = "#1a1a2e"      # Main background
    BG_SECONDARY = "#16213e"    # Sidebar/cards background
    BG_TERTIARY = "#0f3460"     # Elevated surfaces
    SURFACE = "#1f1f3a"         # Card surfaces
    CANVAS = "#0d0d1a"          # Video canvas background

    # ═══════════════════════════════════════════════════════════════
    # GLASS EFFECTS
    # ═══════════════════════════════════════════════════════════════
    GLASS_BG = "rgba(26, 26, 46, 0.75)"
    GLASS_BG_HOVER = "rgba(31, 31, 58, 0.85)"
    GLASS_BORDER = "rgba(255, 255, 255, 0.1)"
    GLASS_BORDER_HOVER = "rgba(255, 255, 255, 0.15)"
    GLASS_HIGHLIGHT = "rgba(255, 255, 255, 0.05)"

    # ═══════════════════════════════════════════════════════════════
    # ACCENT COLORS (Orange)
    # ═══════════════════════════════════════════════════════════════
    ACCENT = "#ff6b35"           # Primary orange
    ACCENT_SECONDARY = "#f7931e" # Secondary/gradient end
    ACCENT_LIGHT = "#ff8555"     # Hover state
    ACCENT_DARK = "#e55525"      # Pressed state
    ACCENT_GLOW = "rgba(255, 107, 53, 0.4)"
    ACCENT_GLOW_STRONG = "rgba(255, 107, 53, 0.6)"

    # ═══════════════════════════════════════════════════════════════
    # TEXT HIERARCHY
    # ═══════════════════════════════════════════════════════════════
    TEXT_PRIMARY = "#ffffff"     # Headlines, important text
    TEXT_SECONDARY = "#b0b0c0"   # Body text
    TEXT_TERTIARY = "#6c6c8a"    # Muted/labels
    TEXT_ACCENT = "#ff6b35"      # Highlighted text
    TEXT_DISABLED = "#4a4a5a"    # Disabled state

    # ═══════════════════════════════════════════════════════════════
    # STATE COLORS
    # ═══════════════════════════════════════════════════════════════
    SUCCESS = "#4ade80"
    SUCCESS_BG = "rgba(74, 222, 128, 0.15)"
    SUCCESS_GLOW = "rgba(74, 222, 128, 0.4)"

    ERROR = "#ef4444"
    ERROR_BG = "rgba(239, 68, 68, 0.15)"
    ERROR_GLOW = "rgba(239, 68, 68, 0.4)"

    WARNING = "#fbbf24"
    WARNING_BG = "rgba(251, 191, 36, 0.15)"

    # ═══════════════════════════════════════════════════════════════
    # ZONE OVERLAY (for watermark marking)
    # ═══════════════════════════════════════════════════════════════
    ZONE_FILL = "rgba(255, 107, 53, 0.3)"
    ZONE_BORDER = "#ff6b35"
    ZONE_BORDER_WIDTH = 2

    # ═══════════════════════════════════════════════════════════════
    # COMPONENT DIMENSIONS
    # ═══════════════════════════════════════════════════════════════
    BORDER_RADIUS_SM = 8
    BORDER_RADIUS_MD = 12
    BORDER_RADIUS_LG = 16
    BORDER_RADIUS_XL = 20
    BORDER_RADIUS_FULL = 9999

    # ═══════════════════════════════════════════════════════════════
    # SPACING
    # ═══════════════════════════════════════════════════════════════
    SPACING_XS = 4
    SPACING_SM = 8
    SPACING_MD = 16
    SPACING_LG = 24
    SPACING_XL = 32
    SPACING_2XL = 48

    # ═══════════════════════════════════════════════════════════════
    # ANIMATION DURATIONS (ms)
    # ═══════════════════════════════════════════════════════════════
    ANIM_FAST = 100
    ANIM_NORMAL = 200
    ANIM_SLOW = 300
    ANIM_LOADING = 1000

    # ═══════════════════════════════════════════════════════════════
    # SHADOWS
    # ═══════════════════════════════════════════════════════════════
    SHADOW_COLOR = "rgba(0, 0, 0, 0.3)"
    SHADOW_GLOW_COLOR = "rgba(255, 107, 53, 0.25)"

    @staticmethod
    def get_gradient_css(direction: str = "horizontal") -> str:
        """Get CSS gradient for orange accent"""
        if direction == "horizontal":
            return f"qlineargradient(x1:0, y1:0, x2:1, y2:0, stop:0 {Colors.ACCENT}, stop:1 {Colors.ACCENT_SECONDARY})"
        else:
            return f"qlineargradient(x1:0, y1:0, x2:0, y2:1, stop:0 {Colors.ACCENT}, stop:1 {Colors.ACCENT_SECONDARY})"

    @staticmethod
    def get_hover_gradient_css() -> str:
        """Get CSS gradient for hover state"""
        return f"qlineargradient(x1:0, y1:0, x2:1, y2:0, stop:0 {Colors.ACCENT_LIGHT}, stop:1 #ffaa3e)"

    @staticmethod
    def get_pressed_gradient_css() -> str:
        """Get CSS gradient for pressed state"""
        return f"qlineargradient(x1:0, y1:0, x2:1, y2:0, stop:0 {Colors.ACCENT_DARK}, stop:1 #d7810e)"
