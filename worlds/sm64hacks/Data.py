from typing import List, Tuple
from pathlib import Path
from importlib import resources
from importlib.resources.abc import Traversable
import pkgutil
import Utils
import json
import re
import os


sm64hack_items: Tuple[str] = (
    "Key 1", 
    "Key 2", 
    "Wing Cap", 
    "Vanish Cap", 
    "Metal Cap", 
    "Power Star", 
    "Progressive Key", 
    "Course 1 Cannon",
    "Course 2 Cannon",
    "Course 3 Cannon",
    "Course 4 Cannon",
    "Course 5 Cannon",
    "Course 6 Cannon",
    "Course 7 Cannon",
    "Course 8 Cannon",
    "Course 9 Cannon",
    "Course 10 Cannon",
    "Course 11 Cannon",
    "Course 12 Cannon",
    "Course 13 Cannon",
    "Course 14 Cannon",
    "Course 15 Cannon",
    "Bowser 1 Cannon",
    "Bowser 2 Cannon",
    "Bowser 3 Cannon",
    "Slide Cannon",
    "Secret 1 Cannon",
    "Secret 2 Cannon",
    "Secret 3 Cannon",
    "Metal Cap Cannon",
    "Wing Cap Cannon",
    "Vanish Cap Cannon",
    "Overworld Cannon",
    "Progressive Stomp Badge",
    "Wall Badge",
    "Triple Jump Badge",
    "Lava Badge",
    "Overworld Cannon Star",
    "Bowser 2 Cannon Star",
    "Yellow Switch",
    "Black Switch",
    "Coin",
    "Green Demon Trap",
    "Mario Choir",
    "Heave-Ho Trap",
    "Squish Trap"
)

traps: Tuple[str] = (
    "Green Demon Trap",
    "Mario Choir",
    "Heave-Ho Trap",
    "Squish Trap"
)

badges: Tuple[str] = (
    "Super Badge",
    "Ultra Badge",
    "Wall Badge",
    "Triple Jump Badge",
    "Lava Badge"
)

star_like: Tuple[str] = (
    "Power Star",
    "Overworld Cannon Star",
    "Bowser 2 Cannon Star"
)

c1 = [{"exists": True}, {"exists": True}, {"exists": True}, {"exists": True}, {"exists": True}, {"exists": True, "Requirements": ["Wing Cap"]}, {"exists": True, "Requirements": ["Vanish Cap"]}]
c2 = [{"exists": True}, {"exists": True}, {"exists": True}, {"exists": True}, {"exists": True}, {"exists": True, "Requirements": ["Wing Cap"]}, {"exists": True, "Requirements": ["Vanish Cap"]}]
c3 = [{"exists": True}, {"exists": True}, {"exists": True}, {"exists": True}, {"exists": True}, {"exists": True, "Requirements": ["Wing Cap"]}, {"exists": True, "Requirements": ["Vanish Cap"]}]
c4 = [{"exists": True}, {"exists": True}, {"exists": True}, {"exists": True}, {"exists": True}, {"exists": True, "Requirements": ["Wing Cap"]}, {"exists": True, "Requirements": ["Vanish Cap"]}]
c5 = [{"exists": True}, {"exists": True}, {"exists": True}, {"exists": True}, {"exists": True}, {"exists": True, "Requirements": ["Wing Cap"]}, {"exists": True, "Requirements": ["Vanish Cap"]}]
c6 = [{"exists": True}, {"exists": True}, {"exists": True}, {"exists": True}, {"exists": True}, {"exists": True, "Requirements": ["Wing Cap"]}, {"exists": True, "Requirements": ["Vanish Cap"]}]
c7 = [{"exists": True}, {"exists": True}, {"exists": True}, {"exists": True}, {"exists": True}, {"exists": True, "Requirements": ["Wing Cap"]}, {"exists": True, "Requirements": ["Vanish Cap"]}]
c8 = [{"exists": True}, {"exists": True}, {"exists": True}, {"exists": True}, {"exists": True}, {"exists": True, "Requirements": ["Wing Cap"]}, {"exists": True, "Requirements": ["Vanish Cap"]}]
c9 = [{"exists": True}, {"exists": True}, {"exists": True}, {"exists": True}, {"exists": True}, {"exists": True, "Requirements": ["Wing Cap"]}, {"exists": True, "Requirements": ["Vanish Cap"]}]
c10 = [{"exists": True}, {"exists": True}, {"exists": True}, {"exists": True}, {"exists": True}, {"exists": True, "Requirements": ["Wing Cap"]}, {"exists": True, "Requirements": ["Vanish Cap"]}]
c11 = [{"exists": True}, {"exists": True}, {"exists": True}, {"exists": True}, {"exists": True}, {"exists": True, "Requirements": ["Wing Cap"]}, {"exists": True, "Requirements": ["Vanish Cap"]}]
c12 = [{"exists": True}, {"exists": True}, {"exists": True}, {"exists": True}, {"exists": True}, {"exists": True, "Requirements": ["Wing Cap"]}, {"exists": True, "Requirements": ["Vanish Cap"]}]
c13 = [{"exists": True}, {"exists": True}, {"exists": True}, {"exists": True}, {"exists": True}, {"exists": True, "Requirements": ["Wing Cap"]}, {"exists": True, "Requirements": ["Vanish Cap"]}]
c14 = [{"exists": True}, {"exists": True}, {"exists": True}, {"exists": True}, {"exists": True}, {"exists": True, "Requirements": ["Wing Cap"]}, {"exists": True, "Requirements": ["Vanish Cap"]}]
c15 = [{"exists": True}, {"exists": True}, {"exists": True}, {"exists": True}, {"exists": True}, {"exists": True, "Requirements": ["Wing Cap"]}, {"exists": True, "Requirements": ["Vanish Cap"]}]

