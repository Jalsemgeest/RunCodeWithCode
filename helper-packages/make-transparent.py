from PIL import Image
import sys
import os

original_target = sys.argv[1]
target = original_target

if target.endswith(".jpg") or target.endswith(".jpeg"):
    img = Image.open(target)
    img.save(f"temp_file.png")
    target = "temp_file.png"

original_target = original_target.split("/")
original_target = original_target[len(original_target) -1].split('.')[0]

img = Image.open(target)
rgba = img.convert("RGBA")
datas = rgba.getdata()

def pixel_value_check(value, min, max):
    return value >= min and value <= max

def is_value(pixel, target_color, range=0):
    r_check = pixel_value_check(pixel[0], max(target_color[0] - range, 0), min(target_color[0] + range, 255))
    g_check = pixel_value_check(pixel[1], max(target_color[1] - range, 0), min(target_color[1] + range, 255))
    b_check = pixel_value_check(pixel[2], max(target_color[2] - range, 0), min(target_color[2] + range, 255))
    return r_check and g_check and b_check

newData = []
percentage = 0
total_datas = len(datas)
print(f"Going over {total_datas} pixels...")
for x, target_color in enumerate(datas):
    if (x % (total_datas // 10) == 0):
        percentage += 10
        print(f"{percentage}% Complete...")
    if is_value(target_color, (255, 255, 255), 10):  # finding white 
        # replacing it with a transparent value 
        newData.append((255, 255, 255, 0)) 
    else: 
        newData.append(target_color) 

rgba.putdata(newData) 
print("Saving png...")
rgba.save(os.path.join(os.path.realpath(os.path.join(os.getcwd(), os.path.dirname(sys.argv[1]))), f"transparent_{original_target}.png"), "PNG")
print("Done")

if (os.path.isfile(target)):
    os.remove(target)