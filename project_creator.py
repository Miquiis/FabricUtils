import shutil
from pathlib import Path
from tkinter import Tk
from jproperties import Properties
import tomllib
import os, stat
import json
import toml

class ProjectCreator:
    def __init__(self):
        pass
    
    def createProject(self, modId:str, modName:str = "New Mod", modDescription:str = "Lorem ipsum here"):
        self.modId = modId
        self.modName = modName
        self.modDescription = modDescription

        self.templateFolder = self.getTemplateFolder()
        self.destinationFolder = Path(self.getDestinationFolder()).joinpath(modName)
        self.projectFolder = shutil.copytree(self.templateFolder, self.destinationFolder)

        # os.chmod(os.path.join(self.projectFolder, '.git'), stat.S_IWRITE)
        # shutil.rmtree(os.path.join(self.projectFolder, '.git'))

        self.updateVariables()

    def loadProject(self, modId:str, modName:str = "New Mod", modDescription:str = "Lorem ipsum here"):
        self.modId = modId
        self.modName = modName
        self.modDescription = modDescription

        self.projectFolder = self.getProjectFolder()

        self.updateVariables()

    def updateVariables(self):
        # Gradle
        gradleProperties = Properties()
        with open(os.path.join(self.projectFolder, 'gradle.properties'), 'r+b') as gradlePropertiesFile:
            gradleProperties.load(gradlePropertiesFile)
            gradleProperties["archives_base_name"] = self.modId
            gradleProperties["maven_group"] = "work.tbnr"
            gradlePropertiesFile.seek(0)
            gradlePropertiesFile.truncate(0)
            gradleProperties.store(gradlePropertiesFile)

        # Rename package
        os.rename(os.path.join(self.projectFolder, 'src\main\java\work\\tbnr\examplemod'), os.path.join(self.projectFolder, f'src\main\java\work\\tbnr\{self.modId}'))

        # Refactor all packages
        for root, dirs, files in os.walk( os.path.join(self.projectFolder, f'src\main\java\work\\tbnr\{self.modId}'), topdown=False):
            for file in files:
                if(file.endswith(".java")):
                    filePath = os.path.join(root, file)
                    with open(filePath, "r") as f:
                        data = f.read()
                        data = data.replace("work.tbnr.examplemod", "work.tbnr." + self.modId)
                        with open(filePath, "w") as fw:
                            fw.write(data)

        #Rename Mixin Json
        os.rename(os.path.join(self.projectFolder, 'src\main\\resources\examplemod.mixins.json'), os.path.join(self.projectFolder, f'src\main\\resources\{self.modId}.mixins.json'))

        #Adjust Mixin Json properties
        with open(os.path.join(self.projectFolder, f'src\main\\resources\{self.modId}.mixins.json'), 'r') as f:
            mixinJson = json.load(f)
            mixinJson["package"] = f'work.tbnr.{self.modId}.mixin'
            with open(os.path.join(self.projectFolder, f'src\main\\resources\{self.modId}.mixins.json'), 'w') as fw:
                json.dump(mixinJson, fw, indent=2)
        
        #Adjust Fabric Json properties
        with open(os.path.join(self.projectFolder, f'src\main\\resources\\fabric.mod.json'), 'r') as f:
            fabricJson = json.load(f)
            fabricJson["id"] = self.modId
            fabricJson["name"] = self.modName
            fabricJson["description"] = self.modDescription
            fabricJson["icon"] = f"assets/{self.modId}/icon.png"
            
            fabricJson["entrypoints"]["main"] = [f"work.tbnr.{self.modId}.ExampleMod"]
            fabricJson["entrypoints"]["client"] = [f"work.tbnr.{self.modId}.ExampleMod"]
            fabricJson["entrypoints"]["fabric-datagen"] = [f"work.tbnr.{self.modId}.common.registry.ModDataGenerators"]

            fabricJson["mixins"] = [f"{self.modId}.mixins.json"]

            with open(os.path.join(self.projectFolder, f'src\main\\resources\\fabric.mod.json'), 'w') as fw:
                json.dump(fabricJson, fw, indent=2)

        # Rename current assets folder
        os.rename(os.path.join(self.projectFolder, 'src\main\\resources\\assets\\examplemod'), os.path.join(self.projectFolder, f'src\main\\resources\\assets\\{self.modId}'))

        self.assetsFolder = os.path.join(self.projectFolder, f'src\\main\\resources\\assets\\{self.modId}')

        # Creates directory for assets
        if not os.path.exists(self.assetsFolder):
            os.makedirs(self.assetsFolder, exist_ok=True)
        
        os.makedirs(os.path.join(self.assetsFolder, "geo"), exist_ok=True)
        os.makedirs(os.path.join(self.assetsFolder, "animations"), exist_ok=True)
        os.makedirs(os.path.join(self.assetsFolder, "models\\block"), exist_ok=True)
        os.makedirs(os.path.join(self.assetsFolder, "models\\entity"), exist_ok=True)
        os.makedirs(os.path.join(self.assetsFolder, "models\\item"), exist_ok=True)
        os.makedirs(os.path.join(self.assetsFolder, "textures\\block"), exist_ok=True)
        os.makedirs(os.path.join(self.assetsFolder, "textures\\entity"), exist_ok=True)
        os.makedirs(os.path.join(self.assetsFolder, "textures\\item"), exist_ok=True)
        os.makedirs(os.path.join(self.assetsFolder, "blockstates"), exist_ok=True)
        os.makedirs(os.path.join(self.assetsFolder, "lang"), exist_ok=True)

        self.dataFolder = os.path.join(self.projectFolder, f'src\\main\\resources\\data\\{self.modId}')

        # Creates directory for data
        if not os.path.exists(self.dataFolder):
            os.makedirs(self.dataFolder)
        
        #Change Java Reference File
        with open(os.path.join(self.projectFolder, f'src\main\java\work\\tbnr\{self.modId}\ModInformation.java'), "r") as f:
            data = f.read()
            data = data.replace("examplemod", self.modId)
            data = data.replace("ExampleMod", self.modName)
            with open(os.path.join(self.projectFolder, f'src\main\java\work\\tbnr\{self.modId}\ModInformation.java'), "w") as fw:
                fw.write(data)

    def _dumps_value(self, value):
        if isinstance(value, bool):
            return "true" if value else "false"
        elif isinstance(value, (int, float)):
            return str(value)
        elif isinstance(value, str):
            return f'"{value}"'
        elif isinstance(value, list):
            return f"[{', '.join(self._dumps_value(v) for v in value)}]"
        else:
            raise TypeError(f"{type(value).__name__} {value!r} is not supported")

    def getDestinationFolder(self) -> str:
        tk = Tk()
        inp = input("Copy (do not paste) the absolute file of your destination folder and press ENTER ")
        while (not Path(tk.clipboard_get()).exists()):
            inp = input("Copy (do not paste) the absolute file of your destination folder and press ENTER ")
            if (len(inp) > 0):
                raise SystemExit
        destinationFolder = tk.clipboard_get()
        tk.destroy()
        return destinationFolder

    def getProjectFolder(self) -> str:
        tk = Tk()
        inp = input("Copy (do not paste) the absolute file of your project folder and press ENTER ")
        while (not Path(tk.clipboard_get()).exists()):
            inp = input("Copy (do not paste) the absolute file of your project folder and press ENTER ")
            if (len(inp) > 0):
                raise SystemExit
        projectFolder = tk.clipboard_get()
        tk.destroy()
        return projectFolder

    def getTemplateFolder(self) -> str:
        tk = Tk()
        inp = input("Copy (do not paste) the absolute file of your template project and press ENTER ")
        while (not Path(tk.clipboard_get()).exists()):
            inp = input("Copy (do not paste) the absolute file of your template project and press ENTER ")
            if (len(inp) > 0):
                raise SystemExit
        templateFolder = tk.clipboard_get()
        tk.destroy()
        return templateFolder