b1 = [{"exists": True}, {"exists": True}, {"exists": True}, {"exists": True}, {"exists": True}, {"exists": True}, {"exists": True}]
b2 = [{"exists": True}, {"exists": True}, {"exists": True}, {"exists": True}, {"exists": True}, {"exists": True}, {"exists": True}]
b3 = [{"exists": True}, {"exists": True}, {"exists": True}, {"exists": True}, {"exists": True}, {"exists": True}, {"exists": True}]

slide = [{"exists": True}, {"exists": True}, {"exists": True}, {"exists": True}, {"exists": True}, {"exists": True}, {"exists": True}]
s1 = [{"exists": True}, {"exists": True}, {"exists": True}, {"exists": True}, {"exists": True}, {"exists": True}, {"exists": True}]
s2 = [{"exists": True}, {"exists": True}, {"exists": True}, {"exists": True}, {"exists": True}, {"exists": True}, {"exists": True}]
s3 = [{"exists": True}, {"exists": True}, {"exists": True}, {"exists": True}, {"exists": True}, {"exists": True}, {"exists": True}]

mc = [{"exists": True}, {"exists": True}, {"exists": True}, {"exists": True}, {"exists": True}, {"exists": True}, {"exists": True}]
wc = [{"exists": True}, {"exists": True}, {"exists": True}, {"exists": True}, {"exists": True}, {"exists": True}, {"exists": True}]
vc = [{"exists": True}, {"exists": True}, {"exists": True}, {"exists": True}, {"exists": True}, {"exists": True}, {"exists": True}]

ow = [{"exists": True}, {"exists": True}, {"exists": True, "StarRequirement":15}, {"exists": True, "StarRequirement":50}, {"exists": True, "StarRequirement":25}, {"exists": True, "StarRequirement":35}, {"exists": True, "StarRequirement":10}]

other = [{"exists": True}, {"exists": True}, {"exists": True}, {"exists": True}, {"exists": True, "StarRequirement":50}]


sr6_25_locations = ( #special = hack-specific
    "Yellow Switch",
    "Bowser Fight Reds",
    "Star 210",
    "Toursome Trouble RT Star 1",
    "Toursome Trouble RT Star 2",
    "Toursome Trouble RT Star 3",
    "Toursome Trouble RT Star 4",
    "Toursome Trouble RT Star 5",
    "Toursome Trouble RT Star 6",
)

