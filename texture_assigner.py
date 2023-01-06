import json
import os
import jsbeautifier
from setup import Setup
from pathlib import Path

opts = jsbeautifier.default_options()
opts.indent_size = 4

class TextureAssigner:
    def __init__(self):
        self.unassignedItemModels = list()
        self.unassignedBlockModels = list()
    
    def start(self, setup : Setup):
        # Finds and inserts unassigned block textures to the list.
        for blockModel in setup.modelBlockFolder.iterdir():
            with open(blockModel) as f:
                data = json.load(f)
                if (not 'textures' in data): continue
                textures = data['textures']
                for key in textures:
                    isAssigned = len(str(textures[key]).split(':')) > 1
                    if (not isAssigned):
                        self.unassignedBlockModels.append(blockModel)
                        break

        # Finds and inserts unassigned item textures to the list.
        def findAndAssignItem(folder : Path):
            for itemModel in folder.iterdir():
                if (itemModel.is_dir()): 
                    findAndAssignItem(itemModel)
                    continue
                with open(itemModel) as f:
                    try:
                        data = json.load(f)
                    except json.JSONDecodeError as e:
                        continue 
                    if (not 'textures' in data): continue
                    textures = data['textures']
                    for key in textures:
                        isAssigned = len(str(textures[key]).split(':')) > 1
                        if (not isAssigned):
                            self.unassignedItemModels.append(itemModel)
                            break
        findAndAssignItem(setup.modelItemFolder)

        if (len(self.unassignedBlockModels) == 0 and len(self.unassignedItemModels) == 0):
            print("No unassigned textures were found, make sure to add your items and blocks to the models folder!")
            return
        
        print(f"Found {len(self.unassignedItemModels)} unassigned item textures.")
        print(f"Found {len(self.unassignedBlockModels)} unassigned block textures.")

        inp = input('Do you wish to continue? Y/N ')
        if (str(inp).lower() == 'n'): return

        convertedBlockModels = 0
        convertedItemModels = 0

        for blockModel in self.unassignedBlockModels:
            with open(blockModel) as f:
                model = json.load(f)
                if (not 'textures' in model): continue
                textures = model['textures']
                for key in textures:
                    model['textures'][key] = f"{setup.modId}:block/{os.path.splitext(blockModel.name)[0]}"
                with open(blockModel, 'w') as f:
                    f.write(jsbeautifier.beautify(json.dumps(model), opts))
                    convertedBlockModels += 1

        for itemModel in self.unassignedItemModels:
            with open(itemModel) as f:
                model = json.load(f)
                if (not 'textures' in model): continue
                textures = model['textures']
                for key in textures:
                    model['textures'][key] = f"{setup.modId}:item/{os.path.splitext(itemModel.name)[0]}"
                with open(itemModel, 'w') as f:
                    f.write(jsbeautifier.beautify(json.dumps(model), opts))
                    convertedItemModels += 1

        if (convertedBlockModels > 0):
            print(f"Finished converting {convertedBlockModels} block model(s).")

        if (convertedItemModels > 0):
            print(f"Finished converting {convertedItemModels} item model(s).")