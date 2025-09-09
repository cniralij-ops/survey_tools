import easyocr
import os

tiles_folder = "Ahmedabad_TP_tiles01gdn"
output_file = "tile_numbers01gdn.txt"
processed_file = "processed_tiles.txt"

reader = easyocr.Reader(['en'], gpu=False)

# Load already processed files into a set
if os.path.exists(processed_file):
    with open(processed_file, "r") as f:
        processed = set(line.strip() for line in f.readlines())
else:
    processed = set()

# Open the output file in append mode
with open(output_file, "a", encoding="utf-8") as out_f:
    # Process all PNG files
    for filename in os.listdir(tiles_folder):
        if not filename.lower().endswith(".png"):
            continue  # skip non-png files

        if filename in processed:
            print(f"⏩ Skipping {filename}, already processed.")
            continue  # skip already processed files

        filepath = os.path.join(tiles_folder, filename)
        print(f"Processing {filename}...")

        try:
            results = reader.readtext(filepath)

            out_f.write(f"File: {filename}\n")
            if results:
                for bbox, text, confidence in results:
                    out_f.write(f"Detected: {text} (Confidence: {confidence:.2f})\n")
                    print(f"  Detected: {text} (Confidence: {confidence:.2f})")
            else:
                out_f.write("No text detected\n")
                print("  No text detected")

            out_f.write("-" * 40 + "\n")

        except Exception as e:
            print(f"⚠️ Error processing {filename}: {e}")
            out_f.write(f"File: {filename}\nError: {e}\n")
            out_f.write("-" * 40 + "\n")

        # Mark as processed (success or error, dono case me)
        with open(processed_file, "a") as f:
            f.write(filename + "\n")
        processed.add(filename)  # also update in-memory set

print("\n✅ All new images processed, old ones skipped, and results saved.")

