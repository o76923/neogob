from PIL import Image

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
    first_image = None
    last_image = None
    with Image.open("neogob/neogob_happy.png") as im:
        first_image = im.convert("RGBA")
    with Image.open("neogob/neogob_owo.png") as im:
        last_image = im.convert("RGBA")

    first_image.save(
        "neogob/aneogob_blink.apng", 
        save_all=True, 
        append_images=[last_image, first_image],
        loop=0,
        duration=[700, 7000, 700],
        disposal=0,
        blend=0
    )

if __name__ == "__main__":
    make_blink()
    make_alternating("aneogob_bongo", "neogob_bongo_up", "neogob_bongo_down")
    make_alternating("aneogob_bongo_fast", "neogob_bongo_up", "neogob_bongo_down", 160)
    make_alternating("aneogob_bongo_faster", "neogob_bongo_up", "neogob_bongo_down", 100)
    make_alternating("aneogob_bongo_hyper", "neogob_bongo_up", "neogob_bongo_down", 60)
    make_alternating("aneogob_mlem", "neogob_blep", "neogob")
    make_alternating("aneogob_talk", "neogob_yell", "neogob")
