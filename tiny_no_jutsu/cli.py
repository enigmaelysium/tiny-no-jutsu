import argparse
import time
import json
import csv
from pathlib import Path
from PIL import Image, UnidentifiedImageError
from tqdm import tqdm
import humanize
import tiny_no_jutsu.config as config
import os
import sys
import pillow_heif


# Determine base directory
if getattr(sys, 'frozen', False):
    # Running as PyInstaller exe
    BASE_DIR = sys._MEIPASS
else:
    # Running as Python script
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))

ASSETS_DIR = os.path.join(BASE_DIR, "assets")


# Optional HEIC support
try:
    pillow_heif.register_heif_opener()
except ImportError:
    pass

SUPPORTED_EXTS = config.SUPPORTED_EXTS

VERSION = config.VERSION

FORMAT_MAP = config.FORMAT_MAP

PROJECT_NAME = config.PROJECT_NAME

BANNER = config.BANNER


def banner():
    print(BANNER)
    print(f"🌀 {PROJECT_NAME} v{VERSION} — Ninja-level image compression and conversion!\n")


def clamp_quality(quality):
    return max(1, min(quality, 100))


def get_supported_files(folder: Path):
    return sorted(
        f for f in folder.iterdir()
        if f.is_file() and f.suffix.lower() in SUPPORTED_EXTS
    )


def get_total_size(folder: Path, files):
    return sum(f.stat().st_size for f in files)


def print_mission_briefing(input_folder, output_folder, total_files, quality, convert_format, compress, convert, dry_run, overwrite):
    if convert and compress:
        goal = "Convert + Compress"
    elif convert:
        goal = "Convert"
    elif compress:
        goal = "Compress"
    else:
        goal = "Inspect"

    print("\n📋 Mission Briefing")
    print("───────────────────────────────────────────────")

    def line(label, value):
        print(f"{label:<20}: {value}")

    line("📂 Input Folder", input_folder)
    line("📁 Output Folder", output_folder)
    line("🖼️ Total Images", total_files)
    line("🎯 Goal", goal)
    line("⚙️ Quality", quality)
    if convert:
        line("🔄 Convert To", convert_format)
    line("🧪 Dry Run", "Yes" if dry_run else "No")
    line("♻️ Overwrite", "Yes" if overwrite else "No")

    print("───────────────────────────────────────────────\n")


def process_single_file(file: Path, input_folder: Path, output_folder: Path, quality, convert_format, compress, convert, dry_run, overwrite):
    try:
        with Image.open(file) as img:
            exif_data = img.info.get("exif", None)
            if img.mode in ("RGBA", "P"):
                img = img.convert("RGB")

            output_ext = (convert_format or file.suffix[1:]).lower()
            format_name = FORMAT_MAP.get(output_ext, output_ext.upper())
            output_file = output_folder / f"{file.stem}.{output_ext}"

            if output_file.exists() and not overwrite:
                tqdm.write(f"⚠️ Skipped (exists): {file.name}")
                return output_file.stat().st_size, output_file

            if img.format == "GIF" and getattr(img, "is_animated", False):
                tqdm.write(f"⚠️ Skipped animated GIF: {file.name}")
                return 0, output_file

            if dry_run:
                tqdm.write(f"🔍 Dry run: would process {file.name}")
                return file.stat().st_size, output_file

            save_kwargs = {}
            if compress or convert:
                if output_ext in ["jpg", "jpeg", "webp"]:
                    save_kwargs["quality"] = clamp_quality(quality)
                    save_kwargs["optimize"] = True
            if exif_data:
                save_kwargs["exif"] = exif_data

            output_file.parent.mkdir(parents=True, exist_ok=True)  # ensure parent exists
            img.save(output_file, format=format_name, **save_kwargs)
            return output_file.stat().st_size, output_file

    except UnidentifiedImageError:
        tqdm.write(f"⚠️ Unsupported file: {file.name}")
    except Exception as e:
        tqdm.write(f"⚠️ Error: {file.name} → {e}")

    return 0, Path("")


