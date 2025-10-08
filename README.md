
<img src="assets/banner.png" width="100%" alt="Banner">

# <img src="assets/thanos-snap.gif" width="20" height="20"> Tiny no Jutsu

> Image Compressor & Converter — Cast compression techniques with ninja precision!

[![Python Version](https://img.shields.io/badge/python-3.7+-blue.svg)](https://www.python.org/downloads/)
[![License](https://img.shields.io/badge/license-CC%20BY--NC%204.0-lightgrey.svg)](LICENSE)
[![Version](https://img.shields.io/badge/version-1.2.2-orange.svg)](https://github.com/yourusername/tiny-no-jutsu)

## 📖 Overview

**Tiny no Jutsu** is a powerful yet simple Python utility that compresses and converts images in bulk. Inspired by anime ninja techniques, it reduces image file sizes while maintaining visual quality, making it perfect for web optimization, storage management, and batch processing.

## ✨ Features

- **🗜️ Batch Compression** - Compress multiple images at once with adjustable quality settings
- **🔄 Format Conversion** - Convert between popular image formats (JPG, PNG, WebP, etc.)
- **📊 Detailed Statistics** - View before/after sizes, compression ratios, and processing time
- **⚡ Fast Processing** - Optimized with progress bars and efficient PIL operations
- **🎨 Wide Format Support** - Supports JPG, JPEG, PNG, BMP, TIFF, GIF, HEIC, HEIF, and more
- **🛡️ Safe Processing** - Handles RGBA and palette modes automatically
- **🧠 Smart Prompts** – Automatically prompts for missing input, output, quality, format, and action flags
- **📝 Reports** – Save processed file statistics in JSON or CSV

## 🚀 Installation

There are two ways to install Tiny no Jutsu:

1. Download the prebuilt installer from our [website](https://tiny-no-jutsu.vercel.app/) and follow the instructions.
2. Install via pip from source.

### Prerequisites

Before installation, make sure you have:

- Python 3.7 or higher — Download from [python.org](https://www.python.org/downloads/) if needed.
- pip package manager (comes bundled with Python)
- Git (optional, only needed if cloning the repository)

You can verify your setup with:

```bash
python --version
pip --version
```

You should see Python 3.7+ and pip version information. If you don’t have Git, you can download it from [git-scm.com](https://git-scm.com/downloads) or skip Git and download the ZIP directly from GitHub.

### Option 1: Clone the Project

```bash
git clone https://github.com/yourusername/tiny-no-jutsu.git
cd tiny-no-jutsu
```

### Option 2: Download ZIP

1. Navigate to the GitHub repository.
2. Click **Code → Download ZIP**.
3. Extract the ZIP to a folder of your choice.

### Install Dependencies

```bash
pip install .
```

Or use a requirements file:

```bash
pip install -r requirements.txt
```

**requirements.txt:**
```
Pillow>=9.0.0
tqdm>=4.64.0
humanize>=4.0.0
pillow-heif>=0.5.0
```

## 📋 Usage

### Global Run

simply run:
```bash
tinynojutsu
```
Follow the prompts if any required flags are missing.

### Command-Line Usage

```bash
tinynojutsu -i INPUT_FOLDER -o OUTPUT_FOLDER [OPTIONS]
```
and it will prompt you with the missing options

### Required Arguments

| Argument | Description |
|----------|-------------|
| `-i, --input` | Path to the folder containing images to process |
| `-o, --output` | Path to the folder where processed images will be saved |

### Optional Arguments

| Argument | Default | Description |
|----------|---------|-------------|
| `-q, --quality` | 80 | Compression quality (0-100). Higher = better quality but larger size |
| `-f, --format` | None | Target format for conversion (e.g., `webp`, `jpg`, `png`) |
| `--compress` | False | Enable image compression |
| `--convert` | False | Enable format conversion |
| `--dry-run` | False | Simulate without writing files |
| `--overwrite` | False | Overwrite existing files if present |
| `--report` | False | Generate report of processed files |
| `--report-format` | `json` | Report format (`json` or `csv`) |

**Note:** You must specify at least one action: `--compress` or `--convert` (or both).

### Info And Help Arguments

| Argument | Description |
|----------|-------------|
| `-h, --help` | Show help message and exit |
| `-v, --version` | Show program version and exit |


## 💡 Examples

### Compress Images

Compress all images in a folder to 85% quality:

```bash
tinynojutsu -i ./photos -o ./compressed --compress -q 85
```

### Convert Format

Convert all images to WebP format:

```bash
tinynojutsu -i ./photos -o ./webp_images --convert -f webp
```

### Compress + Convert

Compress AND convert images to JPG at 75% quality:

```bash
tinynojutsu -i ./photos -o ./optimized --compress --convert -f jpg -q 75
```

### High-Quality Compression

Preserve maximum quality while still optimizing:

```bash
tinynojutsu -i ./originals -o ./high_quality --compress -q 95
```

### Web Optimization

Convert to WebP with aggressive compression for web use:

```bash
tinynojutsu -i ./images -o ./web_ready --compress --convert -f webp -q 70
```

## 🖼️ Supported Formats

The following image formats are supported:

- **JPEG** (`.jpg`, `.jpeg`, `.jfif`, `.pjpeg`, `.pjp`)
- **PNG** (`.png`)
- **WebP** (`.webp`)
- **BMP** (`.bmp`)
- **TIFF** (`.tiff`)
- **GIF** (`.gif`)
- **HEIC/HEIF** (`.heic`, `.heif`)

## 📊 Sample Output

```

 _____  _                  _   _           ___         _               
|_   _|(_)                | \ | |         |_  |       | |              
  | |   _  _ __   _   _   |  \| |  ___      | | _   _ | |_  ___  _   _ 
  | |  | || '_ \ | | | |  | . ` | / _ \     | || | | || __|/ __|| | | |
  | |  | || | | || |_| |  | |\  || (_) |/\__/ /| |_| || |_ \__ \| |_| |
  \_/  |_||_| |_| \__, |  \_| \_/ \___/ \____/  \__,_| \__||___/ \__,_|
                   __/ |                                               
                  |___/                                                 

🌀 Tiny no Jutsu v1.2.2 — Ninja-level image compression and conversion!

📋 Mission Briefing
───────────────────────────────────────────────
📂 Input Folder     : ./photos
📁 Output Folder    : ./compressed
🖼️ Total Images      : 25
🎯 Goal             : Compress + Convert
⚙️ Quality          : 85
🔄 Convert To       : webp
🧪 Dry Run          : No
♻️ Overwrite        : No
───────────────────────────────────────────────

⚔️  Casting Tiny no Jutsu: 100%|██████████| 25/25 [00:03<00:00, 7.52img/s]

📊 Mission Complete
────────────────────────────
🕐 Duration       : 3.32 sec
📦 Original Size  : 45.2 MB
💾 New Size       : 12.8 MB
📉 Saved          : 32.4 MB (71.68%)
🎉 Operation Successful — Images mastered with Tiny no Jutsu!

```

## ⚠️ Important Notes

- **Automatic Output Folder Creation** – The script will create the output folder if it does not exist
- **Original Files**: The script never modifies original files—all output goes to a separate folder
- **Format Compatibility**: Some formats (like JPEG) don't support transparency—RGBA images are converted to RGB
- **Quality Trade-offs**: Lower quality values significantly reduce file size but may introduce visible artifacts
- **HEIC/HEIF Support**: May require additional system libraries depending on your OS

## 🐛 Troubleshooting

### "No supported image files found"

- Verify the input folder path is correct
- Ensure your images have supported file extensions
- Check file permissions

### Windows Folder Errors

If `WinError 2` occurs when creating output folder, specify a path with simple names:

```
C:\temp\tiny_output
C:\Users\<yourname>\Desktop\tiny_output
```

### PIL/Pillow Installation Issues

```bash
# Try upgrading pip first
pip install --upgrade pip

# Then install Pillow
pip install --upgrade Pillow
```

### HEIC/HEIF Support

On some systems, you may need additional libraries:

**macOS:**
```bash
brew install libheif
pip install pillow-heif
```

**Linux:**
```bash
sudo apt-get install libheif-dev
pip install pillow-heif
```

## 📝 License

This project is licensed under the **Creative Commons Attribution-NonCommercial 4.0 International ({LICENSE_SERIAL})**.  

You are free to **use, share, and modify** this project for **non-commercial purposes only**, as long as you give appropriate credit.  
For full license details, see the [LICENSE](LICENSE) file.


## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## 💬 Support

If you encounter any issues or have questions:

- Open an issue on GitHub
- Check existing issues for solutions
- Review the documentation above

## 🎯 Roadmap

- [ ] Add support for more image formats
- [ ] Implement recursive folder processing
- [ ] Add preview mode before processing
- [ ] Add batch renaming options
- [ ] Support for metadata preservation

## 🙏 Acknowledgments

- Built with [Pillow (PIL)](https://python-pillow.org/) - Python Imaging Library
- Progress bars powered by [tqdm](https://github.com/tqdm/tqdm)
- Human-readable file sizes via [humanize](https://github.com/python-humanize/humanize)

---

<div align="center">

**Made by anas daghma with ❤️ and ninja precision**

⭐ Star this repo if you find it useful!

</div>
