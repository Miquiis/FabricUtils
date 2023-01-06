from setup import Setup
import os
import javalang
import json

def clearQuotes(string: str):
    return string[1:len(string) - 1]

def capitalizeWords(string: str):
    word = ""
    for s in string.split("_"):
        word += s.capitalize() + " "
    return word[:len(word) - 1]

def convertRegistryTypeToLangString(string : str):
    if string == "ENTITIES":
        return "entity"
    elif string == "BLOCKS":
        return "block"
    elif string == "ITEMS":
        return "item"
    return ""

class LangGenerator:

    def __init__(self):
        self.langDir = {}
        pass

    def start(self, setup : Setup):
        javaFolder = setup.projectFolder.joinpath("java")
        javaClasses = list()
        for root, dirs, files in os.walk(javaFolder, topdown=False):
            for file in files:
                if(file.endswith(".java")):
                    filePath = os.path.join(root, file)
                    javaClasses.append(filePath)
        registerClasses = list()
        for javaClass in javaClasses:
            with open(javaClass, "r") as f:
                tree = None
                try:
                    tree = javalang.parse.parse(f.read())
                except:
                    continue
                for path, node in tree.filter(javalang.tree.FieldDeclaration):
                    if isinstance(node.declarators[0].initializer, javalang.tree.MethodInvocation):
                        if len(node.declarators[0].initializer.arguments) > 0:
                            if isinstance(node.declarators[0].initializer.arguments[0], javalang.tree.MemberReference):
                                if node.declarators[0].initializer.arguments[0].qualifier == "ForgeRegistries":
                                    registryName = node.declarators[0].initializer.arguments[0].member
                                    if (registryName == "ENTITIES" or registryName == "ITEMS" or registryName == "BLOCKS"):
                                        registerClasses.append({"node": node, "path": path})
        for registerClass in registerClasses:
            for path, node in registerClass["path"][0].filter(javalang.tree.FieldDeclaration):
                if isinstance(node.declarators[0].initializer.arguments[0], javalang.tree.Literal):
                    id = clearQuotes(node.declarators[0].initializer.arguments[0].value)
                    name = capitalizeWords(id)
                    registryType = registerClass["node"].declarators[0].initializer.arguments[0].member
                    self.langDir[f"{convertRegistryTypeToLangString(registryType)}.{setup.modId}.{id}"] = name
        self.__output(setup.langFolder.joinpath("en_us.json"))

    def __output(self, outputFile : str):
        prevJson = {}
        if (os.path.exists(outputFile)):
            with open(outputFile, "r") as input:
                try:
                    prevJson = json.load(input)
                except:
                    pass
        with open(outputFile, "w") as output:
            output.write(json.dumps({**self.langDir, **prevJson}, indent=2, sort_keys=True))