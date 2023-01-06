from setup import Setup
from texture_assigner import TextureAssigner
from lang_generator import LangGenerator

def startup(reocurring = False):
    if setup.ready:
        if (not reocurring):
            print("What do you wish do execute?")
        else: print("What do you wish do execute next?")
        print(" 1: Texture Assigner")
        print(" 2: Lang Generator")
        print(" 3: Exit")
        inp = input("Enter your response: ")

        if (inp == "3"): 
            raise SystemExit
        
        if (inp == "1"):
            ta = TextureAssigner()
            ta.start(setup)

        if (inp == "2"):
            ta = LangGenerator()
            ta.start(setup)

        startup(True)

setup = Setup()

startup()