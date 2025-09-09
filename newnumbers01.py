import easyocr
import os
from PIL import Image, ImageFile

# Allow loading of truncated images
ImageFile.LOAD_TRUNCATED_IMAGES = True

tiles_folder = "Ahmedabad_TP_tiles01gdn"
output_file = "tile_numbers01gdn.txt"
processed_file = "processed_tiles.txt"

reader = easyocr.Reader(['en'], gpu=False)

# Load already processed files
if os.path.exists(processed_file):
    with open(processed_file, "r") as f:
        processed = set(line.strip() for line in f.readlines())
else:
    processed = set()

with open(output_file, "a", encoding="utf-8") as out_f:
    for filename in os.listdir(tiles_folder):
        if filename.lower().endswith(".png") and filename not in processed:
            filepath = os.path.join(tiles_folder, filename)
            print(f"Processing {filename}...")

            try:
                results = reader.readtext(filepath)
            except OSError:
                print(f"  Skipping corrupted image: {filename}")
                results = []

            out_f.write(f"File: {filename}\n")
            if results:
                for bbox, text, confidence in results:
                    out_f.write(f"Detected: {text} (Confidence: {confidence:.2f})\n")
                    print(f"  Detected: {text} (Confidence: {confidence:.2f})")
            else:
                out_f.write("No text detected\n")
                print("  No text detected")

            out_f.write("-" * 40 + "\n")

            # Mark as processed
            with open(processed_file, "a") as f:
                f.write(filename + "\n")

print("\nAll new images processed and results saved.")

