import os
import argparse
import time
from PIL import Image
from tqdm import tqdm
import humanize

SUPPORTED_EXTS = (".jpg", ".jpeg", ".png", ".bmp", ".tiff", ".gif", ".heic", ".heif", ".jfif", ".pjpeg", ".pjp")

VERSION = "1.0.0"

def banner():
    print(r"""
 _____  _                  _   _           ___         _               
|_   _|(_)                | \ | |         |_  |       | |              
  | |   _  _ __   _   _   |  \| |  ___      | | _   _ | |_  ___  _   _ 
  | |  | || '_ \ | | | |  | . ` | / _ \     | || | | || __|/ __|| | | |
  | |  | || | | || |_| |  | |\  || (_) |/\__/ /| |_| || |_ \__ \| |_| |
  \_/  |_||_| |_| \__, |  \_| \_/ \___/ \____/  \__,_| \__||___/ \__,_|
                   __/ |                                               
                  |___/                                                
""")
    print(f"🌀 Tiny no Jutsu v{VERSION} — Casting compression technique with ninja precision!\n")


def get_total_size(folder, files):
    """Calculate total size in bytes for given files in folder."""
    return sum(os.path.getsize(os.path.join(folder, f)) for f in files if os.path.isfile(os.path.join(folder, f)))

def process_images(input_folder, output_folder, quality, convert_format=None, compress=False, convert=False):
    os.makedirs(output_folder, exist_ok=True)

    files = get_supported_files(input_folder)
    total_files = len(files)

    if total_files == 0:
        print("⚠️ No supported image files found.")
        return

    print_mission_briefing(input_folder, output_folder, total_files, quality, convert_format, compress, convert)

    total_size_before = get_total_size(input_folder, files)
    total_size_after, duration = process_all_files(files, input_folder, output_folder, quality, convert_format, compress, convert)

    print_summary(total_size_before, total_size_after, duration)


def get_supported_files(input_folder):
    return [
        f for f in os.listdir(input_folder)
        if os.path.isfile(os.path.join(input_folder, f)) and f.lower().endswith(SUPPORTED_EXTS)
    ]


def print_mission_briefing(input_folder, output_folder, total_files, quality, convert_format, compress, convert):
    goal = ""
    if convert and not compress:
        goal = "Convert"
    elif compress and not convert:
        goal = "Compress"
    elif convert and compress:
        goal = "Convert + Compress"

    print("📋 Mission Briefing")
    print("────────────────────────────")
    print(f"📂 Input Folder : {input_folder}")
    print(f"📁 Output Folder: {output_folder}")
    print(f"🖼️  Total Images: {total_files}")
    print(f"🎯 Goal         : {goal}")
    if compress:
        print(f"⚙️  Quality      : {quality}")
    if convert:
        print(f"🔄 Convert To   : {convert_format}")
    print("────────────────────────────\n")


def process_all_files(files, input_folder, output_folder, quality, convert_format, compress, convert):
    total_size_after = 0
    start_time = time.time()

    with tqdm(total=len(files), desc="⚔️  Casting Tiny no Jutsu", unit="img") as pbar:
        for filename in files:
            total_size_after += process_single_file(filename, input_folder, output_folder, quality, convert_format, compress, convert)
            pbar.update(1)

    duration = time.time() - start_time
    return total_size_after, duration


def process_single_file(filename, input_folder, output_folder, quality, convert_format, compress, convert):
    input_path = os.path.join(input_folder, filename)
    base_name, ext = os.path.splitext(filename)

    try:
        with Image.open(input_path) as img:
            if img.mode in ("RGBA", "P"):
                img = img.convert("RGB")

            output_ext = convert_format.lower() if convert_format else ext[1:].lower()
            output_filename = f"{base_name}.{output_ext}"
            output_path = os.path.join(output_folder, output_filename)

            save_kwargs = {}
            if compress or convert:
                if output_ext in ["jpg", "jpeg", "webp"]:
                    save_kwargs["quality"] = quality
                    save_kwargs["optimize"] = True

            img.save(output_path, output_ext.upper(), **save_kwargs)
            return os.path.getsize(output_path)

    except Exception as e:
        tqdm.write(f"⚠️ Error: {filename} → {e}")
        return 0


def print_summary(total_size_before, total_size_after, duration):
    size_reduction = total_size_before - total_size_after
    percent_reduction = (size_reduction / total_size_before * 100) if total_size_before > 0 else 0

    print("\n📊 Mission Complete")
    print("────────────────────────────")
    print(f"🕐 Duration       : {round(duration, 2)} sec")
    print(f"📦 Original Size  : {humanize.naturalsize(total_size_before)}")
    print(f"💾 Compressed Size: {humanize.naturalsize(total_size_after)}")
    print(f"📉 Saved          : {humanize.naturalsize(size_reduction)} ({percent_reduction:.2f}%)")
    print("🎉 Operation Successful — Images mastered with Tiny no Jutsu!\n")

def main():
    """Entry point for CLI with interactive prompts."""
    banner()

    parser = argparse.ArgumentParser(description="🌀 Tiny no Jutsu - Image Compressor & Converter")
    parser.add_argument("-i", "--input", help="Path to input folder")
    parser.add_argument("-o", "--output", help="Path to output folder")
    parser.add_argument("-q", "--quality", type=int, help="Compression quality (0-100)")
    parser.add_argument("-f", "--format", help="Convert format (e.g. webp, jpg, png)")
    parser.add_argument("--compress", action="store_true", help="Compress images")
    parser.add_argument("--convert", action="store_true", help="Convert format")

    args = parser.parse_args()

    # Step-by-step interactive prompts if arguments are missing
    if not args.input:
        args.input = input("📂 Enter input folder path: ").strip()
    if not args.output:
        args.output = input("📁 Enter output folder path: ").strip()

    if not args.compress and not args.convert:
        action = ""
        while action.lower() not in ["c", "x", "b"]:
            action = input("Choose action: [C]ompress, [X] Convert, [B]oth: ").strip().lower()
        args.compress = action in ["c", "b"]
        args.convert = action in ["x", "b"]

    if args.compress:
        if not args.quality:
            args.quality = input("⚙️  Enter compression quality (0-100, default 80): ").strip()
            args.quality = int(args.quality) if args.quality else 80

    if args.convert and not args.format:
        args.format = input("🔄 Enter format to convert to (e.g. webp, jpg, png): ").strip()

    process_images(
        input_folder=args.input,
        output_folder=args.output,
        quality=args.quality or 80,
        convert_format=args.format,
        compress=args.compress,
        convert=args.convert
    )


