from setuptools import setup, find_packages
import tiny_no_jutsu.config as config

setup(
    name=config.PROJECT_NAME,
    version=config.VERSION,
    packages=find_packages(),
    install_requires=[
        "Pillow",
        "tqdm",
        "humanize",
        "pillow-heif",
    ],
    entry_points={
        "console_scripts": [
            "tinynojutsu = tiny_no_jutsu.cli:main",
        ],
    },
    python_requires=">=3.8",
    description="🌀 Tiny no Jutsu - Image Compressor & Converter",
    author=config.AUTHOR,
    author_email=config.AUTHOR_EMAIL,
    url=config.GIT_URL,  # optional
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: Other/Proprietary License",
        "Operating System :: OS Independent",
    ],
)
