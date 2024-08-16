import os
import shutil
import json
import re
from datetime import datetime

CATEGORY = "neogob"
EMOJI_FILE_TYPES = (".gif", ".png", ".apng", ".webp")
HOST = "sakurajima.social"
LICENSE = "CC BY-NC-SA 4.0"

name_pattern = re.compile(r"(a?)neogob_?(.*)\.a?png")

def clean_name(file_name):
    animated, emoji_name = name_pattern.match(file_name).groups()
    match(emoji_name):
        case "0_0":
            return "neogob_0_0"
        case "x_x":
            return "neogob_x_x"
        case "_":
            return "neogob__"
        case "_w_":
            return "neogob_w_"
        case "":
            return "neogob"
        case _:
            return f"{animated}neogob_{emoji_name}"

def make_emoji_json():
    emoji_list = []
    for emoji in os.scandir("neogob"):
        if emoji.name.endswith(EMOJI_FILE_TYPES):
            emoji = {
                "downloaded": True,
                "fileName": f"{emoji.name}",
                "emoji": {
                    "name": clean_name(emoji.name),
                    "category": CATEGORY,
                    "license": LICENSE,
                    "aliases": []
                }
            }
            emoji_list.append(emoji)
    data = {
        "metaVersion": 2,
        "host": HOST,
        "exportedAt": datetime.now().strftime("%Y-%m-%dT%H:%I:%SZ"),
        "emojis": emoji_list
    }
    with open(f"neogob/meta.json", "w") as f:
        json.dump(data, f, indent=4)

def make_pack_json():
    emoji_dict = {}
    for emoji in os.scandir("neogob"):
        if emoji.name.endswith(EMOJI_FILE_TYPES):
            emoji_dict[clean_name(emoji.name)] = f"{emoji.name}"
    data = {
        "files": emoji_dict,
        "pack": {},
        "count": len(emoji_dict)
    }
    with open(f"neogob/pack.json", "w") as f:
        json.dump(data, f, indent=4)

if __name__ == "__main__":
    make_emoji_json()
    make_pack_json()
    shutil.copy("LICENSE", f"neogob\\LICENSE")
    shutil.copy("THANKS", f"neogob\\THANKS")
    os.remove("neogob.zip")
    shutil.make_archive("neogob", "zip", "neogob")
    os.remove("neogob\\LICENSE")
    os.remove("neogob\\THANKS")
    os.remove("neogob\\pack.json")
    os.remove("neogob\\meta.json")