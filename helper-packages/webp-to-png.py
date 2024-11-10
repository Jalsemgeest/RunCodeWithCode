from PIL import Image
import sys

target_file = sys.argv[1]

output_dir = "/".join(target_file.split("/")[0:-1])
output_file = target_file.split("/")[-1].split(".")[0]

img = Image.open(target_file).convert("RGB")
img.save(f"{output_dir}/{output_file}.png", "png")

# Use like:
# python3 webp-to-png.py <path_to_webp>
# ex. python3 .\helper-packages\webp-to-png.py C:/Users/cptli/Documents/dev/HelpfulTools/helper-packages/alpha-tester.webp