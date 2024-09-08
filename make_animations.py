import subprocess
import xml.etree.ElementTree as ET
import re
import os
import shutil
from PIL import Image

INKSCAPE_PATH = "C:\\Program Files\\Inkscape\\bin\\inkscape.com"
ET.register_namespace('', "http://www.w3.org/2000/svg")


def make_alternating(output_name, first_name, last_name, duration=200):
    first_image = None
    last_image = None
    with Image.open(f"neogob/{first_name}.png") as im:
        first_image = im.convert("RGBA")
    with Image.open(f"neogob/{last_name}.png") as im:
        last_image = im.convert("RGBA")

    first_image.save(
        f"neogob/{output_name}.apng", 
        save_all=True, 
        append_images=[last_image, ],
        loop=0,
        duration=duration,
        disposal=0,
        blend=0
    )

def make_blink():
    first_image = Image.open("neogob/neogob_happy.png").convert("RGBA")
    last_image = Image.open("neogob/neogob_owo.png").convert("RGBA")

    first_image.save(
        "neogob/aneogob_blink.apng", 
        save_all=True, 
        append_images=[last_image, first_image],
        loop=0,
        duration=[700, 7000, 700],
        disposal=0,
        blend=0
    )

def make_dizzy():
    gob = ET.parse("./svg/neogob_dizzy.svg")
    eye = gob.find(".//{http://www.w3.org/2000/svg}path[@id='left_eye']")
    os.mkdir("dizzy_dir")
    for rotation in range(6):
        eye.set("transform", f"rotate({rotation*(-60)} 1304 901)")
        gob.write(f"dizzy_dir/temp.svg")
        subprocess.run(f"{INKSCAPE_PATH} .\\dizzy_dir\\temp.svg --export-area-page -w 256 -h 256 --export-filename=.\\dizzy_dir\\neogob_dizzy{rotation:1d}.png")

    frames = []
    for offset in range(6):
        frames.append(Image.open(f"./dizzy_dir/neogob_dizzy{offset:1d}.png"))

    frames[0].save(
        "./neogob/aneogob_dizzy.apng",
        save_all=True,
        append_images=frames[1:],
        loop=0,
        duration=100,
    )

    shutil.rmtree("./dizzy_dir")

def make_walk():
    gob = ET.parse("./svg/neogob_legs.svg")
    right_leg_outline = gob.find(".//{http://www.w3.org/2000/svg}path[@id='right_leg_outline']")
    right_leg_fill = gob.find(".//{http://www.w3.org/2000/svg}path[@id='right_leg_fill']")
    left_leg_outline = gob.find(".//{http://www.w3.org/2000/svg}path[@id='left_leg_outline']")
    left_leg_fill = gob.find(".//{http://www.w3.org/2000/svg}path[@id='left_leg_fill']")
    bucket = gob.find(".//{http://www.w3.org/2000/svg}g[@id='bucket']")
    laces = gob.find(".//{http://www.w3.org/2000/svg}g[@id='laces']")

    left_leg = (left_leg_outline, left_leg_fill)
    right_leg = (right_leg_fill, right_leg_outline, laces, bucket)

    os.mkdir("walk_dir")

    gob.write(f"walk_dir/temp.svg")
    subprocess.run(f"{INKSCAPE_PATH} .\\walk_dir\\temp.svg --export-area-page -w 256 -h 390 --export-filename=.\\walk_dir\\neogob_walk0.png")

    for part in right_leg:
        part.set("transform", "translate(0 -120)")
    gob.write(f"walk_dir/temp.svg")
    subprocess.run(f"{INKSCAPE_PATH} .\\walk_dir\\temp.svg --export-area-page -w 256 -h 390 --export-filename=.\\walk_dir\\neogob_walk1.png")

    for part in right_leg:
        part.attrib.pop("transform", None)
    for part in left_leg:
        part.set("transform", "translate(0 -160)")
    gob.write(f"walk_dir/temp.svg")
    subprocess.run(f"{INKSCAPE_PATH} .\\walk_dir\\temp.svg --export-area-page -w 256 -h 390 --export-filename=.\\walk_dir\\neogob_walk2.png")

    for part in left_leg:
        part.set("transform", "translate(0 -320)")
    gob.write(f"walk_dir/temp.svg")
    subprocess.run(f"{INKSCAPE_PATH} .\\walk_dir\\temp.svg --export-area-page -w 256 -h 390 --export-filename=.\\walk_dir\\neogob_walk3.png")

    for part in left_leg:
        part.set("transform", "translate(0 -480)")
    gob.write(f"walk_dir/temp.svg")
    subprocess.run(f"{INKSCAPE_PATH} .\\walk_dir\\temp.svg --export-area-page -w 256 -h 390 --export-filename=.\\walk_dir\\neogob_walk4.png")

    frames = []
    for offset in range(6):
        frames.append(Image.open(f"./walk_dir/neogob_walk{offset:1d}.png"))
    
    frame_order = [1, 0, 2, 3, 4, 3, 2]

    frames[0].save(
        "./neogob/aneogob_walk.apng",
        save_all=True,
        append_images=[frames[f] for f in frame_order],
        loop=0,
        duration=[72, 144, 72, 72, 72, 72, 72, 72, 72]
    )

    shutil.rmtree("./walk_dir")

if __name__ == "__main__":
    print("Started making animations")
    make_blink()
    make_alternating("aneogob_bongo", "neogob_bongo_up", "neogob_bongo_down")
    make_alternating("aneogob_bongo_fast", "neogob_bongo_up", "neogob_bongo_down", 160)
    make_alternating("aneogob_bongo_faster", "neogob_bongo_up", "neogob_bongo_down", 100)
    make_alternating("aneogob_bongo_hyper", "neogob_bongo_up", "neogob_bongo_down", 60)
    make_alternating("aneogob_mlem", "neogob_blep", "neogob")
    make_alternating("aneogob_talk", "neogob_yell", "neogob")
    make_alternating("aneogob_bongo_alt", "neogob_bongo_left", "neogob_bongo_right", 120)
    make_walk()