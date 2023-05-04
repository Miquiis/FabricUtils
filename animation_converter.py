import json
import jsbeautifier
from setup import Setup
import copy

opts = jsbeautifier.default_options()
opts.indent_size = 4

def replace_post_with_vector(data, key):
    if isinstance(data, dict):
        if "post" in data:
            data["vector"] = data.pop("post")["vector"]
            data[key] = data.pop("lerp_mode")
        for key in data:
            replace_post_with_vector(data[key], key)
    elif isinstance(data, list):
        for item in data:
            replace_post_with_vector(item, None)

class AnimationConverter:
    def __init__(self):
        pass

    def start(self, setup : Setup):
        # Finds and inserts unassigned block textures to the list.
        animationsConverted = 0
        for animation in setup.animationsFolder.iterdir():
            if not animation.name.endswith(".json"):
                continue

            # load JSON data from file
            with open(animation, "r") as f:
                data = json.load(f)

            # replace "post" with "vector" recursively
            prevData = copy.deepcopy(data)
            replace_post_with_vector(data, None)

            if (prevData != data):
                animationsConverted += 1
                with open(animation, "w") as f:
                    json.dump(data, f, indent=4)
        if animationsConverted > 0:
            print(f"{animationsConverted} Animation(s) were converted.")
        else:
            print("No animations were found to be converted.")