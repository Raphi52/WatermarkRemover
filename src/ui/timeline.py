"""
Timeline - Video navigation controls
"""

from typing import List

from PySide6.QtWidgets import (
    QWidget, QHBoxLayout, QVBoxLayout, QLabel,
    QSlider, QComboBox
)
from PySide6.QtCore import Qt, Signal

from ..styles.colors import Colors
from ..components.glass_panel import GlassPanel
from ..components.icon_button import NavigationButton


class Timeline(GlassPanel):
    """
    Bottom timeline controls with:
    - Timeline slider
    - Frame navigation buttons
    - Frame counter
    - Keyframe quick jump
    """

    # Signals
    frame_changed = Signal(int)
    keyframe_selected = Signal(int)

    def __init__(self, parent=None):
        super().__init__(parent, hover_effect=False)

        self._total_frames = 0
        self._current_frame = 0

        self._setup_ui()

    def _setup_ui(self):
        """Build the timeline UI"""
        layout = QVBoxLayout(self)
        layout.setContentsMargins(16, 12, 16, 12)
        layout.setSpacing(12)

        # Timeline slider
        self.slider = QSlider(Qt.Horizontal)
        self.slider.setMinimum(0)
        self.slider.setMaximum(100)
        self.slider.setValue(0)
        self.slider.valueChanged.connect(self._on_slider_change)
        self.slider.setStyleSheet(f"""
            QSlider::groove:horizontal {{
                background-color: rgba(255, 255, 255, 0.1);
                height: 8px;
                border-radius: 4px;
            }}
            QSlider::handle:horizontal {{
                background: {Colors.get_gradient_css()};
                width: 20px;
                height: 20px;
                margin: -6px 0;
                border-radius: 10px;
                border: 2px solid white;
            }}
            QSlider::handle:horizontal:hover {{
                background: {Colors.get_hover_gradient_css()};
                width: 22px;
                height: 22px;
                margin: -7px 0;
                border-radius: 11px;
            }}
            QSlider::sub-page:horizontal {{
                background: {Colors.get_gradient_css()};
                border-radius: 4px;
            }}
            QSlider::add-page:horizontal {{
                background-color: rgba(255, 255, 255, 0.1);
                border-radius: 4px;
            }}
        """)
        layout.addWidget(self.slider)

        # Controls row
        controls_layout = QHBoxLayout()
        controls_layout.setSpacing(8)

        # Navigation buttons
        self.btn_back_10 = NavigationButton("<< -10")
        self.btn_back_10.clicked.connect(lambda: self._jump_frames(-10))
        controls_layout.addWidget(self.btn_back_10)

        self.btn_back_1 = NavigationButton("< -1")
        self.btn_back_1.clicked.connect(lambda: self._jump_frames(-1))
        controls_layout.addWidget(self.btn_back_1)

        # Frame label
        self.frame_label = QLabel("Frame: 0 / 0")
        self.frame_label.setStyleSheet(f"""
            color: {Colors.TEXT_PRIMARY};
            font-size: 13px;
            font-weight: 500;
            padding: 0 16px;
        """)
        self.frame_label.setMinimumWidth(150)
        self.frame_label.setAlignment(Qt.AlignCenter)
        controls_layout.addWidget(self.frame_label)

        self.btn_forward_1 = NavigationButton("+1 >")
        self.btn_forward_1.clicked.connect(lambda: self._jump_frames(1))
        controls_layout.addWidget(self.btn_forward_1)

        self.btn_forward_10 = NavigationButton("+10 >>")
        self.btn_forward_10.clicked.connect(lambda: self._jump_frames(10))
        controls_layout.addWidget(self.btn_forward_10)

        # Spacer
        controls_layout.addStretch()

        # Keyframe jump
        separator = QLabel("|")
        separator.setStyleSheet(f"color: {Colors.TEXT_TERTIARY}; padding: 0 8px;")
        controls_layout.addWidget(separator)

        jump_label = QLabel("Jump to keyframe:")
        jump_label.setStyleSheet(f"color: {Colors.TEXT_SECONDARY}; font-size: 12px;")
        controls_layout.addWidget(jump_label)

        self.keyframe_combo = QComboBox()
        self.keyframe_combo.addItem("None")
        self.keyframe_combo.setMinimumWidth(100)
        self.keyframe_combo.currentTextChanged.connect(self._on_keyframe_selected)
        self.keyframe_combo.setStyleSheet(f"""
            QComboBox {{
                background-color: rgba(255, 255, 255, 0.05);
                border: 1px solid rgba(255, 255, 255, 0.1);
                border-radius: 8px;
                color: white;
                padding: 6px 12px;
                font-size: 12px;
                min-height: 16px;
            }}
            QComboBox:hover {{
                border: 1px solid rgba(255, 255, 255, 0.2);
            }}
            QComboBox::drop-down {{
                border: none;
                padding-right: 8px;
            }}
            QComboBox::down-arrow {{
                border-left: 4px solid transparent;
                border-right: 4px solid transparent;
                border-top: 5px solid {Colors.TEXT_SECONDARY};
            }}
            QComboBox QAbstractItemView {{
                background-color: {Colors.SURFACE};
                border: 1px solid rgba(255, 255, 255, 0.1);
                border-radius: 8px;
                color: white;
                selection-background-color: rgba(255, 107, 53, 0.3);
                padding: 4px;
            }}
        """)
        controls_layout.addWidget(self.keyframe_combo)

        layout.addLayout(controls_layout)

    def _on_slider_change(self, value: int):
        """Handle slider value change"""
        self._current_frame = value
        self._update_frame_label()
        self.frame_changed.emit(value)

    def _jump_frames(self, delta: int):
        """Jump forward or backward by frames"""
        new_frame = max(0, min(self._total_frames - 1, self._current_frame + delta))
        self.slider.setValue(new_frame)

    def _on_keyframe_selected(self, text: str):
        """Handle keyframe dropdown selection"""
        if text != "None":
            try:
                frame = int(text)
                self.keyframe_selected.emit(frame)
                self.slider.setValue(frame)
            except ValueError:
                pass

    def _update_frame_label(self):
        """Update the frame counter label"""
        max_frame = max(0, self._total_frames - 1)
        self.frame_label.setText(f"Frame: {self._current_frame} / {max_frame}")

    # Public methods

    def set_total_frames(self, total: int):
        """Set the total number of frames"""
        self._total_frames = total
        self.slider.setMaximum(max(1, total - 1))
        self._update_frame_label()

    def set_current_frame(self, frame: int):
        """Set the current frame (without emitting signal)"""
        self._current_frame = frame
        self.slider.blockSignals(True)
        self.slider.setValue(frame)
        self.slider.blockSignals(False)
        self._update_frame_label()

    def set_keyframes(self, keyframes: List[int]):
        """Update the keyframe dropdown"""
        self.keyframe_combo.clear()
        self.keyframe_combo.addItem("None")
        for kf in sorted(keyframes):
            self.keyframe_combo.addItem(str(kf))

    def set_enabled(self, enabled: bool):
        """Enable/disable timeline controls"""
        self.slider.setEnabled(enabled)
        self.btn_back_10.setEnabled(enabled)
        self.btn_back_1.setEnabled(enabled)
        self.btn_forward_1.setEnabled(enabled)
        self.btn_forward_10.setEnabled(enabled)
        self.keyframe_combo.setEnabled(enabled)
