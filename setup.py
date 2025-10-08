from setuptools import setup, find_packages

setup(
    name="tiny-no-jutsu",
    version="1.2.0",
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
    author="Your Name",
    url="https://github.com/yourusername/tiny-no-jutsu",  # optional
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)
