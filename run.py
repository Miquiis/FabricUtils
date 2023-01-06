from setup import Setup
from texture_assigner import TextureAssigner
from lang_generator import LangGenerator

def startup():
    if setup.ready:
        print("What do you wish do execute?")
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

        startup()

setup = Setup()

startup()