from pathlib import Path
import tomllib
import jsbeautifier
from tkinter import Tk
import time

tk = Tk()
opts = jsbeautifier.default_options()
opts.indent_size = 4

def checkFolder(path, isCritical = True, createFolder = False):
    folder = path.name
    if (not path.exists()):
        if (isCritical):
            print(f"Error: Could not find '{folder}' folder at '{path.parent.name}'.")
            raise SystemExit
        else:
            print(f"Warning: Could not find '{folder}' folder at '{path.parent.name}'.")
            if (createFolder):
                print(f"Creating missing {folder} folder at '{path.parent.name}.")
                path.mkdir()

tempFolder = Path(tk.clipboard_get())
if (not tempFolder.exists() or tempFolder.name != 'resources'):
    print('Copy the absolute path of the resources folder from where you want to convert the models.')
    while(not tempFolder.exists() or tempFolder.name != 'resources'):
        time.sleep(0.1)
        tempFolder = Path(tk.clipboard_get())
tk.destroy()

parentFolder = tempFolder
metainfFolder = parentFolder.joinpath("META-INF")

if (parentFolder.name != 'resources'):
    print("Error: You need to drag this script onto your resources folder, then execute it.")
    raise SystemExit

if (not metainfFolder.exists()):
    print("Error: Missing META-INF folder inside your resources folder.")
    raise SystemExit

with open(metainfFolder.joinpath('mods.toml'), 'rb') as f:
    data = tomllib.load(f)
    modId = data.get('mods')[0].get('modId')

modAssetsFolder = parentFolder.joinpath('assets', modId)

checkFolder(modAssetsFolder)

texturesFolder = modAssetsFolder.joinpath('textures')

checkFolder(texturesFolder)

textureBlockFolder = texturesFolder.joinpath('block')
textureItemFolder = texturesFolder.joinpath('item')

checkFolder(textureBlockFolder, False, True)
checkFolder(textureItemFolder, False, True)

modelsFolder = modAssetsFolder.joinpath('models')

checkFolder(modelsFolder)

modelBlockFolder = modelsFolder.joinpath('block')
modelItemFolder = modelsFolder.joinpath('item')

checkFolder(modelBlockFolder, False, True)
checkFolder(modelItemFolder, False, True)