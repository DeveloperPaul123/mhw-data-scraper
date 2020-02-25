from colorutils import *
import os
import cv2

def clamp(x): 
  return max(0, min(x, 255))

rootdir = 'images/items'

for subdir, dirs, files in os.walk(rootdir):
    for file in files:
        img = cv2.imread(os.path.join(subdir, file), cv2.IMREAD_COLOR)
        colors = get_dominant_color(img)
        r = int(round(colors[0]))
        g = int(round(colors[1]))
        b = int(round(colors[2]))
        hexcolor = "#{0:02x}{1:02x}{2:02x}".format(clamp(r), clamp(g), clamp(b))
        print("{} {}".format(file, colors))