def find_json_files(directory: Traversable):
    if directory.is_file() and directory.endswith("json"):
        return directory
    if directory.is_dir():
        ret = []

    print("gay", list(directory.iterdir()))


class Data:
    #default locations for location_name_to_id, will be overritten by import_json
    locations = {
        "Course 1": {"Stars": c1, "StarRequirement": 0,},
        "Course 2": {"Stars": c2, "StarRequirement": 0,},
        "Course 3": {"Stars": c3, "StarRequirement": 0,},
        "Course 4": {"Stars": c4, "StarRequirement": 10,},
        "Course 5": {"Stars": c5, "StarRequirement": 10,},
        "Course 6": {"Stars": c6, "StarRequirement": 0,},
        "Course 7": {"Stars": c7, "StarRequirement": 20,},
        "Course 8": {"Stars": c8, "StarRequirement": 20,},
        "Course 9": {"Stars": c9, "StarRequirement": 20,},
        "Course 10": {"Stars": c10, "StarRequirement": 0,},
        "Course 11": {"Stars": c11, "StarRequirement": 40,},
        "Course 12": {"Stars": c12, "StarRequirement": 40,},
        "Course 13": {"Stars": c13, "StarRequirement": 40,},
        "Course 14": {"Stars": c14, "StarRequirement": 75, "Requirements": ["Metal Cap"]},
        "Course 15": {"Stars": c15, "StarRequirement": 100,},
        "Bowser 1": {"Stars": b1, "StarRequirement": 20,},
        "Bowser 2": {"Stars": b2, "StarRequirement": 33,},
        "Bowser 3": {"Stars": b3, "StarRequirement": 80, "Requirements": ["Metal Cap"]},
        "Slide": {"Stars": slide, "StarRequirement": 20,},
        "Secret 1": {"Stars": s1, "StarRequirement": 80, "Requirements": ["Metal Cap"]},
        "Secret 2": {"Stars": s2, "StarRequirement": 80, "Requirements": ["Metal Cap"]},
        "Secret 3": {"Stars": s3, "StarRequirement": 0,},
        "Metal Cap": {"Stars": mc, "StarRequirement": 33,},
        "Wing Cap": {"Stars": wc, "StarRequirement": 100,},
        "Vanish Cap": {"Stars": vc, "StarRequirement": 50},
        "Overworld": {"Stars": ow, "StarRequirement": 0},
        "Other": {"Stars": other, "StarRequirement": 0} 
        #Other represents the keys + caps; the "star" ids 1 and 2 are keys 1 and 2, and 3-5 are wing, vanish, and metal cap
        #respectively
    }


    def import_json(self, file_name):
        json_dir = os.path.join(Utils.home_path(), "sm64hack_jsons")
        os.makedirs(json_dir, exist_ok=True)
        json_file = list(Path(json_dir).rglob(file_name)) #external takes priority over internal
        local_file = True
        if json_file == []:
            json_file = list(resources.files(__package__).joinpath("jsons").rglob(file_name))
            local_file = False
        if len(json_file) > 1:
            raise ValueError("Multiple JSON files with the same name detected")
        if len(json_file) == 0:
            raise FileNotFoundError(f"JSON file {file_name} does not exist")
        json_file = json_file[0]
        print(json_file)
        if(local_file):
            with open(json_file, 'r') as infile:
                filetext = infile.read()
                self.maxstarcount = max(int(i) for i in re.findall("\"StarRequirement\": *\"(\\d+)\"", filetext))
                self.locations = json.loads(filetext)
        else:
            json_file = str(json_file).replace("\\", "/") #extremely janky but it works
            print(json_file, resources.files(__package__))
            json_file = os.path.relpath(json_file, start=str(resources.files(__package__)).replace("\\", "/"))
            file = pkgutil.get_data(__name__, json_file).decode()
            filetext = file
            self.maxstarcount = max(int(i) for i in re.findall("\"StarRequirement\": *\"(\\d+)\"", filetext))
            self.locations = json.loads(filetext)





