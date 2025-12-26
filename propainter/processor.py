"""
Video Processing with LaMa Inpainting
High-quality watermark removal
"""

import cv2
import numpy as np
import os
from typing import Callable, Dict, List, Tuple
import torch
from PIL import Image

DEVICE = torch.device("cuda" if torch.cuda.is_available() else "cpu")


class LamaInpainter:
    """LaMa inpainting for high-quality results."""

    def __init__(self):
        self.model = None
        self._load_model()

    def _load_model(self):
        try:
            from simple_lama_inpainting import SimpleLama
            self.model = SimpleLama()
            print(f"LaMa inpainting loaded on {DEVICE}")
        except Exception as e:
            print(f"Could not load LaMa: {e}")
            self.model = None

    def inpaint_frame(self, frame: np.ndarray, mask: np.ndarray) -> np.ndarray:
        if not np.any(mask > 0) or self.model is None:
            return frame

        frame_pil = Image.fromarray(frame)
        mask_pil = Image.fromarray(mask)
        result = np.array(self.model(frame_pil, mask_pil))

        # Ensure same size
        if result.shape[:2] != frame.shape[:2]:
            result = cv2.resize(result, (frame.shape[1], frame.shape[0]))

        return result

    def process_video(
        self,
        frames: List[np.ndarray],
        masks: List[np.ndarray],
        progress_callback: Callable = None
    ) -> List[np.ndarray]:
        results = []
        for i, (frame, mask) in enumerate(zip(frames, masks)):
            if np.any(mask > 0):
                result = self.inpaint_frame(frame, mask)
            else:
                result = frame
            results.append(result)
            if progress_callback:
                progress_callback(i + 1, len(frames))
        return results


# Alias
StableDiffusionInpainter = LamaInpainter


def create_mask_from_zones(
    width: int,
    height: int,
    zones: List[Tuple[int, int, int, int]],
    feather: int = 5
) -> np.ndarray:
    mask = np.zeros((height, width), dtype=np.uint8)
    for zone in zones:
        x1, y1, x2, y2 = zone
        pad = 8
        x1 = max(0, x1 - pad)
        y1 = max(0, y1 - pad)
        x2 = min(width, x2 + pad)
        y2 = min(height, y2 + pad)
        mask[y1:y2, x1:x2] = 255
    kernel = np.ones((5, 5), np.uint8)
    mask = cv2.dilate(mask, kernel, iterations=2)
    return mask


def get_zones_at_frame(keyframes: Dict, frame_num: int) -> List[Tuple]:
    if not keyframes:
        return []
    kf_dict = {int(k): v for k, v in keyframes.items()}
    valid_keyframes = [k for k in kf_dict.keys() if k <= frame_num]
    if not valid_keyframes:
        return []
    nearest = max(valid_keyframes)
    return [tuple(z) for z in kf_dict[nearest]]


def process_video(
    input_path: str,
    output_path: str,
    keyframes: Dict,
    progress_callback: Callable = None,
    chunk_size: int = 50
):
    cap = cv2.VideoCapture(input_path)
    if not cap.isOpened():
        raise ValueError(f"Could not open video: {input_path}")

    width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    fps = cap.get(cv2.CAP_PROP_FPS)
    total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))

    temp_output = output_path + ".temp.avi"
    fourcc = cv2.VideoWriter_fourcc(*'XVID')
    out = cv2.VideoWriter(temp_output, fourcc, fps, (width, height))

    inpainter = LamaInpainter()

    frame_idx = 0
    frames_buffer = []
    masks_buffer = []

    print(f"Processing {total_frames} frames with LaMa (~{total_frames*0.8/60:.0f} min estimated)...")

    while True:
        ret, frame = cap.read()
        if not ret:
            break

        frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        zones = get_zones_at_frame(keyframes, frame_idx)

        if zones:
            mask = create_mask_from_zones(width, height, zones)
        else:
            mask = np.zeros((height, width), dtype=np.uint8)

        frames_buffer.append(frame_rgb)
        masks_buffer.append(mask)

        if len(frames_buffer) >= chunk_size:
            processed = inpainter.process_video(frames_buffer, masks_buffer)
            for p_frame in processed:
                out.write(cv2.cvtColor(p_frame, cv2.COLOR_RGB2BGR))
            frames_buffer = []
            masks_buffer = []

        frame_idx += 1

        if progress_callback:
            progress_callback(frame_idx, total_frames)

    if frames_buffer:
        processed = inpainter.process_video(frames_buffer, masks_buffer)
        for p_frame in processed:
            out.write(cv2.cvtColor(p_frame, cv2.COLOR_RGB2BGR))

    cap.release()
    out.release()

    try:
        convert_to_mp4(temp_output, output_path, input_path)
        os.remove(temp_output)
    except Exception as e:
        print(f"FFmpeg conversion failed: {e}")
        import shutil
        shutil.move(temp_output, output_path)

    print(f"Video saved to: {output_path}")


def get_ffmpeg_path() -> str:
    import shutil
    try:
        from imageio_ffmpeg import get_ffmpeg_exe
        return get_ffmpeg_exe()
    except ImportError:
        pass
    ffmpeg_path = shutil.which("ffmpeg")
    if ffmpeg_path:
        return ffmpeg_path
    common_paths = [
        r"C:\ffmpeg\bin\ffmpeg.exe",
        r"C:\Program Files\ffmpeg\bin\ffmpeg.exe",
    ]
    for path in common_paths:
        if os.path.exists(path):
            return path
    raise FileNotFoundError("ffmpeg not found")


def convert_to_mp4(input_path: str, output_path: str, original_video: str):
    import subprocess
    ffmpeg = get_ffmpeg_path()
    cmd = [
        ffmpeg, "-y",
        "-i", input_path,
        "-i", original_video,
        "-c:v", "libx264",
        "-preset", "fast",
        "-crf", "18",
        "-c:a", "aac",
        "-b:a", "192k",
        "-map", "0:v:0",
        "-map", "1:a:0?",
        "-movflags", "+faststart",
        output_path
    ]
    subprocess.run(cmd, capture_output=True, check=True)
