
# ForgeUtils

A collection of QoL scripts to use while creating Mods for Forge. It's completely written in Python, but essentially want to move over to Intellij for easy access.


## Usage/Examples

Start by running the `start.py`, it will prompt you to copy your 'main' folder of your project. On Intellij, you can just click on the folder and press `Ctrl+Shift+C` and it will copy the absolute path of that folder.

After doing that, you can return to the script, if you copied it correctly, it will automatically ask you what script you wish to run, otherwise, you probably copied the wrong file.

This is what your absolute path should look like:

```C:\Users\User\Projects\ExampleMod\src\main```
## Scripts

- Texture Assigner:
    - Looks up for any item or block models that doesn't have the modid before the texture and applies to it.
    - Example:
        The script will look for models like that:
        ```json
        {
            ...
            "textures": {
                "0": "fire_sword"
            },
        }
        ```
        and change them to this: (it will automatically put item or block accordingly)
        ```json
        {
            ...
            "textures": {
                "0": "modid:item/fire_sword"
            },
        }
        ```
- Lang Generator
    - Looks up for every item, block and entity registered in your project and creates a `en_us.json` file with all the translations applied. 
    - It creates a `en_us.json` file in your `resources/assets/modid/lang/` folder automatically. If there is already an existing lang file, it will keep all changes from the old one and append missing keys to it. That means, it prioritizes the file that already exists over the one auto-generated, for sake of changing values after without them being overrided.
    - It follows the current rule for naming:
        - It will automatically capitalize all starting letters
        - It will swap '_' with ' '
    - Example: `flame_sword` to `Flame Sword`

## Contributing

Contributions are always welcome!

I will definitely will be implementing more scripts later on, those were just to start off and see how well it works in a real project.

