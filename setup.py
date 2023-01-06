from pathlib import Path
import tomllib
from tkinter import Tk
import time

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
        
        self.metainfFolder = self.resourceFolder.joinpath("META-INF")

        if (not self.metainfFolder.exists()):
            print("Error: Missing 'META-INF' folder inside your 'resources' folder.")
            return
        
        with open(self.metainfFolder.joinpath('mods.toml'), 'rb') as f:
            data = tomllib.load(f)
            self.modId = data.get('mods')[0].get('modId')

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


        self.ready = True