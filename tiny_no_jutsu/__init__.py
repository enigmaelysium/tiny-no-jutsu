"""
Tiny no Jutsu - Image Compressor & Converter
"""

__version__ = "1.2.0"
__author__ = "anas daghma"
__email__ = "contact@anasdaghma.com"

from .cli import main, process_images

__all__ = ["main", "process_images", "__version__"]