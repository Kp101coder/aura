from xml.dom import minidom
import distutils.util
import pathlib
import os
from typing import Tuple


class PetConfiguration:
    offset: int
    bg_color: str
    target_resolution: Tuple[int, int]

    def __init__(self, offset, bg_color, target_resolution):
        self.offset = offset
        self.bg_color = bg_color
        self.target_resolution = target_resolution


class XMLReader:
    path: str
    """
    Path to the xml data store
    """
    dom: minidom

    def __init__(self, path=None, dom=None):
        if dom is None:
            if path is None:
                path = os.path.join(pathlib.Path().resolve(), "config.xml")
            self.path = path
            self.dom = minidom.parse(path)
        else:
            self.path = path
            self.dom = dom

    def getDefaultPet(self):
        return self.getFirstTagValue("defualt_pet")
    
    def getDefaultPetData(self):
        pet_config = self.getMatchingPetConfigurationAsDom(self.getDefaultPet())
        pet_reader = XMLReader(dom=pet_config)
        description= pet_reader.getFirstTagValue("description")
        example= pet_reader.getFirstTagValue("example")
        return (description, example)

    def getForceTopMostWindow(self):
        return self.getFirstTagValueAsBool("force_topmost")

    def getShouldRunAnimationPreprocessing(self):
        return self.getFirstTagValueAsBool("should_run_preprocessing")
    
    def getInterfaceDescription(self):
        actionData = []
        actions = self.dom.getElementsByTagName("Action")
        for action in actions:
            name = action.getAttribute("name")
            actionReader = XMLReader(dom=action)
            description = actionReader.getFirstTagValue("description")
            codesData = []
            codes = actionReader.dom.getElementsByTagName("Code")
            for code in codes:
                codeName = code.getAttribute("name")
                codeReader = XMLReader(dom=code)
                codeDescription = codeReader.getFirstTagValue("description")
                codesDict = {
                    'name' : codeName,
                    'description' : codeDescription
                }
                codesData.append(codesDict)
            dict = {
                'name' : name,
                'description' : description,
                'codes' : codesData
            }
            actionData.append(dict)
        return actionData
    
    def getPetDescription(self, petname : str):
        pets = self.dom.getElementsByTagName("pet")
        for pet in pets:
            name = pet.getAttribute("name")
            if name == petname:
                petReader = XMLReader(dom=pet)
                data = (petReader.getFirstTagValue("description"), petReader.getFirstTagValue("example"))
                return data
            
    def getMatchingPetConfigurationAsDom(self, pet: str) -> minidom:
        pets = self.dom.getElementsByTagName("pet")
        pet_config = None
        for i in range(len(pets)):
            if pets[i].getAttribute("name") == pet:
                pet_config = pets[i]
        if pet_config is None:
            raise Exception(
                "Could not find the current pet as one of \
                the supported pets in the config.xml. 'current_pet' must \
                match one of the 'pet' element's 'name' attribute"
            )
        return pet_config

    def getMatchingPetConfigurationClean(self, pet: str) -> PetConfiguration:
        pet_config = self.getMatchingPetConfigurationAsDom(pet)
        pet_reader = XMLReader(dom=pet_config)
        offset = int(pet_reader.getFirstTagValue("offset"))
        bg_color = pet_reader.getFirstTagValue("bg_color")
        resolution = XMLReader(dom=pet_config.getElementsByTagName("resolution")[0])
        target_resolution = (
            int(resolution.getFirstTagValue("x")),
            int(resolution.getFirstTagValue("y")),
        )

        return PetConfiguration(offset, bg_color, target_resolution)

    def getFirstTagValueAsBool(self, tag_name: str) -> bool:
        return XMLReader.xml_bool(self.getFirstTagValue(tag_name))

    def getFirstTagValue(self, tag_name: str) -> str:
        return self.dom.getElementsByTagName(tag_name)[0].firstChild.nodeValue

    def setFirstTagValue(self, tag_name: str, val: any):
        self.dom.getElementsByTagName(tag_name)[0].firstChild.replaceWholeText(val)

    def save(self, path: str = None):
        if path is None:
            path = self.path

        with open(self.path, "w") as f:
            f.write(self.dom.toxml())

    @staticmethod
    def xml_bool(val: str) -> bool:
        return bool(distutils.util.strtobool(val))

if __name__ == "__main__":
    config = XMLReader()
    print(config.getInterfaceDescription())