"""
KeyframeManager - Watermark zone management across frames
"""

import json
from typing import Dict, List, Tuple, Optional
from pathlib import Path


# Type alias for zone coordinates
Zone = Tuple[int, int, int, int]  # (x1, y1, x2, y2)


class KeyframeManager:
    """
    Manages watermark zones across different video frames.

    Zones are stored per keyframe, and interpolated for frames
    between keyframes (zones persist until the next keyframe).
    """

    def __init__(self):
        # Format: {frame_number: [(x1, y1, x2, y2), ...]}
        self._keyframes: Dict[int, List[Zone]] = {}

    @property
    def keyframes(self) -> Dict[int, List[Zone]]:
        """Get all keyframes"""
        return self._keyframes

    @property
    def is_empty(self) -> bool:
        """Check if there are no zones defined"""
        return len(self._keyframes) == 0

    def add_zone(self, frame: int, zone: Zone) -> None:
        """
        Add a watermark zone at a specific frame.

        Args:
            frame: Frame number to add the zone at
            zone: Tuple of (x1, y1, x2, y2) coordinates
        """
        if frame not in self._keyframes:
            self._keyframes[frame] = []
        self._keyframes[frame].append(zone)

    def remove_zone(self, frame: int, index: int) -> bool:
        """
        Remove a zone at a specific frame by index.

        Args:
            frame: Frame number
            index: Index of the zone to remove

        Returns:
            True if removed successfully
        """
        if frame in self._keyframes and 0 <= index < len(self._keyframes[frame]):
            self._keyframes[frame].pop(index)
            # Clean up empty keyframes
            if not self._keyframes[frame]:
                del self._keyframes[frame]
            return True
        return False

    def remove_keyframe(self, frame: int) -> bool:
        """
        Remove all zones at a specific frame.

        Args:
            frame: Frame number to remove

        Returns:
            True if removed successfully
        """
        if frame in self._keyframes:
            del self._keyframes[frame]
            return True
        return False

    def get_zones_at_frame(self, frame: int) -> List[Zone]:
        """
        Get active zones for a specific frame.

        Uses nearest previous keyframe interpolation - zones persist
        from a keyframe until the next keyframe is reached.

        Args:
            frame: Frame number to query

        Returns:
            List of zone coordinates active at this frame
        """
        if not self._keyframes:
            return []

        # Find the nearest keyframe at or before this frame
        valid_keyframes = [k for k in self._keyframes.keys() if k <= frame]
        if not valid_keyframes:
            return []

        nearest = max(valid_keyframes)
        return self._keyframes[nearest].copy()

    def get_all_keyframe_numbers(self) -> List[int]:
        """Get sorted list of all keyframe numbers"""
        return sorted(self._keyframes.keys())

    def get_zone_count(self, frame: int = None) -> int:
        """
        Get total number of zones.

        Args:
            frame: If specified, count zones at this frame only

        Returns:
            Number of zones
        """
        if frame is not None:
            return len(self.get_zones_at_frame(frame))
        return sum(len(zones) for zones in self._keyframes.values())

    def clear(self) -> None:
        """Clear all keyframes and zones"""
        self._keyframes.clear()

    def to_dict(self) -> Dict[str, List[Zone]]:
        """
        Convert to dictionary format for serialization.

        Returns:
            Dictionary with string keys (frame numbers)
        """
        return {str(k): v for k, v in self._keyframes.items()}

    def from_dict(self, data: Dict[str, List[Zone]]) -> None:
        """
        Load from dictionary format.

        Args:
            data: Dictionary with string keys (frame numbers)
        """
        self._keyframes = {int(k): v for k, v in data.items()}

    def save_to_file(self, video_path: str) -> str:
        """
        Save keyframes to a JSON file.

        Args:
            video_path: Path to the video file (used to generate save path)

        Returns:
            Path to the saved file
        """
        save_path = f"{video_path}.zones.json"
        with open(save_path, 'w') as f:
            json.dump(self.to_dict(), f, indent=2)
        return save_path

    def load_from_file(self, video_path: str) -> bool:
        """
        Load keyframes from a JSON file.

        Args:
            video_path: Path to the video file

        Returns:
            True if loaded successfully
        """
        zones_path = f"{video_path}.zones.json"
        if Path(zones_path).exists():
            try:
                with open(zones_path, 'r') as f:
                    data = json.load(f)
                self.from_dict(data)
                return True
            except (json.JSONDecodeError, IOError):
                pass
        return False

    def get_summary(self) -> str:
        """Get a text summary of all keyframes and zones"""
        if not self._keyframes:
            return "No zones defined"

        lines = []
        for frame in self.get_all_keyframe_numbers():
            zones = self._keyframes[frame]
            lines.append(f"Frame {frame}:")
            for i, zone in enumerate(zones):
                lines.append(f"  Zone {i+1}: {zone}")
        return "\n".join(lines)
