# config.py

PROJECT_NAME = "Tiny no Jutsu"
COMMAND_NAME = "tinynojutsu"
VERSION = "1.2.2"
LICENSE_SERIAL = "CC BY-NC 4.0"
LICENSE_NAME = "Creative Commons Attribution-NonCommercial 4.0 International ({LICENSE_SERIAL})"
LICENSE_BADGE_URL = "https://img.shields.io/badge/license-CC%20BY--NC%204.0-lightgrey.svg"

BANNER_URL = "assets/banner.png"
EMOJI_URL = "assets/thanos-snap.gif"

AUTHOR = "anas daghma"
AUTHOR_EMAIL = "contact@anasdaghma.com"
GIT_URL = "https://github.com/enigmaelysium/tiny-no-jutsu.git"

PYTHON_BADGE_URL = "https://img.shields.io/badge/python-3.7+-blue.svg"
VERSION_BADGE_URL = f"https://img.shields.io/badge/version-{VERSION}-orange.svg"

SUPPORTED_EXTS = (
    ".jpg", ".jpeg", ".png", ".bmp", ".tiff",
    ".gif", ".heic", ".heif", ".jfif", ".pjpeg", ".pjp"
)

FORMAT_MAP = {
    "jpg": "JPEG",
    "jpeg": "JPEG",
    "png": "PNG",
    "webp": "WEBP",
    "bmp": "BMP",
    "gif": "GIF",
    "tiff": "TIFF"
}

BANNER = r"""
 _____  _                  _   _           ___         _               
|_   _|(_)                | \ | |         |_  |       | |              
  | |   _  _ __   _   _   |  \| |  ___      | | _   _ | |_  ___  _   _ 
  | |  | || '_ \ | | | |  | . ` | / _ \     | || | | || __|/ __|| | | |
  | |  | || | | || |_| |  | |\  || (_) |/\__/ /| |_| || |_ \__ \| |_| |
  \_/  |_||_| |_| \__, |  \_| \_/ \___/ \____/  \__,_| \__||___/ \__,_|
                   __/ |                                               
                  |___/                                                 
"""