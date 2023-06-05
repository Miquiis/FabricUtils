from pathlib import Path
import tomllib
from tkinter import Tk
import time
import os
import json

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

class Setup:

    def __init__(self):
        self.ready = False
        self.__setupProjectFolder()

    def __setupProjectFolder(self):
        tk = Tk()
        tempFolder = Path(tk.clipboard_get())
        if (not tempFolder.exists() or tempFolder.name != 'main'):
            print('Copy the absolute path of the \'main\' folder of your project.')
            while(not tempFolder.exists() or tempFolder.name != 'main'):
                time.sleep(0.1)
                tempFolder = Path(tk.clipboard_get())
        tk.destroy()

        self.projectFolder = tempFolder
        self.resourceFolder = self.projectFolder.joinpath("resources")

        if (not self.resourceFolder.exists()):
            print("Error: The 'resource' folder was not able to be found. Make sure your project is setup correctly.")
            return
        
        with open(os.path.join(self.projectFolder, f'resources\\fabric.mod.json'), 'r') as f:
            fabricJson = json.load(f)
            self.modId = fabricJson["id"]

        self.modAssetsFolder = self.resourceFolder.joinpath('assets', self.modId)
        checkFolder(self.modAssetsFolder)
        self.langFolder = self.modAssetsFolder.joinpath('lang')
        checkFolder(self.langFolder, False, True)
        self.texturesFolder = self.modAssetsFolder.joinpath('textures')
        checkFolder(self.texturesFolder, False, True)
        self.textureBlockFolder = self.texturesFolder.joinpath('block')
        self.textureItemFolder = self.texturesFolder.joinpath('item')
        checkFolder(self.textureBlockFolder, False, True)
        checkFolder(self.textureItemFolder, False, True)
        self.modelsFolder = self.modAssetsFolder.joinpath('models')
        checkFolder(self.modelsFolder)
        self.modelBlockFolder = self.modelsFolder.joinpath('block')
        self.modelItemFolder = self.modelsFolder.joinpath('item')
        checkFolder(self.modelBlockFolder, False, True)
        checkFolder(self.modelItemFolder, False, True)
        self.geoFolder = self.modAssetsFolder.joinpath('geo')
        checkFolder(self.geoFolder, False, True)
        self.animationsFolder = self.modAssetsFolder.joinpath('animations')
        checkFolder(self.animationsFolder, False, True)

        self.ready = True