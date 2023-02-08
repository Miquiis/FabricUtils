import shutil
from pathlib import Path
from tkinter import Tk
from jproperties import Properties
import tomllib
import os
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
            gradleProperties["mod_id"] = self.modId
            gradleProperties["mod_name"] = self.modName
            gradleProperties["mod_package"] = f"me.miquiis.{self.modId}"
            gradleProperties["mod_description"] = self.modDescription
            gradlePropertiesFile.seek(0)
            gradlePropertiesFile.truncate(0)
            gradleProperties.store(gradlePropertiesFile)

        # Rename package
        os.rename(os.path.join(self.projectFolder, 'src\main\java\me\miquiis\examplemod'), os.path.join(self.projectFolder, f'src\main\java\me\miquiis\{self.modId}'))

        # Refactor all packages
        for root, dirs, files in os.walk( os.path.join(self.projectFolder, f'src\main\java\me\miquiis\{self.modId}'), topdown=False):
            for file in files:
                if(file.endswith(".java")):
                    filePath = os.path.join(root, file)
                    with open(filePath, "r") as f:
                        data = f.read()
                        data = data.replace("me.miquiis.examplemod", "me.miquiis." + self.modId)
                        with open(filePath, "w") as fw:
                            fw.write(data)

        #Rename Mixin Json
        os.rename(os.path.join(self.projectFolder, 'src\main\\resources\examplemod.mixin.json'), os.path.join(self.projectFolder, f'src\main\\resources\{self.modId}.mixin.json'))

        #Adjust Mixin Json properties
        with open(os.path.join(self.projectFolder, f'src\main\\resources\{self.modId}.mixin.json'), 'r') as f:
            mixinJson = json.load(f)
            mixinJson["package"] = f'me.miquiis.{self.modId}.mixin'
            mixinJson["refmap"] = f'{self.modId}.mixin-refmap.json'
            with open(os.path.join(self.projectFolder, f'src\main\\resources\{self.modId}.mixin.json'), 'w') as fw:
                json.dump(mixinJson, fw, indent=2)
        
        #Adjust META-INF mods.toml
        with open(os.path.join(self.projectFolder, f'src\main\\resources\META-INF\mods.toml'), 'rb') as f:
            modsToml = tomllib.load(f)
            modsToml["mods"][0]["modId"] = self.modId
            modsToml["mods"][0]["displayName"] = self.modName
            modsToml["mods"][0]["description"] = self.modDescription
            modsToml["dependencies"][self.modId] = modsToml["dependencies"]["examplemod"]
            modsToml["dependencies"].pop("examplemod")
            with open(os.path.join(self.projectFolder, f'src\main\\resources\META-INF\mods.toml'), 'w') as fw:
                toml.dump(modsToml, fw)
        
        #Change Java Reference File
        with open(os.path.join(self.projectFolder, f'src\main\java\me\miquiis\{self.modId}\ModInformation.java'), "r") as f:
            data = f.read()
            data = data.replace("examplemod", self.modId)
            data = data.replace("ExampleMod", self.modName)
            with open(os.path.join(self.projectFolder, f'src\main\java\me\miquiis\{self.modId}\ModInformation.java'), "w") as fw:
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