def process_all_files(files, input_folder: Path, output_folder: Path, quality, convert_format, compress, convert, dry_run, overwrite):
    total_size_after = 0
    start_time = time.time()
    report_data = []

    with tqdm(total=len(files), desc="⚔️  Casting {PROJECT_NAME}", unit="img") as pbar:
        for file in files:
            size_after, output_file = process_single_file(
                file, input_folder, output_folder, quality, convert_format, compress, convert, dry_run, overwrite
            )
            size_before = file.stat().st_size
            total_size_after += size_after
            report_data.append({
                "filename": file.name,
                "input_size": size_before,
                "output_size": size_after,
                "output_path": str(output_file)
            })
            pbar.update(1)

    return total_size_after, time.time() - start_time, report_data


def print_summary(before, after, duration, dry_run):
    saved = before - after
    percent = (saved / before * 100) if before > 0 else 0

    print("\n📊 Mission Complete")
    print("────────────────────────────")
    print(f"🕐 Duration       : {duration:.2f}s")
    print(f"📦 Original Size  : {humanize.naturalsize(before)}")
    print(f"💾 New Size       : {humanize.naturalsize(after)}")
    if not dry_run:
        print(f"📉 Saved          : {humanize.naturalsize(saved)} ({percent:.2f}%)")
    print(f"🎉 {'Simulation finished!' if dry_run else 'Operation Successful — Images mastered!'}\n")


def save_report(report_data, output_folder: Path, report_format="json"):
    report_path = output_folder / f"tiny_no_jutsu_report.{report_format}"
    try:
        if report_format.lower() == "json":
            with open(report_path, "w") as f:
                json.dump(report_data, f, indent=2)
        elif report_format.lower() == "csv":
            keys = report_data[0].keys() if report_data else []
            with open(report_path, "w", newline="", encoding="utf-8") as f:
                writer = csv.DictWriter(f, fieldnames=keys)
                writer.writeheader()
                writer.writerows(report_data)
        print(f"📑 Report saved at: {report_path}")
    except Exception as e:
        print(f"❌ Failed to save report: {e}")


def process_images(input_folder, output_folder, quality, convert_format=None, compress=False, convert=False, dry_run=False, overwrite=False, report=False, report_format="json"):
    import os
    
    # Ensure we have Path objects
    input_folder = Path(input_folder) if not isinstance(input_folder, Path) else input_folder
    output_folder = Path(output_folder) if not isinstance(output_folder, Path) else output_folder
    
    # Create output folder with better error handling
    try:
        # Try using os.makedirs as a fallback for Windows special folders
        if not output_folder.exists():
            os.makedirs(str(output_folder), exist_ok=True)
    except Exception as e:
        print(f"❌ Failed to create output folder: {output_folder}")
        print(f"   Error: {e}")
        print(f"   Try specifying a different output path, such as:")
        print(f"   - C:\\temp\\tiny_output")
        print(f"   - C:\\Users\\anas_\\Desktop\\tiny_output")
        return

    files = get_supported_files(input_folder)
    if not files:
        print("⚠️ No supported image files found.")
        return

    print_mission_briefing(input_folder, output_folder, len(files), quality, convert_format, compress, convert, dry_run, overwrite)

    total_before = get_total_size(input_folder, files)
    total_after, duration, report_data = process_all_files(
        files, input_folder, output_folder, quality, convert_format, compress, convert, dry_run, overwrite
    )

    print_summary(total_before, total_after, duration, dry_run)

    if report:
        save_report(report_data, output_folder, report_format)


