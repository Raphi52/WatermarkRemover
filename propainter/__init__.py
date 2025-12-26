"""
ProPainter Video Inpainting Module
Simplified implementation for watermark removal
"""

from .processor import process_video, StableDiffusionInpainter, LamaInpainter

__all__ = ['process_video', 'StableDiffusionInpainter', 'LamaInpainter']
