"""
Sidebar - Left panel with controls and info
"""

from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel,
    QTextEdit, QCheckBox, QFrame, QScrollArea
)
from PySide6.QtCore import Qt, Signal
from PySide6.QtGui import QFont

from ..styles.colors import Colors
from ..components.glass_panel import GlassPanel, GlassCard
from ..components.glow_button import GlowButton, DangerButton
from ..components.gradient_progress import GradientProgressBar


class Sidebar(GlassPanel):
    """
    Left sidebar with scrollable content
    """

    # Signals
    open_video_clicked = Signal()
    open_batch_clicked = Signal()
    add_zone_clicked = Signal()
    clear_all_clicked = Signal()
    save_keyframes_clicked = Signal()
    select_output_clicked = Signal()
    process_clicked = Signal()
    preview_toggled = Signal(bool)

    def __init__(self, parent=None):
        super().__init__(parent, hover_effect=False)

        self.setFixedWidth(340)
        self._setup_ui()

    def _setup_ui(self):
        """Build the sidebar UI with scroll area"""
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)

        # Scroll area for content
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        scroll.setStyleSheet("""
            QScrollArea {
                background: transparent;
                border: none;
            }
            QScrollArea > QWidget > QWidget {
                background: transparent;
            }
        """)

        # Content widget
        content = QWidget()
        content.setStyleSheet("background: transparent;")
        layout = QVBoxLayout(content)
        layout.setContentsMargins(16, 20, 16, 20)
        layout.setSpacing(12)

        # Title section
        layout.addWidget(self._create_title_section())

        # Separator
        layout.addWidget(self._create_separator())

        # File section
        layout.addWidget(self._create_file_section())

        # Keyframes section
        layout.addWidget(self._create_keyframes_section())

        # Processing section
        layout.addWidget(self._create_processing_section())

        # Spacer
        layout.addStretch()

        # Info section
        layout.addWidget(self._create_info_section())

        scroll.setWidget(content)
        main_layout.addWidget(scroll)

    def _create_separator(self) -> QFrame:
        """Create a horizontal separator line"""
        sep = QFrame()
        sep.setFixedHeight(1)
        sep.setStyleSheet("background-color: rgba(255, 255, 255, 0.1);")
        return sep

    def _create_title_section(self) -> QWidget:
        """Create title and subtitle"""
        container = QWidget()
        container.setStyleSheet("background: transparent;")
        layout = QVBoxLayout(container)
        layout.setContentsMargins(0, 0, 0, 8)
        layout.setSpacing(2)

        # Title
        title = QLabel("WatermarkRemover")
        title_font = QFont("Segoe UI", 16)
        title_font.setWeight(QFont.Bold)
        title.setFont(title_font)
        title.setStyleSheet(f"color: {Colors.TEXT_PRIMARY}; background: transparent;")
        layout.addWidget(title)

        # Subtitle
        subtitle = QLabel("ProPainter Video Inpainting")
        subtitle.setStyleSheet(f"color: {Colors.TEXT_TERTIARY}; font-size: 11px; background: transparent;")
        layout.addWidget(subtitle)

        return container

    def _create_file_section(self) -> QWidget:
        """Create video file controls"""
        card = QWidget()
        card.setStyleSheet(f"""
            QWidget {{
                background-color: rgba(31, 31, 58, 0.6);
                border: 1px solid rgba(255, 255, 255, 0.08);
                border-radius: 12px;
            }}
        """)
        layout = QVBoxLayout(card)
        layout.setContentsMargins(12, 12, 12, 12)
        layout.setSpacing(8)

        # Section title
        title = QLabel("Video File")
        title.setStyleSheet(f"color: {Colors.TEXT_SECONDARY}; font-weight: 600; font-size: 12px; background: transparent; border: none;")
        layout.addWidget(title)

        # Buttons row
        btn_layout = QHBoxLayout()
        btn_layout.setSpacing(6)

        self.open_btn = GlowButton("Open Video", primary=False)
        self.open_btn.setMinimumHeight(36)
        self.open_btn.clicked.connect(self.open_video_clicked.emit)
        btn_layout.addWidget(self.open_btn)

        self.batch_btn = GlowButton("Batch", primary=False)
        self.batch_btn.setMinimumHeight(36)
        self.batch_btn.setMinimumWidth(80)
        self.batch_btn.clicked.connect(self.open_batch_clicked.emit)
        btn_layout.addWidget(self.batch_btn)

        layout.addLayout(btn_layout)

        # File name label
        self.file_label = QLabel("No file loaded")
        self.file_label.setStyleSheet(f"color: {Colors.TEXT_TERTIARY}; font-size: 11px; background: transparent; border: none;")
        self.file_label.setWordWrap(True)
        layout.addWidget(self.file_label)

        return card

    def _create_keyframes_section(self) -> QWidget:
        """Create keyframes management controls"""
        card = QWidget()
        card.setStyleSheet(f"""
            QWidget {{
                background-color: rgba(31, 31, 58, 0.6);
                border: 1px solid rgba(255, 255, 255, 0.08);
                border-radius: 12px;
            }}
        """)
        layout = QVBoxLayout(card)
        layout.setContentsMargins(12, 12, 12, 12)
        layout.setSpacing(8)

        # Section title
        title = QLabel("Keyframes")
        title.setStyleSheet(f"color: {Colors.TEXT_SECONDARY}; font-weight: 600; font-size: 12px; background: transparent; border: none;")
        layout.addWidget(title)

        # Keyframe list
        self.keyframe_list = QTextEdit()
        self.keyframe_list.setReadOnly(True)
        self.keyframe_list.setFixedHeight(80)
        self.keyframe_list.setStyleSheet(f"""
            QTextEdit {{
                background-color: rgba(255, 255, 255, 0.03);
                border: 1px solid rgba(255, 255, 255, 0.08);
                border-radius: 6px;
                color: {Colors.TEXT_SECONDARY};
                font-size: 10px;
                padding: 6px;
            }}
        """)
        self.keyframe_list.setPlaceholderText("Draw rectangles on video...")
        layout.addWidget(self.keyframe_list)

        # Button row
        btn_layout = QHBoxLayout()
        btn_layout.setSpacing(4)

        self.add_zone_btn = GlowButton("Add", primary=False)
        self.add_zone_btn.setMinimumHeight(32)
        self.add_zone_btn.clicked.connect(self.add_zone_clicked.emit)
        btn_layout.addWidget(self.add_zone_btn)

        self.clear_btn = DangerButton("Clear")
        self.clear_btn.setMinimumHeight(32)
        self.clear_btn.clicked.connect(self.clear_all_clicked.emit)
        btn_layout.addWidget(self.clear_btn)

        self.save_btn = GlowButton("Save", primary=False)
        self.save_btn.setMinimumHeight(32)
        self.save_btn.setMinimumWidth(70)
        self.save_btn.clicked.connect(self.save_keyframes_clicked.emit)
        btn_layout.addWidget(self.save_btn)

        layout.addLayout(btn_layout)

        # Preview toggle
        self.preview_check = QCheckBox("Show zones overlay")
        self.preview_check.setChecked(True)
        self.preview_check.setStyleSheet(f"""
            QCheckBox {{
                color: {Colors.TEXT_SECONDARY};
                spacing: 6px;
                font-size: 11px;
                background: transparent;
                border: none;
            }}
            QCheckBox::indicator {{
                width: 16px;
                height: 16px;
                border-radius: 4px;
                background-color: rgba(255, 255, 255, 0.1);
                border: 1px solid rgba(255, 255, 255, 0.15);
            }}
            QCheckBox::indicator:checked {{
                background-color: {Colors.ACCENT};
                border: none;
            }}
        """)
        self.preview_check.toggled.connect(self.preview_toggled.emit)
        layout.addWidget(self.preview_check)

        return card

    def _create_processing_section(self) -> QWidget:
        """Create processing controls"""
        card = QWidget()
        card.setStyleSheet(f"""
            QWidget {{
                background-color: rgba(31, 31, 58, 0.6);
                border: 1px solid rgba(255, 255, 255, 0.08);
                border-radius: 12px;
            }}
        """)
        layout = QVBoxLayout(card)
        layout.setContentsMargins(12, 12, 12, 12)
        layout.setSpacing(8)

        # Section title
        title = QLabel("Processing")
        title.setStyleSheet(f"color: {Colors.TEXT_SECONDARY}; font-weight: 600; font-size: 12px; background: transparent; border: none;")
        layout.addWidget(title)

        # Output folder button
        self.output_btn = GlowButton("Output Folder", primary=False)
        self.output_btn.setMinimumHeight(36)
        self.output_btn.clicked.connect(self.select_output_clicked.emit)
        layout.addWidget(self.output_btn)

        # Output path label
        self.output_label = QLabel("./output")
        self.output_label.setStyleSheet(f"color: {Colors.TEXT_TERTIARY}; font-size: 10px; background: transparent; border: none;")
        self.output_label.setWordWrap(True)
        layout.addWidget(self.output_label)

        # Progress bar
        self.progress_bar = GradientProgressBar()
        layout.addWidget(self.progress_bar)

        # Status label
        self.status_label = QLabel("Ready")
        self.status_label.setStyleSheet(f"color: {Colors.TEXT_TERTIARY}; font-size: 11px; background: transparent; border: none;")
        layout.addWidget(self.status_label)

        # Process button (main action)
        self.process_btn = GlowButton("Remove Watermarks", primary=True)
        self.process_btn.setMinimumHeight(44)
        self.process_btn.clicked.connect(self.process_clicked.emit)
        layout.addWidget(self.process_btn)

        return card

    def _create_info_section(self) -> QWidget:
        """Create help info section"""
        container = QWidget()
        container.setStyleSheet("background: transparent;")
        layout = QVBoxLayout(container)
        layout.setContentsMargins(4, 0, 4, 0)

        info_text = "1. Load video\n2. Navigate to frame\n3. Draw rectangle\n4. Click Remove"

        info = QLabel(info_text)
        info.setStyleSheet(f"color: {Colors.TEXT_TERTIARY}; font-size: 10px; background: transparent;")
        info.setWordWrap(True)
        layout.addWidget(info)

        return container

    # Public methods to update UI

    def set_file_name(self, name: str):
        self.file_label.setText(name if name else "No file loaded")

    def set_output_path(self, path: str):
        self.output_label.setText(path)

    def set_status(self, text: str):
        self.status_label.setText(text)

    def set_progress(self, value: int, maximum: int = 100):
        self.progress_bar.setMaximum(maximum)
        self.progress_bar.setValue(value)

    def set_keyframe_list(self, text: str):
        self.keyframe_list.setText(text)

    def set_processing_enabled(self, enabled: bool):
        self.process_btn.setEnabled(enabled)
        self.open_btn.setEnabled(enabled)
        self.batch_btn.setEnabled(enabled)