def cli():

     # Custom usage string for clean help output
    usage_str = (
        "tinynojutsu [-h] [-v] [-i INPUT] [-o OUTPUT] [-q QUALITY] "
        "[-f FORMAT] [--compress] [--convert] [--dry-run] [--overwrite] "
        "[--report] [--report-format {json,csv}]"
    )

    parser = argparse.ArgumentParser(description=f"🌀 {PROJECT_NAME} - Image Compressor & Converter with reporting", usage=usage_str, formatter_class=argparse.RawTextHelpFormatter, add_help=False )
    # Version & Help first
    parser.add_argument("-v", "--version", action="store_true", help="Show the version and exit")
    parser.add_argument("-h", "--help", action="store_true", help="Show the help and exit")
    
   

    # Then image processing arguments
    parser.add_argument("-i", "--input", help="Input folder", required=False)
    parser.add_argument("-o", "--output", help="Output folder", required=False)
    parser.add_argument("-q", "--quality", type=int, default=None, help="Compression quality (1–100)")
    parser.add_argument("-f", "--format", help="Target format (webp, jpg, png)")
    parser.add_argument("--compress", action="store_true", help="Compress images")
    parser.add_argument("--convert", action="store_true", help="Convert format")
    parser.add_argument("--dry-run", action="store_true", help="Simulate without writing files")
    parser.add_argument("--overwrite", action="store_true", help="Overwrite existing files")
    parser.add_argument("--report", action="store_true", help="Generate report of all processed files")
    parser.add_argument("--report-format", choices=["json", "csv"], default=None, help="Report format")

    args = parser.parse_args()
    
    # Track which flags were explicitly provided via command line
    provided_args = sys.argv[1:]

    # Immediate exit flags
    if len(provided_args) == 1:
        if args.help:
            parser.print_help()
            return
        if args.version:
            print(f"v{VERSION}")
            return
        
    banner()

    

    # --- Input Folder ---
    input_path_str = args.input or input(f"📂 Enter input folder (default: current folder): ").strip()
    input_path_str = input_path_str.strip('"').strip("'")
    input_folder = Path(input_path_str) if input_path_str else Path.cwd()
    
    # Validate input folder exists
    if not input_folder.exists():
        print(f"❌ Input folder does not exist: {input_folder}")
        return
    if not input_folder.is_dir():
        print(f"❌ Input path is not a directory: {input_folder}")
        return
    
    input_folder = input_folder.resolve()

    # --- Output Folder ---
    default_output = input_folder / "tiny_no_jutsu_output"
    output_path_str = args.output or input(f"📁 Enter output folder (default: '{default_output}'): ").strip()
    output_path_str = output_path_str.strip('"').strip("'")
    output_folder = Path(output_path_str) if output_path_str else default_output
    output_folder = output_folder.resolve()

    # --- Action Selection ---
    if not args.compress and not args.convert:
        choice = ""
        while choice.lower() not in ["c", "x", "b"]:
            choice = input("Choose action: [C]ompress, [X] Convert, [B]oth: ").strip().lower()
        args.compress = choice in ["c", "b"]
        args.convert = choice in ["x", "b"]

    # --- Format prompt if converting ---
    if args.convert and not args.format:
        args.format = input("🔄 Enter format to convert to (e.g., webp, jpg, png): ").strip().lower()

    # --- Quality prompt if compressing ---
    if args.compress and args.quality is None:
        q = input("⚙️  Enter compression quality (0-100, default 80): ").strip()
        args.quality = int(q) if q.isdigit() else 80
    elif args.quality is None:
        args.quality = 80

    # --- Dry-run prompt if not specified via CLI ---
    if '--dry-run' not in provided_args:
        dry_choice = input("🧪 Dry run (simulate without writing files)? [y/N]: ").strip().lower()
        args.dry_run = dry_choice == "y"

    # --- Overwrite prompt if not specified via CLI ---
    if '--overwrite' not in provided_args:
        overwrite_choice = input("♻️  Overwrite existing files if present? [y/N]: ").strip().lower()
        args.overwrite = overwrite_choice == "y"

    # --- Report prompt ---
    if '--report' not in provided_args:
        report_choice = input("📑 Generate report of processed files? [y/N]: ").strip().lower()
        args.report = report_choice == "y"

    if args.report and args.report_format is None:
        fmt_choice = ""
        while fmt_choice not in ["json", "csv"]:
            fmt_choice = input("📄 Report format [json/csv]: ").strip().lower()
        args.report_format = fmt_choice
    elif args.report_format is None:
        args.report_format = "json"

    # --- Run processing ---
    process_images(
        input_folder=input_folder,
        output_folder=output_folder,
        quality=args.quality,
        convert_format=args.format,
        compress=args.compress,
        convert=args.convert,
        dry_run=args.dry_run,
        overwrite=args.overwrite,
        report=args.report,
        report_format=args.report_format
    )

def main():
    try:
       cli()
    except KeyboardInterrupt:
        print("\n🌀 Scroll rolled back — mission cancelled!")
        exit(0)