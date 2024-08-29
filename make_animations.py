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

if __name__ == "__main__":
    print("Started making animations")
    # make_blink()
    # make_alternating("aneogob_bongo", "neogob_bongo_up", "neogob_bongo_down")
    # make_alternating("aneogob_bongo_fast", "neogob_bongo_up", "neogob_bongo_down", 160)
    # make_alternating("aneogob_bongo_faster", "neogob_bongo_up", "neogob_bongo_down", 100)
    # make_alternating("aneogob_bongo_hyper", "neogob_bongo_up", "neogob_bongo_down", 60)
    # make_alternating("aneogob_mlem", "neogob_blep", "neogob")
    # make_alternating("aneogob_talk", "neogob_yell", "neogob")
    # make_alternating("aneogob_bongo_alt", "neogob_bongo_left", "neogob_bongo_right", 120)
    make_dizzy()