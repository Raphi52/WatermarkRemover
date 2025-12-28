"""
MainWindow - Main application window with Acrylic/Mica effect
"""

import sys
from pathlib import Path

from PySide6.QtWidgets import (
    QMainWindow, QWidget, QHBoxLayout, QVBoxLayout,
    QApplication, QGraphicsDropShadowEffect
)
from PySide6.QtGui import QScreen
from PySide6.QtCore import Qt, Signal
from PySide6.QtGui import QColor

from ..styles.colors import Colors

# Try to import frameless window for Mica/Acrylic effect
try:
    from qframelesswindow import AcrylicWindow as BaseWindow
    HAS_ACRYLIC = True
except ImportError:
    BaseWindow = QMainWindow
    HAS_ACRYLIC = False


class MainWindow(BaseWindow):
    """
    Main application window with:
    - Frameless design with custom title bar
    - Acrylic/Mica background effect (Windows 10/11)
    - Dark glassmorphism theme
    """

    # Signals
    video_loaded = Signal(str)  # Emitted when a video is loaded
    processing_started = Signal()
    processing_finished = Signal(str)  # Path to output file

    def __init__(self):
        super().__init__()

        self._setup_window()
        self._setup_central_widget()
        self._apply_effects()

    def _setup_window(self):
        """Configure window properties"""
        self.setWindowTitle("WatermarkRemover")
        self.resize(1600, 1000)
        self.setMinimumSize(1400, 900)

        # Center on screen
        screen = QApplication.primaryScreen().geometry()
        x = (screen.width() - 1600) // 2
        y = (screen.height() - 1000) // 2
        self.move(x, y)

        # Enable Mica effect on Windows 11 if available
        if HAS_ACRYLIC and sys.platform == 'win32':
            try:
                self.windowEffect.setMicaEffect(self.winId(), isDark=True)
            except Exception:
                # Fallback to acrylic if Mica not available
                try:
                    self.windowEffect.setAcrylicEffect(self.winId(), "1a1a2eF0")
                except Exception:
                    pass

    def _setup_central_widget(self):
        """Setup the central widget with main layout"""
        self.central_widget = QWidget()
        self.central_widget.setObjectName("centralWidget")
        self.setCentralWidget(self.central_widget)

        # Apply dark background
        self.central_widget.setStyleSheet(f"""
            #centralWidget {{
                background-color: {Colors.BG_PRIMARY};
            }}
        """)

        # Main layout will be set by the App class
        self.main_layout = QHBoxLayout(self.central_widget)
        self.main_layout.setContentsMargins(16, 16, 16, 16)
        self.main_layout.setSpacing(16)

    def _apply_effects(self):
        """Apply visual effects to window"""
        # Add subtle shadow to the window content
        if not HAS_ACRYLIC:
            # Manual dark background for non-acrylic
            self.setStyleSheet(f"""
                QMainWindow {{
                    background-color: {Colors.BG_PRIMARY};
                }}
            """)

    def get_main_layout(self) -> QHBoxLayout:
        """Get the main layout for adding widgets"""
        return self.main_layout

    def add_sidebar(self, sidebar: QWidget):
        """Add sidebar to the left"""
        self.main_layout.insertWidget(0, sidebar)

    def add_content(self, content: QWidget):
        """Add main content area"""
        self.main_layout.addWidget(content, 1)

    def show_message(self, title: str, message: str, is_error: bool = False):
        """Show a message dialog"""
        from PySide6.QtWidgets import QMessageBox

        msg = QMessageBox(self)
        msg.setWindowTitle(title)
        msg.setText(message)
        msg.setIcon(QMessageBox.Critical if is_error else QMessageBox.Information)

        # Style the message box
        msg.setStyleSheet(f"""
            QMessageBox {{
                background-color: {Colors.BG_PRIMARY};
            }}
            QMessageBox QLabel {{
                color: {Colors.TEXT_PRIMARY};
                font-size: 14px;
            }}
            QPushButton {{
                background-color: rgba(255, 255, 255, 0.08);
                border: 1px solid rgba(255, 255, 255, 0.12);
                border-radius: 8px;
                color: white;
                padding: 8px 20px;
                min-width: 80px;
            }}
            QPushButton:hover {{
                background-color: rgba(255, 255, 255, 0.12);
            }}
        """)

        msg.exec()

    def confirm_action(self, title: str, message: str) -> bool:
        """Show a confirmation dialog"""
        from PySide6.QtWidgets import QMessageBox

        msg = QMessageBox(self)
        msg.setWindowTitle(title)
        msg.setText(message)
        msg.setIcon(QMessageBox.Question)
        msg.setStandardButtons(QMessageBox.Yes | QMessageBox.No)
        msg.setDefaultButton(QMessageBox.No)

        msg.setStyleSheet(f"""
            QMessageBox {{
                background-color: {Colors.BG_PRIMARY};
            }}
            QMessageBox QLabel {{
                color: {Colors.TEXT_PRIMARY};
            }}
            QPushButton {{
                background-color: rgba(255, 255, 255, 0.08);
                border: 1px solid rgba(255, 255, 255, 0.12);
                border-radius: 8px;
                color: white;
                padding: 8px 20px;
                min-width: 80px;
            }}
            QPushButton:hover {{
                background-color: rgba(255, 255, 255, 0.12);
            }}
        """)

        return msg.exec() == QMessageBox.Yes
