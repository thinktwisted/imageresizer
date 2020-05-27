#! python3
# imageResizer.py - resizes all images in a folder based on user input

import os
import pyautogui as gui
from PIL import Image

# Prompt the user for the resize percentage
prompt = gui.prompt('What is the resize percent?')
scale = int(prompt)/100
count = 0

# Loop over all the files in the current directory
for filename in os.listdir('.'):
    if not (filename.endswith('.png') or filename.endswith('.jpg') or \
            filename.endswith('.PNG') or filename.endswith('.JPG') or \
            filename.endswith('.jpeg') or filename.endswith('.JPEG')):
        continue # skips files that are not images

    if os.stat(filename).st_size/1000 < 1024:
        continue # skips files that are under 1MB already
    
    im = Image.open(filename)
    width, height = im.size
    print("Risizing " + filename + "...")
    im = im.resize((int(width*scale), int(height*scale)))
    im.save(filename)
    count += 1 # increment counter

print(str(count) + ' images resized.')
gui.alert(str(count) + ' images resized.', 'FINISHED!')
