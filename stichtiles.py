from PIL import Image
import os
import re

# Folder jaha tiles rakhe hai
tiles_folder = "Ahmedabad_TP_tiles01"
output_file = "stitched_map_ahmedabad.png"

# Regex to extract zoom, x, y
pattern = re.compile(r"(\d+)_(\d+)_(\d+)\.png")

tiles = []
for filename in os.listdir(tiles_folder):
    if filename.endswith(".png"):
        match = pattern.match(filename)
        if match:
            zoom, x, y = map(int, match.groups())
            tiles.append((x, y, os.path.join(tiles_folder, filename)))

# Get min/max tile indices
min_x = min(t[0] for t in tiles)
max_x = max(t[0] for t in tiles)
min_y = min(t[1] for t in tiles)
max_y = max(t[1] for t in tiles)

tile_size = 256
width = (max_x - min_x + 1) * tile_size
height = (max_y - min_y + 1) * tile_size

print(f"Final image size: {width} x {height}")

# Create blank image
stitched = Image.new("RGB", (width, height))

# Paste tiles in correct position
for x, y, filepath in tiles:
    img = Image.open(filepath)
    px = (x - min_x) * tile_size
    py = (y - min_y) * tile_size
    stitched.paste(img, (px, py))

stitched.save(output_file)
print(f"Stitched image saved as {output_file}")

