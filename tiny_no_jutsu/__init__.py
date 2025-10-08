import tiny_no_jutsu.config as config

"""
Tiny no Jutsu - Image Compressor & Converter
"""

__version__ = config.VERSION
__author__ = config.AUTHOR
__email__ = config.AUTHOR_EMAIL


# Lazy import functions to avoid import-time errors
def main(*args, **kwargs):
    from .cli import main as cli_main
    return cli_main(*args, **kwargs)

def process_images(*args, **kwargs):
    from .cli import process_images as cli_process
    return cli_process(*args, **kwargs)

__all__ = ["main", "process_images", "__version__"]