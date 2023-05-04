from setup import Setup
from texture_assigner import TextureAssigner
from lang_generator import LangGenerator
from project_creator import ProjectCreator
from animation_converter import AnimationConverter

setup = None

def _getSetup():
    global setup
    if (not setup):
        setup = Setup()
    return setup
        
def startup(reocurring = False):
    if (not reocurring):
        print("What do you wish do execute?")
    else: print("What do you wish do execute next?")
    print(" 1: Project Creator (ONLY WORKS WITH MY PROJECTS)")
    print(" 2: Texture Assigner")
    print(" 3: Lang Generator")
    print(" 4: Animation Converter")
    print(" 0: Exit")
    inp = input("Enter your response: ")

    if (inp == "0"): 
        raise SystemExit
    
    if (inp == "1"):
        ta = ProjectCreator()
        modId = input("Enter a mod id for the project: ")
        modName = input("Enter a mod name for the project: ")
        modDescription = input("Enter a mod description for the project: ")
        ta.createProject(modId, modName, modDescription)

    if (inp == "2"):
        ta = TextureAssigner()
        ta.start(_getSetup())

    if (inp == "3"):
        ta = LangGenerator()
        ta.start(_getSetup())

    if (inp == "4"):
        ta = AnimationConverter()
        ta.start(_getSetup())

    startup(True)
    
startup()