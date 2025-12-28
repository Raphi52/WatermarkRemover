"""
VideoPlayer - Video loading and frame extraction
"""

import cv2
import numpy as np
from pathlib import Path
from typing import Optional


class VideoPlayer:
    """
    Handles video loading and frame extraction using OpenCV.

    Provides:
    - Video file loading with metadata extraction
    - Frame-by-frame navigation
    - Frame retrieval with RGB conversion
    """

    def __init__(self):
        self.cap: Optional[cv2.VideoCapture] = None
        self.total_frames: int = 0
        self.fps: float = 30.0
        self.width: int = 0
        self.height: int = 0
        self.current_frame: int = 0
        self.video_path: Optional[str] = None

    @property
    def is_loaded(self) -> bool:
        """Check if a video is currently loaded"""
        return self.cap is not None and self.cap.isOpened()

    @property
    def duration(self) -> float:
        """Get video duration in seconds"""
        if self.fps > 0:
            return self.total_frames / self.fps
        return 0.0

    def load(self, path: str) -> bool:
        """
        Load a video file.

        Args:
            path: Path to the video file

        Returns:
            True if loaded successfully, False otherwise
        """
        # Release any existing video
        self.release()

        self.cap = cv2.VideoCapture(path)
        if not self.cap.isOpened():
            return False

        self.video_path = path
        self.total_frames = int(self.cap.get(cv2.CAP_PROP_FRAME_COUNT))
        self.fps = self.cap.get(cv2.CAP_PROP_FPS) or 30.0
        self.width = int(self.cap.get(cv2.CAP_PROP_FRAME_WIDTH))
        self.height = int(self.cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
        self.current_frame = 0

        return True

    def get_frame(self, frame_num: int) -> Optional[np.ndarray]:
        """
        Get a specific frame from the video.

        Args:
            frame_num: Frame number to retrieve (0-indexed)

        Returns:
            RGB numpy array of the frame, or None if failed
        """
        if not self.is_loaded:
            return None

        # Clamp frame number to valid range
        frame_num = max(0, min(frame_num, self.total_frames - 1))

        self.cap.set(cv2.CAP_PROP_POS_FRAMES, frame_num)
        ret, frame = self.cap.read()

        if ret:
            self.current_frame = frame_num
            # Convert BGR to RGB
            return cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        return None

    def get_frame_at_time(self, time_seconds: float) -> Optional[np.ndarray]:
        """
        Get frame at a specific time.

        Args:
            time_seconds: Time in seconds

        Returns:
            RGB numpy array of the frame, or None if failed
        """
        frame_num = int(time_seconds * self.fps)
        return self.get_frame(frame_num)

    def next_frame(self) -> Optional[np.ndarray]:
        """Get the next frame"""
        return self.get_frame(self.current_frame + 1)

    def previous_frame(self) -> Optional[np.ndarray]:
        """Get the previous frame"""
        return self.get_frame(self.current_frame - 1)

    def jump_frames(self, delta: int) -> Optional[np.ndarray]:
        """Jump forward or backward by a number of frames"""
        return self.get_frame(self.current_frame + delta)

    def release(self):
        """Release the video capture"""
        if self.cap:
            self.cap.release()
            self.cap = None
            self.video_path = None
            self.total_frames = 0
            self.current_frame = 0

    def get_info_string(self) -> str:
        """Get formatted video info string"""
        if not self.is_loaded:
            return "No video loaded"
        return f"{self.width}x{self.height} | {self.fps:.1f} fps | {self.total_frames} frames"

    def get_filename(self) -> str:
        """Get the video filename"""
        if self.video_path:
            return Path(self.video_path).name
        return ""

    def __del__(self):
        """Cleanup on deletion"""
        self.release()
